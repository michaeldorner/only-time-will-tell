# Only Time Will Tell: Replication package

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/michaeldorner/only-time-will-tell/CI)](https://github.com/michaeldorner/only-time-will-tell/actions)
[![Codecov](https://img.shields.io/codecov/c/github/michaeldorner/only-time-will-tell)](https://app.codecov.io/gh/michaeldorner/only-time-will-tell)
[![Codacy grade](https://img.shields.io/codacy/grade/bc4bb89d16074ad981365c00e6a8ed5c)](https://app.codacy.com/gh/michaeldorner/only-time-will-tell/dashboard)
[![GitHub](https://img.shields.io/github/license/michaeldorner/only-time-will-tell)](./LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6542540.svg)](https://doi.org/10.5281/zenodo.6542540)


Simulation code for the publication "Only Time Will Tell: Modelling Information Diffusion in Code Review With Time-Varying Hypergraphs"


## Data
The results of the simulation can be found on [Zenodo](https://doi.org/10.5281/zenodo.6542540). 


## Prerequisites

The simulation requires at least 50 GB storage, 16 GB RAM, a powerful CPU for running the entire simulation (for options, see next section), and Python 3.8 or higher. Install all dependencies via ```pip3 install -r requirements.txt```. We highly recommend 64 GB RAM and Python 3.9 or later. 

If you want to create or change the plots, please install and use `jupyter`.


## Run simulation

1. Download or pull this repository
2. `cd only-time-will-tell` (or the directory it is stored)
3. run `pip3 install -r requirements.txt`
4. `python3 -m simulation` to run the simulation. With the optional ```--time_ignoring_only``` and ```--time_respecting_only``` you can run the simulation with the time-ignoring model or time-respecting model, respectively.

Although highly hardware-dependent, we recommend to plan for the simulation run to take 10-20 min with ```--time_ignoring_only``` and 2-4 hours with ```--time_respecting_only```. The option ```--skip_storing_reachables``` saves you about 50 GB of data on your local drive and about 10-20 minutes of the time but also does not allow you to check those intermediate results. 


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
f8e6472e74819e6ac74c4bb7ae16aac3d75728da0b795448d849951eb4dd3bd6  results/time_respecting_reachables.json
a07356ef7bf8b8af152e95857c39cbb8138c63ad110f455a309083545b94cbb5  results/time_respecting_upper_bound.jsonn
```


## Design decisions

All computations and simulations are packed into a executable Python module that allow testing the code thoroughly and running it quickly via the command line. Only the visualization is a jupyter notebook and not covered by our test setup.

We use JSON to store our simulation results despite its limitation (i.e., no native time or set type) because it is widely adopted and allows dictionary-like data (in contrast to table-like data formats such as HDF5 or Apache Arrow). We decide against Python's internal serialization module pickle due to its inherent security issues and lousy performance. Since JSON does not support sets, we use sorted arrays for the reachables. Writing an adjacency matrix as CSV is a magnitude slower than our approach. 

At the current state, we do not support multiple cores since the whole graph is kept in memory (about 100 GB peak memory footprint) which causes performance issues on Windows and macOS due to their restriction on [COW](https://en.wikipedia.org/wiki/Copy-on-write) and process forking. Please find more information [here](https://bugs.python.org/issue33725) and [here](https://docs.python.org/3.10/library/multiprocessing.html#contexts-and-start-methods). 
