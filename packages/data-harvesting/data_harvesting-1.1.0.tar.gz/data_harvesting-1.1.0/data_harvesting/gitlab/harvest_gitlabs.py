# -*- coding: utf-8 -*-
#############################################################################################
# Copyright (c), Helmholtz Metadata Collaboration (HMC). All rights reserved.               #
# This file is part of the data-harvesting package.                                             #
# The code is hosted at https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting  #
# For further information on the license, see the LICENSE file                              #
# For further information please visit  https://www.helmholtz-metadaten.de/en               #
#############################################################################################
"""This module contains the code for the gitlab harvester pipeline"""
import json
import os
import shutil
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import requests

from data_harvesting.base_harvester import Harvester
from data_harvesting.data_model import derive_metadata
from data_harvesting.data_model import LinkedDataObject
'''
# we do this: curl --head --request GET "https://jugit.fz-juelich.de/api/v4/projects" > jugit_projects.json
# https://jugit.fz-juelich.de/api/v4/projects?pagination=keyset&non_archived=true&page=2&sort=desc&order_by=id&visibility_level=20&per_page=100
# walking the pages is not trivial, there are links to next pages

{'Date': 'Mon, 10 Oct 2022 13:57:41 GMT', 'Server': 'Apache/2.4.41 (Ubuntu)', 'Cache-Control':
'max-age=0, private, must-revalidate', 'Content-Type': 'application/json', 'Etag': 'W/"6464f11edaeef1b44cf221be7f278ac1"', 'Link': '<https://jugit.fz-juelich.de/api/v4/projects?id_before=7183&imported=false&membership=false&non_archived=true&order_by=id&owned=false&page=1&pagination=keyset&per_page=2&simple=false&sort=desc&starred=false&statistics=false&visibility_level=20&with_custom_attributes=false&with_issues_enabled=false&with_merge_requests_enabled=false>; rel="next"', 'Vary': 'Origin', 'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'SAMEORIGIN', 'X-Request-Id': '01GF12ZRAN75XCXWGY8N903EJA', 'X-Runtime': '0.075538', 'Content-Length': '1918', 'Strict-Transport-Security': 'max-age=15768000;includeSubdomains', 'Keep-Alive': 'timeout=5, max=100', 'Connection': 'Keep-Alive'}

# Helpful to do export GIT_TERMINAL_PROMPT=0
link = "https://jugit.fz-juelich.de/api/v4/projects?pagination=keyset&non_archived=true&page=1&sort=desc&order_by=id&visibility_level=20&per_page=100"

'''


def load_gitlabs_meta():
    """Load all metadata about gitlabs to harvest"""
    this_file = Path(__file__).resolve().parent
    gitlab_json_path = this_file.joinpath('gitlabs.json')
    results_folder = this_file.joinpath('results')
    gitlabs_url = []
    with open(gitlab_json_path, 'r', encoding='utf-8') as fileo:
        gitlabs_meta = json.load(fileo)

    for key, val in gitlabs_meta.items():
        for valu in val:
            gitlabs_url.append(valu['url'])
    return gitlabs_meta


# loading the gitlab data from the config
# we do this once to not do it on every function call..
# still this has to be done in some other way...
#gitlabs_meta = load_gitlabs_meta()

#for giturl in gitlaburls:
#    harest_fullgitlab(base_url=giturl)
# gitlab API https://gitlab.example.com/api/v4/projects

# retrieve public gitlab project list and save it with a date to a file...
# authenticated metadata is richer...


def request_gitlab(link: str):
    """Request a response form the gitlab API

    #TODO: authenticate
    #try and error, look at restrictions
    """
    response = requests.get(link, timeout=(5, 30))
    header = response.headers
    #print(response.status_code)
    # check status..

    return response, header


