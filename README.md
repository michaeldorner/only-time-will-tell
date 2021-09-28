# Only Time Will Tell: Replication package

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/michaeldorner/only-time-will-tell/CI)](https://github.com/michaeldorner/only-time-will-tell/actions)
[![Codecov](https://img.shields.io/codecov/c/github/michaeldorner/only-time-will-tell)](https://app.codecov.io/gh/michaeldorner/only-time-will-tell)
[![Codacy grade](https://img.shields.io/codacy/grade/bc4bb89d16074ad981365c00e6a8ed5c)](https://app.codacy.com/gh/michaeldorner/only-time-will-tell/dashboard)
[![GitHub](https://img.shields.io/github/license/michaeldorner/only-time-will-tell)](./LICENSE)

The simulation code for the publication "Only Time Will Tell: Only Time Will Tell: Modelling Communication for Information Diffusion in Software Engineering"


## Data

Our results can be found on Zenodo. 


## Prerequisites

We recommend at least 50 GB storage and 16 GB RAM. On a server with AMD EPYC 7302P 16 core, 256 GB RAM, and SSD, the simulation takes about ten hours. 
We require Python 3.7 or higher. Install all dependencies via ```pip3 install -r requirements.txt```. 


## Simulation

1. Download or pull this repository
2. `cd only-time-will-tell` (or the directory it is stored)
3. `python3 -m simulation` to run the simulation. With the optional ```--time_ignoring_only``` and ```--time_respecting_only``` you can run the simulation with the time-ignoring model or time-respecting model, respectively.


## Tests and verification

`python3 -m unittest discover` runs all tests. 

The outputs are reproducable and hashable: Verify the files by using hashes such as `sha256sum`.


## Design decisions

All compuations and simulations are execuatable Python scripts. This allows us to test the code properly. Only the visualization is a jupyter notebook and not tested. 

We use JSON to store the results of our simulation despite its limitation (i.e., no native time or set type) because it is widely adopted and allows dictionary-like data (in contrast to table-like data formats such as HDF5 or Apache Arrow). Python's internal serialization module `pickle` was rejected due to its inherent security issues and bad performance. 

## Code snippetts

### Load horizon

```
import json
prefix = 'time_ignoring' # or 'time_respecting' 

with open(prefix + '_horizons.json', 'r') as f:
    data = json.load(f)
```

### Store the horizon to cardinality

```
import json
prefix = 'time_ignoring' # or 'time_respecting' 

with open(prefix + '_horizons.json', 'r') as f:
    data = json.load(f)
  
with open(prefix + '_horizon_cardinalities.json', 'w') as f:
    json.dump({k: len(data[k]) for k in data}, f)
```

