# AIA_fairness

Code repository of the article.
The repositries segments the pipeline as to isolate key componants of the experimental analysis.


## Installation and dependencies
By using pypi :
```pip install aia_fairness```

Or clone the repository then run 
```pip install --editable .```
in the directory containing pyproject.toml

All dependencies are specified in pyproject.toml and installed automatically by pip.
## How to use 
Global configuration parameters can be set by editing ```config.py```

### Dataset automatic download and processing
Part of the dataset uses the kaggle API to download the data.
Hence you need to include your API key in ```~/.kaggle/kaggle.json```.

aia_fairness provides automatic download, formatic and saving of the dataset used in the article. 
To use this feature and thus saving data in the `data_format` directory simply run once 
```python
import aia_fairness.dataset_processing as dp
dp.fetch()
```
Then you can load any dataset easily form anywhere in your code with
```python
import aia_fairness.dataset_processing as dp
data = dp.load_format(dset, attrib)
```
You can refer to the full implementation in `test/target_training.py`.

### Running all the expriments form the paper
** Heavy computing power required **

One you have downloaded all the data you can run all the expirement of the article by running
```bash
python -m aia_fairness.experimental_stack
```
or import `aia_fairness.experimental_stack` in the python interpreter.

### Training a target model
`aia_fairness.models.target` contains various target model type. 
The target models available are :
 - `RandomForest`
 - `RandomForest_EGD` fairlearn is used to impose EGD
 - `NeuralNetwork`
 - `NeuralNetwork_Fairgrad` Original implementation of the fairgrad paper
 - `NeuralNetwork_AdversarialDebiasing` Uses the fairlearn implementation of Adversarial Debisaing 

For instance to train a random forest (based on sklearn) you can
```python
import aia_fairness.models.target as targets
T = dp.split(data,0)
target.fit(T["train"]["x"], T["train"]["y"])
yhat = target.predict(T["test"]["x"])
```
### Evaluation of a target model
`aia_fairness.evaluation` provides the metrics used in the article.
```python
import aia_fairness.evaluation as evaluations
utility = evaluations.utility()
fairness = evaluations.fairness()
utility.add_result(T["test"]["y"], yhat, T["test"]["z"])
fairness.add_result(T["test"]["y"], yhat, T["test"]["z"])
utility.save(type(target).__name__,dset,attrib)
fairness.save(type(target).__name__,dset,attrib)
```
The save method, as called in the example, creates a directory structure of the form :
```
#|result/target/<target type>
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
```

### Training an attack
`aia_fairness.models` provides the two types of AIA attack described in the paper:
 - `Classification` for hard labels
 - `Regression` for soft labels
```python
from aia_fairness.models import attack as attacks
aux = {"y":T["test"]["y"],
       "z":T["test"]["z"],
       "yhat":yhat}
aux_split = dp.split(aux,0)
classif = attacks.Classification()
classif.fit(aux_split["train"]["yhat"], aux_split["train"]["z"])
```

### Evaluation of an attack
Similarly with evaluating the target model `aia_fairness.evaluation.attack` can be used to save the accuracy and the balanced accuracy of the attack.

### Plots and graphs 
TODO

## Tests scripts 
Various tests are provided in the `test` directory.
 - `download_data.py` Fetches all the data form the diferent sources (don't forget to set your kaggle API key)
 - `target_training.py` Loads a dataset, split it with 5-folding (cross validation), train a target model on the data, and computes the metrics for this target model

## Directories structure

- data_processing contains code that downloads, preprocess and saves the dataset in a uniformed pickle format exploitable by the rest of the pipeline using ```load_format(dataset,attribute)``` function of the utils.py file. 