def walk_gitlab(start_link: str,
                destination_folder: Union[str, Path] = '.',
                gitlab_name: str = 'jugit') -> Tuple[list, List[Path]]:
    """Walk through gitlab pages to extract public repo metadata

    and store it into files.
    One gets only 100 projects max, so one as to walk the pages.
    for this the gitlab API as a mechanism.

    example
    link = "https://jugit.fz-juelich.de/api/v4/projects?pagination=keyset&non_archived=true&page=1&sort=desc&order_by=id&visibility_level=20&per_page=100"

    """
    # request public projects metadata
    # the git APIs have restrictions...

    link = start_link
    next_page = True
    i = 0
    results_files = []
    headers = []
    while next_page:
        response, header = request_gitlab(link)
        # print(response.status_code)
        headers.append(header)
        next_link = header.get('Link')

        projects_json_file = Path(f'{destination_folder}/{gitlab_name}_projects{i}.json').resolve()
        results_files.append(projects_json_file)

        # somehow the last files/pages are always empty...
        with open(projects_json_file, 'wb') as fileo:
            res_json = response.content
            fileo.write(res_json)
        i = i + 1

        if next_link is None:
            break
        link_s = next_link.split('; rel=')
        link = link_s[0].replace('<', '').replace('>', '')
        next_l = link_s[1]
        next_page = bool(next_l == '"next"')

    return headers, results_files


def harvest_fullgitlab(projects_metadata_json: Path, gitlab_name: str = 'gitlab', base_savepath: Optional[Path] = None):
    """
    For each repository found in the given metadata, from the Gitlab API
    provided under the given filepath, call harvest_project.

    """
    # in oder to run codemeta harvester we need the source code...
    with open(projects_metadata_json, 'r', encoding='utf-8') as fileo:
        all_project = json.load(fileo)

    for i, project in enumerate(all_project):
        print(i)
        gitrepo_url = project.get('ssh_url_to_repo')
        repo_url = project.get('web_url')
        # the reponame is not enough, names are not unique, we therefore use the
        # group plus reponame as repo_name on disk
        repo_name = project.get('path')  #_with_namespace") #path
        name_space = project.get('namespace').get('path')
        http_url_to_repo = project.get('http_url_to_repo')
        harvest_project(
            gitrepo_url,
            repo_url,
            reponame=repo_name,
            http_url_to_repo=http_url_to_repo,
            repo_name_space=name_space,
            gitlab_name=gitlab_name,
            base_savepath=base_savepath
        )


