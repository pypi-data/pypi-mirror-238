"""
Проекция многомерных данных в пространства меньших размеров.
Использовать только в Python-блокнотах (.ipynb).
"""

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import umap

from numpy import pi, sin, cos
from numpy.typing import ArrayLike
from sklearn.preprocessing import StandardScaler


def __draw_sphere(fig):
    """
    Отрисовка единичной сферы на графике.

    :param fig: график
    """
    theta = np.linspace(0, 2*pi, 120)
    phi = np.linspace(0, pi, 60)
    u , v = np.meshgrid(theta, phi)
    xs = cos(u)*sin(v)
    ys = sin(u)*sin(v)
    zs = cos(v)

    x = []
    y = []
    z = []
    for t in [theta[10*k] for k in range(12)]:
        x.extend(list(cos(t)*sin(phi))+[None])
        y.extend(list(sin(t)*sin(phi))+[None]) 
        z.extend(list(cos(phi))+[None])
        
    for s in [phi[6*k] for k in range(10)]: 
        x.extend(list(cos(theta)*sin(s))+[None])
        y.extend(list(sin(theta)*sin(s))+[None]) 
        z.extend([cos(s)]*120+[None])
    
    fig.add_surface(x=xs, y=ys, z=zs, 
                colorscale=[[0, '#ffffff' ], [1, '#ffffff']], 
                showscale=False, opacity=0.8)

    fig.add_scatter3d(x=x, y=y, z=z, mode='lines', line_width=2, line_color='rgb(10,10,10)', name='')

def __standardize(data: ArrayLike):
    """
    Стандартизация данных. Нулевое выборочное среднее и единичная выборочная дисперсия.
    """
    scaler = StandardScaler()

    return scaler.fit_transform(data)

def __spheric_projection(data: ArrayLike):
    """
    Нормировка данных: проецирование на поверхность гиперсферы.
    """
    data /= np.linalg.norm(data, axis=1)[:, None]

    return data

def project(data: ArrayLike, **kwargs):
    """
    Уменьшение размерности данных с помощью алгоритма UMap.
    Перед подачей на алгоритм снижения размерности проводится нормировка данных.

    Подробнее: https://pair-code.github.io/understanding-umap/

    :param data: выборка данных в пространстве большой размерности

    Принимает на вход также параметры класса `umap.UMAP`.

    :return: выборка данных в пространстве меньшей размерности
    """
    data /= np.linalg.norm(data, axis=1)[:, None]
    manifold = umap.UMAP(**kwargs).fit(data)
    embedded_data = manifold.transform(data)
    return embedded_data

def visualize_3d(data3D: ArrayLike, classes: ArrayLike, label: str, spheric: bool=True):
    """
    Построение трёхмерного графика распределения данных с разметкой классов.

    :param data3D: массив трёхмерных данных
    :param classes: метки классов экземпляров данных
    :param label: категория классификации (например, раса, гендер и т.п.)
    :param spheric: проекция на поверхность сферы
    """
    assert data3D.shape[1] == 3

    data3D = __standardize(data3D)

    if spheric:
        data3D = __spheric_projection(data3D)
    
    fig = px.scatter_3d(
            data3D, x=0, y=1, z=2,
            color=classes, labels={'color': label})
    fig.update_traces(marker_size=2)

    if spheric:
        __draw_sphere(fig)
    
    fig.show()

def visualize_2d(data2D, classes, label):
    """
    Построение двумерного графика распределения данных.

    :param data2D: массив двумерных данных
    :param classes: метки классов экземпляров данных
    :param label: категория классификации (например, раса, гендер и т.п.)
    """
    assert data2D.shape[1] == 2

    data2D = __stanardize(data2D)

    fig = px.scatter(
        data2D, x=0, y=1,
        color=classes, labels={'color': label})
    fig.update_traces(marker_size=2)