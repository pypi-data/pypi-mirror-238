# StarlinkEphemeris

This module allows you to download and parse Starlink ephemeris files.

## Setup

Simply add this module via `pip`

```
pip install starlink_files
```

## Using

You can:

- Download any available public files from SpaceTrack
- Parse Starlink ephemeris

### Downloading public files

### Downloading public files from SpaceTrack

Script below retrieves all public files and downloads them.

```py
import os
from spacetrack_files.api import SpaceTrackApi

api = SpaceTrackApi('your_username', 'your_password')
dirs = api.getDirsList()

base_download_path = '.'

for download_path in dirs:
    if not os.path.exists(download_path):
        os.mkdir(download_path)

    fs = api.getDirsWithFiles()
    downloading_files = fs[download_path]

    for file in downloading_files:
        file_download_path = os.path.join(base_download_path, download_path, file)
        if os.path.exists(file_download_path):
            continue
        api.downloadFile(file, file_download_path)
```

### Parsing Starlink ephemeris

It's as simple as this:

```py
from spacetrack_files.files import EphemerisFile

# DO NOT RENAME FILE
eph = EphemerisFile('MEME_54190_STARLINK-5281_2210828_Operational_1375864140_UNCLASSIFIED.txt') 
```

Keep in mind: module's using filename to parse satellite name, NORAD ID, classification and operational status. **Thus do not rename file**.

Ephemeris structure:

```py
@dataclass
class Ephemeris:
    epoch_j2000: str
    epoch: datetime
    position: np.array
    speed: np.array
    corr_values: np.array
```

Variables `position` and `speed` are 3-dim vectors. `corr_values` is matrix 3x7.

You can also get ephemeris in DataFrame format:

```py
df = eph.to_dataframe()
```