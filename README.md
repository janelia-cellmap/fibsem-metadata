# ⚠️ DEPRECATION NOTICE ⚠️

This repo is no longer used, and the metadata contained within might be accurate but is *no longer being updated.* 

We no longer use this repo to store metadata for imagery on OpenOrganelle. 
Instead, we use a postgresql database managed by [supabase](https://supabase.com/). That database can be accessed via the [supabase python client](https://github.com/supabase-community/supabase-py). Contact me ([davis bennett](https://github.com/d-v-b)) directly to get access to the database. Sorry for any inconvenience this may cause.


# Metadata for publicly hosted fibsem datasets

## Motivation

We store large electron microscopy datasets on cloud storage and offer a web site ([openorganelle.janelia.org](https://openorganelle.janelia.org/)) for browsing those datasets. That site uses this github repo to discover which datasets exist, what their metadata is, which volumes are contained within each dataset, etc.

## Metadata model

At a high level, this repository represents a collection of independent datasets, where each dataset contains the following elements: 
- a thumbnail image
- metadata describing the entire dataset.  
- metadata describing the views associated with the dataset
- a collection of metadata describing each source associated with the dataset

This metadata is stored in the `metadata` folder. Here is how this specification is implemented for a single dataset:
```
metadata/jrc_fly-fsb-1
├── metadata.json
├── sources
│   └── fibsem-uint16.json
├── thumbnail.jpg
└── views.json
```

The structures of the different JSON files are defined by python classes:
- [dataset metadata](https://github.com/janelia-cosem/fibsem-metadata/blob/master/src/fibsem_metadata/models/metadata.py)
- [dataset views](https://github.com/janelia-cosem/fibsem-metadata/blob/master/src/fibsem_metadata/models/views.py)
- [sources](https://github.com/janelia-cosem/fibsem-metadata/blob/master/src/fibsem_metadata/models/sources.py)

## Metadata API

Consuming applications (like OpenOrganelle) benefit from minimizing the number of I/O requests needed to discover datasets. This means that ideally all the metadata for a single dataset should be consolidated into a single file. However, editing metadata is much simpler when it is distributed across multiple logically separable files. Thus, this repository contains two representations of the same information: in addition to the write-optimized `metadata` folder described above, there is a read-optiminzed `api` folder that contains consolidated metadata for each dataset, as well as additional metadata to describe the set of all datasets, e.g.: 

```
api/jrc_fly-fsb-1
├── manifest.json
└── thumbnail.jpg
```
OpenOrganelle accesses these files directly from github for each dataset.

Because the `api` directory is derived entirely from the contents of the `metadata` directory, you should not edit the contents of `api` directly. Instead, the `api` directory is created programmatically by the [`generate_endpoints.py`](https://github.com/janelia-cosem/fibsem-metadata/blob/master/src/fibsem_metadata/generate_endpoints.py) script, which is used by a github actions workflow triggered on each commit.


## Adding metadata

To modify, add, or remove metadata, clone this repository, make changes, and submit a pull request. Although the models are defined as python data structures and python is used for data validation, the metadata itself is all JSON, so no coding is needed for simple metadata updates.

## Local development

To develop locally, clone this repository, install the [`poetry`](https://python-poetry.org/) package manager in your python environment, and run `poetry install` in the root of the cloned directory to install dependencies for this project. 
