"""TO-WRITE"""

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import umap

from numpy import pi, sin, cos
from sklearn.preprocessing import StandardScaler


def __draw_sphere(fig):
    """
    TO-WRITE
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

def __standardize(data):
    """
    TO-WRITE
    """
    scaler = StandardScaler()

    return scaler.fit_transform(data)

def __spheric_projection(data):
    """
    TO-WRITE
    """
    data /= np.linalg.norm(data, axis=1)[:, None]

    return data

def project_3d(data):
    """
    TO-WRITE
    """
    data /= np.linalg.norm(data, axis=1)[:, None]
    manifold = umap.UMAP(n_components=3).fit(data)
    embedded_data = manifold.transform(data)
    return embedded_data

def visualize_3d(data3D, classes, label, spheric=True):
    """
    TO-WRITE
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