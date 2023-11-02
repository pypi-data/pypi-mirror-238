#In this script we show to use aia_fairness to train an attack model 
import aia_fairness.models.attack as attacks
import aia_fairness.experimental_stack as exp

dset = "COMPAS"
attrib = "sex"

yhats = exp.target_training(dset, attrib)
print(yhats)

