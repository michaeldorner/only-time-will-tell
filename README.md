# Only Time Will Tell: Replication package

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/michaeldorner/only-time-will-tell/CI)](https://github.com/michaeldorner/only-time-will-tell/actions)
[![Codecov](https://img.shields.io/codecov/c/github/michaeldorner/only-time-will-tell)](https://app.codecov.io/gh/michaeldorner/only-time-will-tell)
[![Codacy grade](https://img.shields.io/codacy/grade/bc4bb89d16074ad981365c00e6a8ed5c)](https://app.codacy.com/gh/michaeldorner/only-time-will-tell/dashboard)
[![GitHub](https://img.shields.io/github/license/michaeldorner/only-time-will-tell)](./LICENSE)
[![GitHub](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.5568875-brightgreen)](https://zenodo.org/record/5568875)

Simulation code for the publication "Only Time Will Tell: Modelling Information Diffusion in Code Review With Time-Varying Hypergraphs"


## Data

The results of the simulation can be found on [Zenodo](https://zenodo.org/deposit/5568875). 


## Prerequisites

We recommend at least 50 GB storage, 16 GB RAM, and a powerful CPU for running the entire simulation (for options, see next section). We require Python 3.9 or higher since we heavily rely on [```functools.cache```](https://docs.python.org/3/library/functools.html#functools.cache) to improve the computational performance and which is not available in earlier versions. Install all dependencies via ```pip3 install -r requirements.txt```. 

If you want to create or change the plots, please install and use `jupyter`.


## Run simulation

1. Download or pull this repository
2. `cd only-time-will-tell` (or the directory it is stored)
3. run `pip3 install -r requirements.txt`
4. `python3 -m simulation` to run the simulation. With the optional ```--time_ignoring_only``` and ```--time_respecting_only``` you can run the simulation with the time-ignoring model or time-respecting model, respectively.

Although highly hardware-dependent, please plan for the simulation run with ```--time_ignoring_only``` 10-20 minutes and with ```--time_respecting_only``` 2-8 hours. The option ```--skip_storing_reachables``` saves you about 50 GB of data and about 10-20 minutes of the time. 


## Tests and verification

`python3 -m unittest discover` runs all tests. 

The outputs are reproducible and hashable: Verify the files using hashes such as SHA256. The plots can be reproduced by the jupyter notebook in the folder `notebooks`. 

To verify the results, run

```
shasum -a 256 results/*.json                      
```
and compare the hash values of our results:

```
d455f1e37237014830fa9aaca76232594c92c193c241b71ca28ec69969163daf  results/time_ignoring_reachables.json
4a6b2e596f24a3f00784851789cc0244f3688c1a01316e0aef96b0b7add233a3  results/time_ignoring_upper_bound.json
be3c8358754cfa4cf04137b941b280ac587770fd6c70c6383b78a0e196e5a63b  results/time_respecting_reachables.json
8f77979c99935f6b992f8e2f732af55d06ddcdf2b02cc1d22acc49933675c0a9  results/time_respecting_upper_bound.json
```


## Design decisions

All computations and simulations are executable Python scripts that allow testing the code thoroughly and running it quickly via the command line. Only the visualization is a jupyter notebook and not covered by our test setup.

We use JSON to store our simulation results despite its limitation (i.e., no native time or set type) because it is widely adopted and allows dictionary-like data (in contrast to table-like data formats such as HDF5 or Apache Arrow). We decide against Python's internal serialization module pickle due to its inherent security issues and lousy performance. Since JSON does not support sets, we used JSON objects mapping to none for time-ignoring horizons and to strings representing the timestamp in ISO format for time-respecting horizons.

To improve performance, we heavily rely on caching via [```functools.cache```](https://docs.python.org/3/library/functools.html#functools.cache). This makes the data structures (```CommunicationNetwork``` and ```Hypergraph```) very efficient without boilerplate code but not modifiable after creation. 
