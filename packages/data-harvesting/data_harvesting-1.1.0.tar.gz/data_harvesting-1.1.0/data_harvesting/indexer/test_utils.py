# -*- coding: utf-8 -*-
"""Old test utlitiy modul"""
# pylint: skip-file
import hashlib
import json
import os
from functools import partial
from functools import wraps
from pathlib import Path

# Set this to true and where ever the decorator is applied it will store the
# input and results files in folders
GENERATE_TESTS = False
BASE_DIR = Path(__file__).resolve().parent.parent / 'tests'


def test_generation(func=None, post=None):
    def dictize(x):
        if isinstance(x, list):
            return [elt.as_dict for elt in x]
        else:
            return x.as_dict

    if not post:
        post = dictize

    if func is None:
        return partial(test_generation, post=post)

    @wraps(func)
    def inner(*args):
        result = func(*args)

        if not GENERATE_TESTS:
            return result

        _type, data = tuple(args)[1:3]

        _type = _type.replace(':', '__')  # windows machines don't like colons in filenames

        print(f'Generating test {_type}')
        src = json.dumps(data)
        base_path = BASE_DIR / 'generated_test' / _type
        sdir = base_path / 'src'
        dest_dir = base_path / 'dest'
        if not base_path.exists():
            base_path.mkdir(parents=True)
            sdir.mkdir()
            dest_dir.mkdir()

        print(f'Generating test {_type} under ')

        file_hash = hashlib.md5(src.encode('utf-8')).hexdigest()[:10]
        with (sdir / (f'{file_hash}.json')).open('w') as f:
            f.write(src)  # what not use json here?

        with (dest_dir / (f'{file_hash}.json')).open('w') as f:
            json.dump(post(result), f)

        print(f'Generated test {file_hash} for {_type} under {base_path}')

        return result

    return inner
