# Only Time Will Tell: Replication package

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/michaeldorner/only-time-will-tell/CI)](https://github.com/michaeldorner/only-time-will-tell/actions)
[![Codecov](https://img.shields.io/codecov/c/github/michaeldorner/only-time-will-tell)](https://app.codecov.io/gh/michaeldorner/only-time-will-tell)
[![Codacy grade](https://img.shields.io/codacy/grade/bc4bb89d16074ad981365c00e6a8ed5c)](https://app.codacy.com/gh/michaeldorner/only-time-will-tell/dashboard)
[![GitHub](https://img.shields.io/github/license/michaeldorner/only-time-will-tell)](./LICENSE)
[![GitHub](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.5568875-brightgreen)](https://zenodo.org/record/5568875)

The simulation code for the publication "Only Time Will Tell: Modelling Information Diffusion in Code Review With Time-Varying Hypergraphs"


## Data

Our results can be found on [Zenodo](https://zenodo.org/deposit/5568875). 


## Prerequisites

We recommend at least 50 GB storage, minimum 16 GB RAM, and a powerful CPU for the running the full simulation (for options see next section). We require Python 3.8 or higher. Install all dependencies via ```pip3 install -r requirements.txt```. 

If you would like to create or change the plots, please install and use `jupyter`.


## Run simulation

1. Download or pull this repository
2. `cd only-time-will-tell` (or the directory it is stored)
3. run `pip3 install -r requirements.txt`
4. `python3 -m simulation` to run the simulation. With the optional ```--time_ignoring_only``` and ```--time_respecting_only``` you can run the simulation with the time-ignoring model or time-respecting model, respectively.

Although highly hardware-dependent, please plan for the simulation run with ```--time_ignoring_only``` 10-45 minutes and with ```--time_respecting_only``` 8-24 hours. 


## Tests and verification

`python3 -m unittest discover` runs all tests. 

The outputs are reproducible and hashable: Verify the files by using hashes such as SHA256. The plots can be reproduced by the jupyter notebook in the folder `notebooks`. 

To verify the results run

```
shasum -a 256 data/time_*.json                      
```
and compare the hash values of our results:

```
4a6b2e596f24a3f00784851789cc0244f3688c1a01316e0aef96b0b7add233a3 data/time_ignoring_horizon_cardinalities.json
d455f1e37237014830fa9aaca76232594c92c193c241b71ca28ec69969163daf data/time_ignoring_horizons.json
a07356ef7bf8b8af152e95857c39cbb8138c63ad110f455a309083545b94cbb5 data/time_respecting_horizon_cardinalities.json
8722f82d2cb9e1c1947baa3c8ff9239d2faed6deae56469114a364e2c2649832 data/time_respecting_horizons.json
```


## Design decisions

All computations and simulations are executable Python scripts that allow test the code thoroughly and run it quickly via the command line. Only the visualization is a jupyter notebook and not covered by our test setup.

We use JSON to store our simulation results despite its limitation (i.e., no native time or set type) because it is widely adopted and allows dictionary-like data (in contrast to table-like data formats such as HDF5 or Apache Arrow). We decide against Python's internal serialization module pickle due to its inherent security issues and lousy performance. Since JSON does not support sets, we used JSON objects mapping to none for time-ignoring horizons and to strings representing the timestamp in ISO format for time-respecting horizons.


## Code snippets

### Load horizon

```
import json

path = ...
prefix = 'time_ignoring' # or 'time_respecting' 

with open(path + prefix + '_horizons.json', 'r') as f:
    data = json.load(f)
```

The data so far is not typed. We highly recommend to use typed data:

```
import datetime

horizons = {n: {l: datetime.datetime.fromisoformat(data[n][l]) for l in data[n]} for n in tqdm.tqdm(data)}
```
We recommend `tqdm` to show a progress bar. Feel free to replace `tqdm.tqdm(data)` with `data` only otherwise.  

### Store the horizon to cardinality

```
import json

path = ...
prefix = 'time_ignoring' # or 'time_respecting' 

with open(path + prefix + '_horizons.json', 'r') as f:
    data = json.load(f)
  
with open(prefix + '_horizon_cardinalities.json', 'w') as f:
    json.dump({k: len(data[k]) for k in data}, f)
```

