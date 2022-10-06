# leeds-2023

> Data processing and microsite for Leeds 2023


## Scripts

The repo contains a series of pipelines which are used to collect and process data.

If you are running the python scripts, you will need to install the dependencies listed in `requirements.txt`.
You will also need to set `PYTHONPATH` in your environment to include `scripts`. On a mac, this can be acheived
with the following command: `export PYTHONPATH=scripts`. Without that, the scripts will not run, and will throw
an error similar to this:

```
ModuleNotFoundError: No module named 'metrics'
```