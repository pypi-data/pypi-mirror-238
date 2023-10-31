"""TO-WRITE"""

from sklearn.decomposition import PCA
from .spheric import Spheric


class SPCA(PCA):
    """
    TO-WRITE
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def normalize(self, X):
        if len(X.shape) == 0
        return X / np.linalg.norm(X, axis=1)[:, None]
    
    def fit(self, X, y=None):
        X = self.normalize(X)
        X = Spheric.toSpheric(X).phi
        super().fit(X, y)

    def fit_transform(self, X, y=None):
        X = self.normalize(X)
        X = Spheric.toSpheric(X).phi
        return super().fit_transform(X, y)