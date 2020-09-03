# CS Conference Gender Analysis

## Overview

This repository attempts to analyze the gender of first authors of papers at various conferences.
There are several caveats here.
Inferring gender based on name is never exact and the accuracy of this method has not been tested at all so any results should be considered suspect.
Aside from manually labelling the gender of each author (also a difficult and potentially error-prone task), there are several approaches that could improve the accuracy of this method.
For example, attempting to fetch the country of the author's affiliation could provide a more accurate prediction.

## Dependencies

We make use of the [genderComputer](https://github.com/tue-mdse/genderComputer) library for gender inference which is installed as a submodule.
Therefore it is necessary to run `git submodule update --init` to fetch submodules in this repository.
We also make use of [Pipenv](https://pipenv.pypa.io/) to manage dependencies, so this must be installed first as well.
To install other dependencies, run `pipenv install`.


## Running

First, fetch all the paper data:

    ./fetch-papers.sh

This will create a `data/` directory populated with JSON files fetched from DBLP.
Next, analyze the downloaded files:

    pipenv run python analyze_genders.py

This will print the inferred counts of first authors by gender.
