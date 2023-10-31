"""Проведение метода главных компонент на сферических данных"""

import numpy as np
from numpy import ndarray
from sklearn.decomposition import PCA
from .spheric import Spheric


class SPCA(PCA):
    """
    Уменьшение размерности данных, распределенных в положительной четверти гиперсферы 
    с помощью метода главных компонент (PCA).

    Класс наследует методы и члены данных класса `sklearn.decomposition.PCA` и принимает на вход
    те же аргументы.

    Выборка приводится к единичному радиусу гиперсферы путём нормировки каждого экземпляра данных.
    Затем проводится преобразование исходных данных из декартовой системы координат
    в сферическую (N-мерной размерности).

    На вход метода главных компонент (из библиотеки scikit-learn) подаются значения углов каждого
    вектора в сферическом пространстве.

    Важно отметить, что данная реализация PCA корректна только для данных, распределённых в положительной
    четверти гиперсферы (все компоненты положительны).

    Для проведения PCA на данных, распределённых на всей поверхности гиперсферы,
    необходимо написать отдельный метод на основе сингулярного разложения матриц.
    (см. http://gitlab.td/ml-research/sphericalpca/-/tree/master/sources )
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def __normalize(self, X):
        """
        Нормировка исходной выборки.
        """
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