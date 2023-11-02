from pathlib import Path
import pickle

from .main import *

def fetch():
    """Downloads and preprocess data"""
    load_utk()
    load_meps()
    load_compas()
    load_census()
    load_law()

def load_format(dset, attrib):
    """Loads a pre-processed dataset
    dset (string) : name of the dataset 
    attrib (string) : attribut "race" or "sex"
    """

    with open(Path("data_format",f"{dset}.pickle"), "rb") as f:
        d = pickle.load(f)
    e = {}
    e["x"] = d["x"]
    e["y"] = d["y"]
    e["z"] = d[f"z{attrib}"]
    return e

def split(data,k=0):
    """5-folding of preprocessed dataset.
    The format is specified in the load_format function
    data (dictionary) : output of load_format
    k (int) : indice of the fold, can be 0,1,2,3 or 4
    """
    keys = list(data.keys())
    n = np.shape(data[keys[0]])[0]
    idx = np.linspace(0,n-1,n).astype(int)
    test = (idx[int(k*0.2*(n))]<=idx)&(idx<=idx[int((k+1)*0.2*(n-1))])
    train = ~test
    data_split = {"train":{},"test":{}}
    for key in keys:
        data_split["train"][key] = data[key][train]
        data_split["test"][key] = data[key][test]

    return data_split
