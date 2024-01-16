---
title: Site Documentation
description: |
  The Leeds 2023 data microsite site is built by applying data from the LEEDS 2023 operational systems
  to a series of templates to create a static web site.
  This page describes the process by which the site is built.
---

The Leeds 2023 data microsite site is built by applying data from the LEEDS 2023 operational systems
to a series of templates to create a static web site.
This page describes the process by which the site is built.

## Architecture overview

The diagram below shows the main flows in the data preparation and site build pipelines.

![A diagram showing the flows of data from the LEEDS 2023 source systems via a three stage pipeline where data is extracted, then transformed and finally prepared to feed the site build. The site build takes this data and combines with a series of templates, components and other web assets and builds these into a static web site. The site is then deployed to GitHub Pages.](/assets/images/docs/architecture-overview.png)

To the left of the diagram are source systems, comprising a mix of operational and record-keeping systems. Data is either extracted from these automatically (green, solid arrows) or manually (red, dashed arrows). Some intermediary systems are also indicated (Open Innovations SFTP and Open Innovations File Share).

The data pipeline comprises

* an extract stage, which stores its outputs in the
  [the `/working` folder](https://github.com/open-innovations/leeds-2023/tree/main/working).
* a transform stage which targets the 
  [the `/data` folder](https://github.com/open-innovations/leeds-2023/tree/main/data/).
* a prepare stage which converts data to the form required
  for site generation (e.g. to drive visualisations).

Each of thse stages is described in more detail below.

The site is built using the [Lume static site generator software][LUME_LAND], with the site source comprising templates, components and assets.

The resulting static HTML, CSS, JavaScript and assets are then deployed to a GitHub Pages site.

All transformed and prepared data, pipeline and site source code are tracked in
[the Leeds 2023 data GitHub repository][L23_DATA_GITHUB].
Pipelines and site build execution uses GitHub Actions.

## Data extraction

The __extract__ pipeline stages are tasked with extracting data from the source systems
and making it available to downstream __transform__ stages.
The data schema is as close as possible to the source system.
Data is temporarily stored in the GitHub repository in the top-level `/working` folder.

Some datasets require the source systems to provide personally identifiable information
(e.g. postcodes, user IDs).
These are not sanitised until the __transform__ scripts.
The files in the `/working` folder are consequently
not checked in to the repository to avoid leakage of personal data.

There are two basic mechanisms in place:

* Code written in Python / Jupyter, and stored in the `/scripts` folder.
  Generally these will have a name referencing `extract` in some way (e.g `extract.py`).
* Direct references to remote data with a [`dvc import-url`](https://dvc.org/doc/command-reference/import-url)
  / `*.dvc` file. These do not require an associated script.

The extract pipelines are orchestrated using [`dvc`][DVC_ORG], with pipeline defintions being
stored in `dvc.yml` files close to the source code (or associated transform scripts).

## Data transformation

The __transform__ scripts aim to convert the raw data into a sanitised and de-personalised format.
There are a range of techniques at use

* Mapping postcodes to ward codes and local authority codes to geographically 'smear' locations;
* Creating a hashed version of an id code, where this is required to uniquely identify a
  previously extracted record (e.g. volunteer signup data);
* Removing precision from timestamps (e.g. reducing to an hour or day);
* Performing matching of geography names to codes (e.g. ward names to ward codes);
* Cleansing data where there are variant or incorrect spellings of data entries';
* Mapping data to a defined set of desired states (e.g. volunteer status based on checkpoint);

The aim is that any transformed datasets could be released under an open license.

The top-level `data` folder in the GitHub repository contains the transformed files.
The files contained in
[the `/data/metrics` folder](https://github.com/open-innovations/leeds-2023/tree/main/data/metrics)
are listed in [the data catalogue](/catalogue/).
There are also reference files, most of which are manually processed and stored.
These contain, for example, lookups for postcode to ward and local authority.

Where possible, the transformation maintains a similar structure to the raw data.
This avoids losing data granularity in subsequent processing.

Scripts are written in Python / Jupyter, and stored in the `/scripts` folder.
Generally these will have a name referencing `transform` in some way (e.g `transform.ipynb`).
The stages are orchestrated using [`dvc`][DVC_ORG], with pipeline defintions being
stored in `dvc.yml` files close to the source code.

## Data preparation

The _prepare_ stages are responsible for filtering and summarising the data stored in the top-level `/data` directory.
These scripts typically output data into
[an `_data` folder](https://lume.land/docs/creating-pages/shared-data/#the-_data-directories)
in the site source so that they can be made available as build context.

The data is structured in ways appropriate to drive site generation.

Scripts are written in Python / Jupyter, and stored in the `/scripts` folder.
Generally these will have a name referencing `prepare` in some way (e.g `prepare.ipynb`).
The stages are orchestrated using [`dvc`][DVC_ORG], with pipeline defintions being
stored in `dvc.yml` files close to the source code.

## Site build

The site is build using [the Lume static site builder][LUME_LAND].
We make use of Lume components, both defined within [the Leeds 2023 Data GitHub repository][L23_DATA_GITHUB],
and drawn from [the Open Innovations Lume visualisation library][OI_LUME_VIZ].

## Deployment

Once the Lume build has created the static site, the resulting assets are hosted on a GitHub pages site,
hosted using the custom <https://data.leeds2023.co.uk/> subdomain.
This is managed by the owner of the leeds2023.co.uk domain, following instructions contained in [the GitHub documentation on configuring a custom subdomain][GH_PAGES_CUSTOM_SUBDOMAIN]


[LUME_LAND]: https://lume.land/
[L23_DATA_GITHUB]: https://github.com/open-innovations/leeds-2023
[DVC_ORG]: https://dvc.org/
[OI_LUME_VIZ]: https://github.com/open-innovations/oi-lume-viz
[GH_PAGES_CUSTOM_SUBDOMAIN]: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-a-subdomain