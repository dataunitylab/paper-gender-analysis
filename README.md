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

The downloaded files can be analyzed by running the following command:

    pipenv run python analyze_genders.py

This will print a CSV file with inferred counts of first authors by gender.
You can also use [this notebook](cs-paper-gender-analysis.ipynb) for further analysis.

## Adding a new conference

To add a new conference, simply edit [`fetch-papers.py`](fetch-papers.py) to retrieve new JSON data files.
The files should be named `CONF-xx.json` where `CONF` is the name of the conference and `xx` is the year.
The link to the JSON files can be obtained by looking at the table of contents for the proceedings in DBLP and selecting the JSON export link.
Since data coming from DBLP is CC0 and can be freely shared, any new data files should be committed to this repository.
