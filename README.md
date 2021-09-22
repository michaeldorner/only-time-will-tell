# Only Time Will Tell: Replication package

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/michaeldorner/only-time-will-tell/CI)](https://github.com/michaeldorner/only-time-will-tell/actions)
[![Codecov](https://img.shields.io/codecov/c/github/michaeldorner/only-time-will-tell)](https://app.codecov.io/gh/michaeldorner/only-time-will-tell)
[![Codacy grade](https://img.shields.io/codacy/grade/bc4bb89d16074ad981365c00e6a8ed5c)](https://app.codacy.com/gh/michaeldorner/only-time-will-tell/dashboard)
[![GitHub](https://img.shields.io/github/license/michaeldorner/only-time-will-tell)](./LICENSE)

The simulation code for the publication "Only Time Will Tell: Only Time Will Tell: Modelling Communication for Information Diffusion in Software Engineering"

## Prerequisites

We recommend at least 50 GB storage and 16 GB RAM recommended. On a server with AMD EPYC 7302P 16 core, 256 GB RAM, and SSD, the simulation takes about ten hours. 
We require Python 3.7 or higher. Install all dependencies via `pip3 install -r requirements.txt`

## Simulation

1. Download or pull this repository
2. `cd only-time-will-tell` (or the directory it is stored)
3. `python3 -m simulation` to run the simulation. With the optional `--time_ignoring_only` and `--time_respecting_only` you can run the simulation with the time-ignoring model or time-respecting model, respectively.

## Tests

`python3 -m unittest discover` runs all tests. 