def harvest_project(
    gitrepo_url: str,
    repo_url: str,
    http_url_to_repo: Optional[str] = None,
    reponame: Optional[str] = None,
    repo_name_space='.',
    gitlab_name: str = 'gitlab',
    copy_codemeta: bool = True,
    base_savepath: Optional[Path] = None,
    unhidedata: bool = True
):
    """
    Clone a single repo and try to generate a code meta for it

    per default code meta gets copied to a results folder
    copy_codemeta: If this is True the codemeta.json also stays with the source code
    """
    if reponame is None:
        reponame = gitrepo_url.split('/')[-1].split('.')[0]
        print(reponame)
    if base_savepath is None:
        this_path = Path('.').resolve()
    else:
        this_path = base_savepath.resolve()
    repo_paths = this_path / f'cloned_repos/{gitlab_name}/{repo_name_space}'

    if not repo_paths.exists():
        repo_paths.mkdir(parents=True)
    os.chdir(repo_paths)

    repo_path = Path(f'./{reponame}').resolve()
    if not repo_path.exists():
        if http_url_to_repo is None:
            http_url_to_repo = gitrepo_url
        #print(f'Git ssh clone failed, I skip this: {gitrepo_url}')
        # also see https://serverfault.com/questions/544156/git-clone-fail-instead-of-prompting-for-credentials
        # the ssh clone is better, but fails for some, once gets ask a general password and has to add the server to known hosts...
        # one has to figure out how to circumvent this, probably needed for merge requests...
        #result = subprocess.run(["GIT_TERMINAL_PROMPT=0", "git", "clone", gitrepo_url]) # or shallow --depth 1
        #if result.returncode !=0:
        #    # subprocess failed for some reason
        #    if http_url_to_repo is None:
        #        print(f'Git ssh clone failed, I skip this: {gitrepo_url}')
        #        os.chdir(this_path)
        #        return
        #    else:
        # ro think about to limit checkout files like blob:limit=10M
        result = subprocess.run(['git', 'clone', '--filter=blob:none', http_url_to_repo], check=False)
        if result.returncode != 0:
            print(f'Git https clone failed, I skip this: {http_url_to_repo}')
            os.chdir(this_path)
            return
        # we do a deep clone, through this needs much more space, because the harvester gets the authors from
        # the git history if not found otherwise...
        os.chdir(repo_path)
    else:
        os.chdir(repo_path)
        res = subprocess.run(['git', 'pull'], check=False)
        if res.returncode != 0:
            # subprocess failed for some reason
            print(f'Git pull failed, I skip this: {gitrepo_url}')
            os.chdir(this_path)
            return
    # Alternatively one could have provided config files for the codemeta-harveter and could run also it for all repos at once.
    # but so we have the possibility to to other stuff and also keep the repo of the project.
    subprocess.call(['codemeta-harvester', '--baseuri', repo_url])

    # copy codemeta.py
    results_path = this_path / f'codemeta_results/{gitlab_name}/{repo_name_space}/{reponame}'
    results_path.mkdir(parents=True, exist_ok=True)

    # Be careful here, if the project already had a codemeta.json the harverster will not override it, it will be in harvested.json
    # Be careful to not remove the original code meta. through the harvester already tried to merge these...

    if Path('codemeta.json').exists():
        if copy_codemeta:
            shutil.copy('codemeta.json', f'{results_path}/codemeta.jsonld')
        else:
            shutil.move('codemeta.json', f'{results_path}/codemeta.jsonld')
    else:
        print(f'Something went wrong with: {reponame} no codemeta.json')

    if Path(f'{reponame}.codemeta.json').exists():
        if copy_codemeta:
            shutil.copy(f'{reponame}.codemeta.json', f'{results_path}/codemeta_harvested.jsonld')
        else:
            shutil.move(f'{reponame}.codemeta.json', f'{results_path}/codemeta_harvested.jsonld')
    else:
        print(f'No {reponame}.codemeta.json found.')

    # create unhide data, but we also key codemeta.jsonld for now
    if unhidedata and Path(f'{results_path}/codemeta.jsonld').exists():
        metadata = derive_metadata()
        metadata['harvester_class'] = 'GitlabHarvester'
        metadata['source_pid'] = reponame
        metadata['git_url'] = gitrepo_url

        with open(f'{results_path}/codemeta.jsonld', 'r', encoding='utf-8') as fileo:
            jsonld_md = json.load(fileo)
        ldo = LinkedDataObject(original=jsonld_md, derived=jsonld_md, patch_stack=[], metadata=metadata)
        ldo.serialize(destination=Path(f'{results_path}/codemeta_unhide.json'))

    os.chdir(this_path)  # my be not relative but absolute to be sure...


def harvest_hgf_gitlabs(
    name: str, base_savepath: Optional[Path] = None, gitlabs_meta: dict = load_gitlabs_meta()
) -> None:
    """Clone all projects for a given HGF center and harvest codemeta.jsons"""

    for entry in gitlabs_meta[name]:
        base_link = entry['url']
        git_name = entry['name']
        if base_savepath is None:
            savepath = Path(
                '.'
            ) / f'gitlab_project_jsons/{git_name}'  #os.path.abspath(f'./gitlab_project_jsons/{git_name}')
        else:
            savepath = base_savepath / f'gitlab_project_jsons/{git_name}'
        project_files = []
        for files in savepath.glob('**/*.json'):
            if 'header' not in str(files):
                project_files.append(files)

        #print(project_files)
        for projects_json_file in project_files:
            harvest_fullgitlab(projects_json_file, gitlab_name=git_name, base_savepath=base_savepath)


