from pathlib import Path
from datetime import datetime

date_file = Path(__file__).parent.joinpath('../docs/_data/timestamp/data.yml')

date_file.parent.mkdir(parents=True, exist_ok=True)

with open(date_file, 'w') as f:
    f.write(datetime.now().isoformat())
