"""TO-WRITE"""

import numpy as np


class Spheric:
    def __init__(self, data):
        """
        TO-WRITE
        """
        self.n_dim = data.shape[1]
        self.r = self.__r(data)
        self.phi = self.__phi(data)
        self.data = self.__unite(self.r,
                                 self.phi)

    def __r(self, x):
        return np.linalg.norm(x, axis=1).reshape(-1, 1)

    def __n_phi(self, x, n):
        if n < self.n_dim - 2:
            return np.arctan2(np.linalg.norm(x[:, n + 1:], axis=1), x[:, n])
        elif n == self.n_dim - 2:
            return np.arctan2(x[:, -1], x[:, n])
        else:
          raise IndexError("Too many angles for this sample")


    def __phi(self, data):
        return np.array([self.__n_phi(data, n) for n in range(self.n_dim - 1)]).T
    
    def __unite(self, r, phi):
        return np.concatenate([self.r, self.phi], axis=1)
    
    def __getitem__(self, n):
        return self.data[n]
    
    @staticmethod
    def toSpheric(data):
        """
        TO-WRITE
        """
        if type(data) == list:
            data = np.array(data)
        elif type(data) == np.ndarray:
            pass
        else:
            raise ValueError("Wrong data type! Must be list or Numpy array.")
          
        if len(data.shape) == 1:
            data = data.reshape(1, -1)

        return Spheric(data)
    
    @staticmethod
    def toCartesian(data):
        """
        TO-WRITE
        """
        if type(data) == list:
            data = np.array(data)
        elif type(data) == np.ndarray:
            pass
        else:
            raise ValueError("Wrong data type! Must be list or Numpy array.")
          
        if len(data.shape) == 1:
            data = data.reshape(1, -1)

        r = data[:, 0].reshape(-1, 1)
        phi = data[:, 1:]

        x = np.multiply(np.ones(data.shape), r)

        x[:, 1] = np.multiply(x[:, 1], np.sin(phi[:, 0]))
        
        for i in range(2, x.shape[1]):
            x[:, i] = np.multiply(x[:, i - 1], np.sin(phi[:, i - 1]))
        
        for i in range(x.shape[1] - 1):
            x[:, i] = np.multiply(x[:, i], np.cos(phi[:, i]))
        
        return x