def request_gitlab_projects(
    name: str,
    base_savepath: Optional[Path] = Path('.'),
    gitlabs_meta=load_gitlabs_meta(),
    since: Optional[datetime] = None
) -> None:
    """Get all projects from API for a given HGF center"""

    if base_savepath is None:
        base_savepath = Path('.')

    for entry in gitlabs_meta[name]:
        base_link = entry['url']
        git_name = entry['name']
        base_savepath_p = base_savepath / f'gitlab_project_jsons/{git_name}'
        # fixme: build since into the gitlab API request, to get only projects updated since
        # there is a key last_activity_after https://docs.gitlab.com/ee/api/projects.html
        if since is not None:  # ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
            since_f = since.isoformat()
            link = f'{base_link}/api/v4/projects?pagination=keyset&non_archived=true&last_activity_after={since_f}&page=1&sort=desc&order_by=id&visibility_level=20&per_page=100'
        else:
            link = f'{base_link}/api/v4/projects?pagination=keyset&non_archived=true&page=1&sort=desc&order_by=id&visibility_level=20&per_page=100'

        os.makedirs(base_savepath_p, exist_ok=True)

        projects_json_file = base_savepath_p / f'{git_name}_projects_headers.json'

        headers, results_files = walk_gitlab(start_link=link, destination_folder=base_savepath_p, gitlab_name=git_name)

        with open(projects_json_file, 'w', encoding='utf-8') as fileo:
            for header in headers:
                fileo.write(str(header))

        projects_json_file1 = results_files[0]
        with open(projects_json_file1, 'r', encoding='utf-8') as fileo:
            projects_json = json.load(fileo)

        #print(f'NProjects: {len(projects_json)}')

        #for project in projects_json:
        #    print(project['name'])


class GitHarvester(Harvester):
    """This is the Harvester for git repositories from gitlabs and github.

    It relies on codemetapy and codemeta-harvester
    """
    def __init__(self, outpath=Path('.'), **kwargs):
        super().__init__(outpath=outpath.resolve(), **kwargs)

    def get_gitlabs(self):
        return self.sources

    def run(
        self,
        hgf_name: str = 'all',
        base_savepath: Optional[Path] = None,
        use_threading: bool = False,
        since: Optional[datetime] = None,
        **kwargs
    ) -> None:
        """Execute the harvester for a certain HGF center"""

        if since is None:
            since = self.last_run

        if base_savepath is None:
            base_savepath = self.outpath

        gitlabs_r = self.get_gitlabs()
        if hgf_name == 'all':
            threads: List[threading.Thread] = []
            for center, val in gitlabs_r.items():
                request_gitlab_projects(center, base_savepath=base_savepath, gitlabs_meta=gitlabs_r, since=since)
                if use_threading:
                    # for now one thread per center
                    thread = threading.Thread(
                        target=harvest_hgf_gitlabs,
                        kwargs={
                            'name': center,
                            'base_savepath': base_savepath,
                            'gitlabs_meta': gitlabs_r
                        }
                    )
                    threads.append(thread)
                    thread.start()
                    #time.sleep(10) # otherwise there is some io problem...
                else:
                    harvest_hgf_gitlabs(center, base_savepath=base_savepath)

            for thread in threads:
                thread.join()
        else:
            request_gitlab_projects(hgf_name, base_savepath=base_savepath, gitlabs_meta=gitlabs_r, since=since)
            harvest_hgf_gitlabs(hgf_name, base_savepath=base_savepath, gitlabs_meta=gitlabs_r)


'''
if __name__ == "__main__":  # pragma: no cover
    if hgf_name == 'ALL':
        threads = []
        for center, val in gitlabs.items():
            if use_threading:
                # for now one thread per center
                thread = threading.Thread(target=harvest_hgf_gitlabs, kwargs={'name':center})
                threads.append(thread)
                thread.start()
                #time.sleep(10) # otherwise there is some io problem...
            else:
                harvest_hgf_gitlabs(center)

        for threads in threads:
            thread.join()
    else:
        harvest_hgf_gitlabs(hgf_name)
'''
