"""Пробразования данных между системами координат"""

import numpy as np
from numpy.typing import ArrayLike


def toSpheric(data: ArrayLike):
    """
    Преобразование данных из декартовой в сферическую систему координат.
    
    :param data: выборка данных в декартовой системе координат
    :return: выборка данных в сферической системе координат
    """

    if type(data) == list:
        data = np.array(data)
    elif type(data) == np.ndarray:
        pass
    else:
        raise ValueError("Wrong data type! Must be list or Numpy array.")
    
    if len(data.shape) == 1:
        data = data.reshape(1, -1)
    
    n_dim = data.shape[1]

    def n_phi(self, n: int):
        """
        Вычисление угла вектора в сферической системе координат в n-м измерении.

        :param n: номер измерения в пространстве
        :return: массив углов
        """
        if n < n_dim - 2:
            return np.arctan2(np.linalg.norm(data[:, n + 1:], axis=1), data[:, n])
        elif n == n_dim - 2:
            return np.arctan2(data[:, -1], data[:, n])
        else:
            raise IndexError("Too many angles for this sample")
        
    r = np.linalg.norm(data, axis=1).reshape(-1, 1)
    np.array([n_phi(n) for n in range(n_dim - 1)]).T
    data = np.concatenate([r, phi], axis=1)

    return data


def toCartesian(data: ArrayLike):
    """
    Преобразование данных из сферической в декартовую систему координат.

    :param data: выборка данных в сферической системе координат
    :return: выборка данных в декартовой системе координат
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