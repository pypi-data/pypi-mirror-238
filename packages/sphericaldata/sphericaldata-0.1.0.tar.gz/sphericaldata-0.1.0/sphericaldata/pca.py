"""TO-WRITE"""

import numpy as np
from numpy import ndarray
from sklearn.decomposition import PCA
from .spheric import Spheric


class SPCA(PCA):
    """
    TO-WRITE
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __normalize(self, X):
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
        return X / np.linalg.norm(X, axis=1)[:, None]
    
    def fit(self, X, y=None):
        X = self.__normalize(X)
        print(type(X))
        X = Spheric.toSpheric(X).phi
        super().fit(X, y)

    def fit_transform(self, X, y=None):
        X = self.__normalize(X)
        X = Spheric.toSpheric(X).phi
        return super().fit_transform(X, y)
    
    def transform(self, X) -> ndarray:
        X = self.__normalize(X)
        X = Spheric.toSpheric(X).phi
        return super().transform(X)