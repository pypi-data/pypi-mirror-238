#Set the seed for every experiement
random_state = 1234

#Numbre of folding used in cross validation 
#Can be 1,2,3,4 or 5
NN = 1

#Do you want to use only 10 entries for each dataset ? 
#(Usefull to test for new features)
small = True

#Lunch in parallel or not
para = True

#select dataset 
dsets = ["COMPAS", "CENSUS", "LAW", "MEPS", "UTKflat"]

#Select sensitive attribute (they are not used in training, just for mitigation)
attribs = ["race", "sex"]

#Select target model
from ..models import target as targets #Don't touch this line ! 
#Choose which target model you want to use
target_models = [targets.RandomForest,
                 targets.RandomForest_EGD,
                 targets.NeuralNetwork,
                 targets.NeuralNetwork_EGD,
                 targets.NeuralNetwork_Fairgrad,
                 targets.NeuralNetwork_AdversarialDebiasing]
