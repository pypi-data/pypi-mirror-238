from pathlib import Path
import os

class Metric:
    """Base class for metric
    opens pickel file"""
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path,'rb') as f:
            out = pickle.load(f)
        return out

class BaseEval:
    def __init__(self, path):
        self.path = path

    def list_metrics(self):
        metric_name = os.listdir(self.path)

def get_result_list():
    lst = {}
    targets  = os.listdir(Path("result"))
    for target in targets:
        evaltypes = os.listdir(Path("result",target))
        lst[target] = evaltypes
        for evaltype in evaltypes :
            print(os.listdir(Path("result",target,evaltype)))


        #lst[target] = os.


