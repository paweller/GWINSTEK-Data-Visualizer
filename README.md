# GWINSTEK-Data-Visualizer

[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

## Overview
Python code to read in and visualize .csv files exported from a GWINSTEK GDS-1072A-U oscilloscope.

## API

```python
parse_data(fds)
plot_data(
    as_captured=True,
    show_metadata=True
)
```

Arguments:
- `fds` *([str])*: A list of strings containing the source .csv files.
- `as_captured` *(bool)*:\
True: Visualize data as shown on the oscilloscope's screen.\
False: Translate measurements to the coordinate system's origin.

## Dependencies

- Numpy
- Matplotlib

## Dummy code example

```python
from GWINSTEK_GDS_1072A_U_CSV_Reader import GWINSTEK_GDS_1072A_U_CSV_Reader

fds = [
    'A0000CH1.CSV',
    'A0000CH2.CSV'
]

reader = GWINSTEK_GDS_1072A_U_CSV_Reader()
reader.parse_data(fds)
reader.plot_data()
```

## Plot example
