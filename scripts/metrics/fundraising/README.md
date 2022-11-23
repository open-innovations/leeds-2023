# Fundraising data processing

## Extract from Good CRM

The fundraising export is defined in a System Segment called
`data_organisation_fundraising`. It uses the following criteria:

* `Organisation Type` `Has any of` `Fundraising`

Here is how to extract it.

1) Sign in to Good CRM https://lct.goodcrm.co.uk
2) Navigate to [Profile Icon] -> Tools and Settings -> Queries, then select the
   System Segments tab https://lct.goodcrm.co.uk/queries/index/1
3) Select Export button on the the data_organisation_fundraising segment.
4) Find the file that was downloaded and rename as
   `data_organisation_fundraising.csv`
5) Navigate to files.open-innovations.org and sign in, wither with the general
   `leeds2023` account, or with the leeds2023/fundraising`.
6) If you see a `fundraising` folder navigate into it.
7) Upload the csv file into that folder, overwriting the previous file.

## Adding to the repo

Assuming that you have a valid `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
set in your shell, the file can be added to the repo by issueing the following
command from the workspace root.

```
dvc import-url s3://open-innovations-data/filestash/leeds2023/fundraising/data_organisation_fundraising.csv working/fundraising
```

This can be updated with the command

```
dvc update --recursive working/fundraising/
```

## Running the scripts:

There are two 