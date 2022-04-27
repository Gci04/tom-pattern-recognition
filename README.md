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
1. Navigate to `src` then train and test the model by running train and test scripts : `python main.py`.

## Repository directory layout


    .
    ├── Data                    # datasets directory
    │   ├── Repositories.csv    # ..
    │   ├── sample_data.zip     # ..
    │   └── README.md           # Dataset info
    ├── Notebooks               # Jupyter notebooks with examples and EDA
    │   ├── TOM_SUMPY.ipynb     # Training Dataset folder
    │   └── README.md           # Notebooks info
    ├── src                     # Implementation directory
    │   ├── main.py             # file with main implementation
    │   └──utils.py             # Main file for utils      
    ├── requirements.txt
    └── README.md

## Contributions
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or improve.

## Contact
If you would like to get in touch, please contact: <br/>
Gcinizwe Dlamini - g.dlamini@innopolis.university
