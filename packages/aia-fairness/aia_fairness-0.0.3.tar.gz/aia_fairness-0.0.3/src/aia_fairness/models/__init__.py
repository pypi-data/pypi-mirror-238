import numpy as np

class BaseClassifier:
    """Base classifier to be used as a model for all target and attack.
    In our usecase all prediction and sensitive attributes are binary"""
    def __init__(self):
        #Set to True if the classifier needs
        #The sensitive attribute for training
        #It is typically the case for fairness 
        #Enforcing mechanisms 
        self.need_z = False

    def fit(self, x, y):
        pass

    def predict_proba(self, x):
        unif = np.random.uniform(0,1,np.shape(x)[0])
        return unif

    def predict(self, x):
        p = self.predict_proba(x)
        return p<0.5




