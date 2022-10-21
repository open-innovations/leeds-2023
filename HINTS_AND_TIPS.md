# Processing data with [`jq`](https://stedolan.github.io/jq/)

This is useful https://michaelheap.com/extract-keys-using-jq/

## GeoJSON to CSV

```
jq -cr '["WD21CD","WD21NM"],(.hexes | to_entries[] | [ .key, .value.n ]) | @csv' docs/_data/hex/wards_leeds.json
```
