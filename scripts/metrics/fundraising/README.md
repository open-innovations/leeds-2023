# Fundraising

## GoodCRM Segments

The segment `data_organisation_fundraising` has been created with the following criteria:

* `Organisation Type` `Has any of` `Fundraising`

Export this file to the `working` directory of this repo. The process is expecting the following files to exist.

* `working/fundraising_orgs.csv`

## Processing the data

To process the data, run the following command (assuming working directory is root of repo):

```
python scripts/metrics/fundraising
```

You can override the input file path by providing this as the first argument.
