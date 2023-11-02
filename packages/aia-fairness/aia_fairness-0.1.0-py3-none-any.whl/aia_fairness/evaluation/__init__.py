from pathlib import Path
import numpy as np
import os
import pickle

class utility:
    def __init__(self):
        self.balanced_accuracy = []
        self.accuracy = []
    
    def add_result(self, y, yhat):

        accuracies = [np.mean(yhat[y==yy]==yy) for yy in np.unique(y)]
        self.balanced_accuracy += [np.mean(accuracies)]
        self.accuracy += [np.mean(yhat==y)]

    def save(self, target, dset, attrib):
        os.makedirs(Path("result",target, "utility",dset, attrib), exist_ok=True)
        with open(Path("result",target,"utility",dset,attrib,"balanced_accuracy.pickle"), "wb") as f:
            pickle.dump(self.balanced_accuracy, f)
        with open(Path("result",target,"utility",dset,attrib,"accuracy.pickle"), "wb") as f:
            pickle.dump(self.balanced_accuracy, f)

class attack(utility):
    def __init__(self, attack_type):
        super().__init__()
        self.attack_type = attack_type
    
    def save(self,target,dset,attrib):
        attack_type = self.attack_type
        os.makedirs(Path("result",target, "attack",attack_type,dset, attrib), exist_ok=True)
        with open(Path("result",target,"attack",attack_type,dset,attrib,"balanced_accuracy.pickle"), "wb") as f:
            pickle.dump(self.balanced_accuracy, f)
        with open(Path("result",target,"attack",attack_type,dset,attrib,"accuracy.pickle"), "wb") as f:
            pickle.dump(self.balanced_accuracy, f)

class fairness:
    def __init__(self):
        self.dp_lvl = []

    def add_result(self, y, yhat, z):
        p0 = np.mean(yhat[z==0]==1)
        p1 = np.mean(yhat[z==1]==1)
        self.dp_lvl += [np.abs(p0-p1)]

    def save(self, target,dset,attrib):
        os.makedirs(Path("result",target,"fairness",dset,attrib), exist_ok=True)
        with open(Path("result",target,"fairness",dset,attrib,"dp_lvl.pickle"), "wb") as f:
            pickle.dump(self.dp_lvl, f)
