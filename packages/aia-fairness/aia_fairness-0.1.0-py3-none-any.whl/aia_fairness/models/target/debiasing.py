import numpy as np
import silence_tensorflow.auto
from fairlearn.adversarial import AdversarialFairnessClassifier 
from fairlearn.adversarial import AdversarialFairnessRegressor 
import tensorflow as tf

# Générer des données tabulaires de démonstration
# Remplacez cela par vos propres données
class predictor:
    def __init__(self, num_features):
        # Création du modèle de réseau de neurones
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(num_features,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Compilation du modèle
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        

    def fit(self, x,y):

        # Entraînement du modèle
        self.model.fit(x, y, epochs=5, batch_size=100)

    def predict_proba(self, x):
        return self.model.predict(x)

    def predict(self, x):
        return (self.predict_proba(x)>0.5).astype(int).reshape(-1)



class adversary:
    def __init__(self):
        # Création du modèle de réseau de neurones
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(1,)),
            tf.keras.layers.Dense(1, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Compilation du modèle
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


    def set_sizes(self, sizes):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(1,)),
            tf.keras.layers.Dense(1, activation='relu'),
            tf.keras.layers.Dense(sizes[0], activation='relu'),
            tf.keras.layers.Dense(sizes[1], activation='relu'),
            tf.keras.layers.Dense(sizes[2], activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        # Compilation du modèle
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])



    def fit(self, x,y):

        # Entraînement du modèle
        self.model.fit(x,y, epochs=10, batch_size=32)

    def predict_proba(self, x):
        return self.model.predict(x)

    def predict(self, x):
        return (self.predict_proba(x)>0.5).astype(int).reshape(-1)

class debiasing:
    def __init__(self, num_feature):
        self.predictor = predictor(num_feature)
        self.adversary = adversary()
        self.model = AdversarialFairnessRegressor(predictor_model=self.predictor.model, adversary_model=self.adversary.model)

    def fit(self, x, y, z):
        n = np.shape(y)[0]
        u =np.random.normal(0,00.1,n)
        self.model.fit(x, y+u, sensitive_features=z)

    def predict_proba(self,x):
        return self.model.predict(x)

    def predict(self, x):
        return (self.predict_proba(x)>0.5).astype(int).reshape(-1)

