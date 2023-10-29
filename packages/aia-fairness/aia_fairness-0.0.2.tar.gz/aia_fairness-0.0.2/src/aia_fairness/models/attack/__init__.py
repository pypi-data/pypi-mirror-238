import copy
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from .. import BaseClassifier

class Regression(BaseClassifier):
    def __init__(self):
        self.model = RandomForestClassifier()
        self.t = 0.5

    def fit(self, x,y):

        self.model.fit(x.reshape(-1,1),y)

        #meilleur seuil pour la B.A.
        t =np.linspace(0,1,100)
        prob = self.model.predict_proba(x.reshape(-1,1))[:,0]
        probas = np.unique(prob)
        #roc
        d = []
        P = np.sum(y==1)
        N = np.sum(y==0)
        for ti in t:
            p = (prob<=ti).astype(int)

            TP = np.sum((p==1)&(y==1))
            TPR = TP/P

            FP = np.sum((p==1)&(y==0))
            FPR = FP/N

            d += [(1-TPR)**2+FPR**2]

        self.t = t[np.argmin(d)]

    def predict_proba(self, x):
        self.model.predict_proba(x.reshape(-1,1))[:,0]

    def predict(self, x):
        p = self.model.predict_proba(x.reshape(-1,1))[:,0]
        return (p<=self.t).astype(int)

class Classification:
    def __init__(self):
        self.clas = [0,1]
    
    def fit(self, x,y):
        n = np.shape(y)[0]
        yhat = np.zeros(n).astype(int)
        classes= [[0,0],[1,0],[0,1],[1,1]]
        ba = []
        for clas in classes:
            yhat[x==clas[0]]==0
            yhat[x==clas[1]]==1
            ba += [np.mean([np.mean(yhat==yy) for yy in np.unique(y)])]
        i = np.argmax(ba)
        self.clas = classes[i]

    def predict(self,x):
        n = np.shape(x)[0]
        yhat = np.zeros(n).astype(int)
        yhat[x==self.clas[0]]=0
        yhat[x==self.clas[1]]=1
        return yhat
