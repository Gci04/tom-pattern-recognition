# TOM pattern recognition

This repository provides a implementation of an approach of patterns recognition in gihub repositories commits history

## Prerequisites

* stumpy
* Numpy >= 1.13.3
* Matplotlib >= 2.0.2
* plotly

All the libraries can be pip installed

## Getting Started

1. Clone this repo (for help see this [tutorial](https://help.github.com/articles/cloning-a-repository/)).
1. Navigate to repository folder
1. Install dependencies which are specified in requirements.txt. use `pip install -r requirements.txt` or `pip3 install -r requirements.txt`
1. Raw Data is being kept [here](Data) within this repo.
1. Navigate to `src` then generate/find patterns using the command : `python main.py` parsing the appropiate arguments. **Note (this step can be skipped if the patterns are already existing in directory `results`)**
1. The found patterns are saved in `.json` file in the `results` directory
1. To detect found patterns (stored in `.json`) in a new repository : `python detect.py` parsing the appropiate arguments. i.e :
```
python detect.py -metric total_removed total_changed -m 10 -repo ../Data/test_repo.csv
```
1. To test with your own repository, parse the path to the `.csv` file containing the repo commit history. i.e
```
python detect.py -metric total_removed total_changed -m 10 -repo <you repo commit history path>
```


## Repository directory layout


    .
    ├── Data                    # datasets directory
    │   ├── Repositories.csv    # ..
    │   ├── sample_data.zip     # small dataset
    │   ├── tom_sample_data.zip # main datasets for extracting patterns (it contains information about commits, forks, issues, workflow, users and pulls)
    │   └── README.md           # Dataset info
    ├── Notebooks               # Jupyter notebooks with examples and EDA
    │   ├── TOM_SUMPY.ipynb     #
    │   └── README.md           # Notebooks info
    ├── results                 # directory where results are dumped
    ├── src                     # Implementation directory
    │   ├── main.py             # file with main implementation for finding patterns
    │   ├── detect.py           # script for detecting found pattern in a given single repository
    │   └── utils.py            # Main file for utils      
    ├── requirements.txt
    └── README.md

## Contributions
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or improve.

## Contact
If you would like to get in touch, please contact: <br/>
Gcinizwe Dlamini - g.dlamini@innopolis.university
