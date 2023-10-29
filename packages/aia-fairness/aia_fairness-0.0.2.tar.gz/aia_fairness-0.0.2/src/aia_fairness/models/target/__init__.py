import numpy as np
from fairlearn.reductions import DemographicParity 
from fairlearn.reductions import ExponentiatedGradient
from sklearn.ensemble import RandomForestClassifier
from . import fairgrad
from .import debiasing

from .. import BaseClassifier

class RandomForest(BaseClassifier):
    def __init__(self):
        self.model = RandomForestClassifier()

    def fit(self,x,y):
        self.model.fit(x,y)

    def predict_proba(self,x):
        return self.model.predict_proba(x)[:,0]

    def predict(self,x):
        return self.model.predict(x)

class NeuralNetwork(BaseClassifier):
    def __init__(self):
        super().__init__()

    def fit(self,x,y):
        input_size = np.shape(x)[1]
        self.model = fairgrad.target_model(input_size)
        self.model.set_fair(False)
        self.model.fit(x,y)

    def predict_proba(self,x):
        return self.model.predict_proba(x)

    def predict_proba(self,x):
        return self.model.predict(x)

class NeuralNetwork_Fairgrad(NeuralNetwork):
    def __init__(self):
        super().__init__()
        self.need_z = True

    def fit(self,x,y,z):
        input_size = np.shape(x)[1]
        self.model = fairgrad.target_model(input_size)
        self.model.set_fair(True)
        self.model.fit(x,y,z=z)

class NeuralNetwork_AdversarialDebiasing(BaseClassifier):
    def __init__(self):
        super().__init__()
        self.need_z = True

    def fit(self,x,y,z):
        input_size = np.shape(x)[1]
        self.model = debiasing.debiasing(input_size)
        self.model.fit(x,y,z)

    def predict_proba(self,x):
        return self.model.predict(x)

    def predict(self, x):
        return (self.predict_proba(x)>0.5).astype(int).reshape(-1)
        
class RandomForest_EGD(RandomForest):
    def __init__(self):
        super().__init__()
        constraint = DemographicParity()
        self.model = ExponentiatedGradient(self.model, constraint)
        self.need_z = True

    def fit(self,x,y,z):
        target.fit(x,y,sensitive_features=z)

    def predict_proba(self,x):
        return self.model._pmt_predict(x)[:,0]

class Dry1(BaseClassifier):
    def __init__(self):
        super().__init__()

class Dry2(BaseClassifier):
    def __init__(self):
        super().__init__()
        self.need_z = True

    def fit(self, x,y,z):
        pass
