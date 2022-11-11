# leeds-2023

> Data processing and microsite for Leeds 2023

[![data-puller](https://github.com/open-innovations/leeds-2023/actions/workflows/data-puller.yml/badge.svg)](https://github.com/open-innovations/leeds-2023/actions/workflows/data-puller.yml)
[![publish-on-github-pages](https://github.com/open-innovations/leeds-2023/actions/workflows/deploy-site.yml/badge.svg)](https://github.com/open-innovations/leeds-2023/actions/workflows/deploy-site.yml)
[![pages-build-deployment](https://github.com/open-innovations/leeds-2023/actions/workflows/pages/pages-build-deployment/badge.svg?branch=gh-pages)](https://github.com/open-innovations/leeds-2023/actions/workflows/pages/pages-build-deployment)

## Scripts

The repo contains a series of pipelines which are used to collect and process data.

If you are running the python scripts, you will need to install the dependencies listed in `requirements.txt`.
You will also need to set `PYTHONPATH` in your environment to include `scripts`. On a mac, this can be acheived
with the following command: `export PYTHONPATH=scripts`. Without that, the scripts will not run, and will throw
an error similar to this:

```
ModuleNotFoundError: No module named 'metrics'
```

## Pipelines

Some of the scripts and data are managed in a [DVC](https://dvc.org/) pipeline.
DVC has been added to the `requirements.txt` file, so ensure that your python
environment has the required dependencies installed. This could be as simple as
running `pip3 install -r requirements.txt`. It's recommended to use a virtual
environment tool such as `virtualenv` to avoid clashing requirements.

The repo uses data held in AWS S3 buckets. To access this, make sure
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are set for your environment.

Here are some useful DVC commands:

* Check the DVC status by running `dvc status`.
* To pull the latest data run `dvc pull`.
* You can run all pipelines with `dvc repro -P`. If no stage dependencies (input
  files or code) have changed, nothing will be executed.
* To list the available pipeline stages run `dvc stage list --all`. You can see the
  dependency graph with `dvc dag`
* You can force a stage to re-run using `dvc repro --force <stage name>`.
