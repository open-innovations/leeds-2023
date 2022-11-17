import pandas as pd
import json

with open('working\\arts_council\\la.json') as f:
    print(pd.DataFrame.from_dict(json.load(f)['hexes'],orient='index'))