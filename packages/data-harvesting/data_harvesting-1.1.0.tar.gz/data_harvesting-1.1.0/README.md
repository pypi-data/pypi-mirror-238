[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
# Data Harvesting

This repository contains harvesters, aggregators for linked Data and tools around them. 
This software allows to harvest small subgraphs exposed by certain sources on the web and
and enrich them such that they can be combined to a single larger linked data graph. 

This software was written for and is mainly currently deployed as a part of the backend for the unified Helmholtz Information and Data Exchange (unHIDE) project by the Helmholtz Metadata Collaboration (HMC) to create
a knowledge graph for the Helmholtz association which allows to monitor, check, enrich metadata as well as
identify gabs and needs.

Contributions of any kind by you are always welcome!

## Approach:

We establish certain data pipelines of certain data providers with linked metadata and complement it, by combining it with other sources. For the unhide project this data is annotated in schema.org semantics and serialized mainly in JSON-LD.

Data pipelines contain code to execute harvesting from a local to a global level. 
They are exposed through a cmdline interface (cli) and thus easily integrated in a cron job and can therefore be used to stream data on a time interval bases into some data eco system

Data harvester pipelines so far:
- gitlab pipeline: harvest all public projects in Helmholtz gitlab instances and extracts and complements codemeta.jsonld files. (todo: extend to github)
- sitemap pipeline: extract JSON-LD metadata a data provider over its sitemap, which contains links to the data entries and when they have been last updated
- oai pmh pipeline: extract metadata over oai-pmh endpoints from a data provider. it contains a list of entries and when they where last updated. This pipeline uses a converter from dublin core to schema.org, since many providers provide just dublin core so far.
- datacite pipeline: extract JSON-LD metadata from datacite.org connected to a given organization identifier.
- schoolix pipeline (todo): Extract links and related resources for a list of given PIDs of any kind

Besides the harvesters there are aggregators which allow one to specify how linked data should be processed while tracking the provenance of the processing in a reversible way. This is done by storing graph updates, so called patches, for each subgraph. These updates can also be then applied directly to a graph database. Processes changes can be provided as SPARQL updates or through python function with a specific interface.

All harvesters and Aggregators read from a single config file (as example see [configs/config.yaml](https://codebase.helmholtz.cloud/hmc/hmc-public/unhide/data_harvesting/-/blob/dev/data_harvesting/configs/config.yaml)), which contains als sources and specific operations. 

## Documentation:

Currently only in code documentation. In the future under the docs folder and hosted somewhere.

## Installation

```
git clone git@codebase.helmholtz.cloud:hmc/hmc-public/unhide/data_harvesting.git
cd data_harvesting
pip install .
```
as a developer install with
```
pip install -e .
```
You can also setup the project using poetry instead of pip.
```
poetry install --with dev
```

The individual pipelines have further dependencies outside of python.

For example the gitlab pipeline relies an codemeta-harvester (https://github.com/proycon/codemeta-harvester)

## How to use this

For examples look at the `examples` folder. Also the tests in `tests` folder may provide some insight.
Also once installed there is a command line interface (CLI), 'hmc-unhide' for example one can execute the gitlab pipeline via:

```
hmc-unhide harvester run --name gitlab --out ~/work/data/gitlab_pipeline
```

further the cli exposes some other utility on the command line for example to convert linked data files 
into different formats.

## License

The software is distributed under the terms and conditions of the MIT license which is specified in the `LICENSE` file.
## Acknowledgement

This project was supported by the Helmholtz Metadata Collaboration (HMC), an incubator-platform of the Helmholtz Association within the framework of the Information and Data Science strategic initiative.
