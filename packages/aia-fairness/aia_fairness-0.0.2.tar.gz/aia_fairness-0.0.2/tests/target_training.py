#In this script we train a target with various models
import numpy as np
from pathlib import Path

import aia_fairness.dataset_processing as dp
import aia_fairness.models.target as targets
import aia_fairness.evaluation as evaluations
import aia_fairness.config as config

dset = "COMPAS"
attrib = "sex"
data = dp.load_format(dset, attrib)

#Initalize the metrics
utility = evaluations.utility()
fairness = evaluations.fairness()

for k in range(config.NN):
    T = dp.split(data, k)
    target = targets.RandomForest()
    target.fit(T["train"]["x"], T["train"]["y"])
    yhat = target.predict(T["test"]["x"])

    #For each cross val set we compute the metrics.
    #Those metrics are stored in the objects utility and fairness
    utility.add_result(T["test"]["y"], yhat, T["test"]["z"])
    fairness.add_result(T["test"]["y"], yhat, T["test"]["z"])

#The save methods creates a directory structure of the form :
#|result
#|  |<name of the metric class>
#|  |   |<dset>
#|  |   |   |<attrib>
#|  |   |   |   <Name of metric 1>.pickle
#|  |   |   |   <Name of metric 2>.pickle
#|  |   |   |   <Name of metric ..>.pickle
#|  |<name of another metric class>
#|  |   |<dset>
#|  |   |   |<attrib>
#|  |   |   |   <Name of another metric 1>.pickle
#|  |   |   |   <Name of another metric 2>.pickle
#|  |   |   |   <Name of another metric ..>.pickle
utility.save(Path(dset,attrib))
fairness.save(Path(dset,attrib))
