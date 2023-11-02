# ReadLIGO

This module provides tools for reading LIGO data files.
Data along with supporting documentation can be downloaded from the [GWOSC web site](https://gwosc.org).

| ! Notice          |
|:------------------|
| This module has been deprecated and we recommend using [GWPy](https://gwpy.github.io) instead. |
| We keep this module public for archival reasons only. No further development is planned.     |


## Installation

To install download the repo and install with pip

```bash
git clone https://git.ligo.org/gwosc/readligo.git; cd readligo
pip install .
```

## Documentation

Some possible use cases are shown below.

### Example 0

To load all data from a single file:

```python
strain, time, dq = rl.loaddata("ligo_data/H-H1_LOSC_4_V1-842653696-4096.hdf5", "H1")
```

Some GWF files require parameters to name the strain, DQ, and hardware injection channel:

```python
strain, time, dq = rl.loaddata(
    "H-H1_LOSC_16_V1-1127415808-4096.gwf",
    "H1",
    strain_chan="H1:GWOSC-16KHZ_R1_STRAIN", 
    dq_chan="H1:GWOSC-16KHZ_R1_DQMASK",
    inj_chan="H1:GWOSC-16KHZ_R1_INJMASK"
)
```

### Example 1

This default configuration assumes that the needed LIGO data files are available in the current working directory or a subdirectory.
LIGO data between the input GPS times are loaded into STRAIN.
META is a dictionary of gps start, gps stop, and the sample time.
DQ is a dictionary of data quality flags.

```python
segList = getsegs(842657792, 842658792, 'H1')
for (start, stop) in segList:
  strain, meta, dq = getstrain(start, stop, 'H1')
  # -- Analysis code here
  ...
```

### Example 2

In Example 2, `H1_segs.txt` is a segment list downloaded from the
GWOSC web site using the [Timeline application](https://gwosc.org/timeline/).  This may be used in the same
manner as `segList` in example 1.

```python
segList = SegmentList("H1_segs.txt")
```

### Example 3

In this example, the first command searches the indicated directory and 
sub-directories for LIGO data files.
This list of data files is then used to construct a segment list and load
the requested data.

```python
filelist = FileList(directory="/home/ligodata")
segList = getsegs(842657792, 842658792, "H1", filelist=filelist)
for start, stop in segList:
  strain, meta, dq = getstrain(start, stop, "H1", filelist=filelist)
  # -- Analysis code here
```

### Segment Lists

Segment lists may be downloaded from the GWOSC web site
using the Timeline Query Form or constructed directly
from the data files.  

Read in a segment list downloaded from the [Timeline application](https://gwosc.org/timeline/)
on the [GWOSC web site](https://gwosc.org) with `SegmentList`.

```python
from readligo import SegmentList
seglist = SegmentList("H1_segs.txt")
```

Or Construct a segment list directly from the LIGO data files with `getsegs`.

```python
from readligo import getsegs
seglist = getsegs(842657792, 842658792, 'H1', flag='DATA', filelist=None)
```
