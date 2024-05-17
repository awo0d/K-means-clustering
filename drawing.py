import random
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets # 2D
import pyqtgraph.opengl as gl # 3D

# Samples content: (x, y) or (x, y, centroid_x, centroid_y) or (x, y, z) or
# (x, y, z, centroid_x, centroid_y, centroid_z). Offset: for translating the 3D data.
def draw(samples, windowSize=1000, offset=(0, 0, 0)):
    random.seed(42)
    dimMap = {2: 2, 3: 3, 4: 2, 6: 3}
    assert len(samples) > 0, "Received 0 samples."
    assert len(samples[0]) in dimMap, "Unsupported samples size."
    dim = dimMap[len(samples[0])]
    createCoord = lambda c: {"pos": c} if dim == 2 else c

    # Grouping samples in clusters for faster rendering.
    centroidsMap, spotsList = {}, []
    for c in samples:
        centroid = tuple(c[dim:])
        if centroid not in centroidsMap:
            centroidsMap[centroid] = len(centroidsMap)
            spotsList.append([])
        spotsList[centroidsMap[centroid]].append(createCoord(c[:dim]))

    # Define specific colors for the clusters
    colors = [(255, 0, 0, 255), (0, 0, 255, 255), (0, 255, 0, 255)]  # Red, Blue, Green
    colormap = [colors[i % len(colors)] for i in range(len(centroidsMap))]

    # Adding centroids, if present:
    if () not in centroidsMap:
        spotsList.append([createCoord(c) for c in centroidsMap])
        colormap.append((255, 255, 255, 255))  # White for centroids

    # Creating a graphical context:
    app = pg.mkQApp("PyQtGraph app")
    if dim == 2:
        w = QtWidgets.QMainWindow()
        view = pg.GraphicsLayoutWidget()
        w.setCentralWidget(view)
        p = view.addPlot()
    else:
        w = gl.GLViewWidget()
        w.setCameraPosition(distance=20.)
        g = gl.GLGridItem()
        w.addItem(g)
    w.setWindowTitle("Clustering data")
    w.resize(windowSize, windowSize)

    # Drawing:
    for i in range(len(spotsList)):
        if dim == 2:
            brush = pg.mkBrush(colormap[i])
            p.addItem(pg.ScatterPlotItem(spots=spotsList[i], brush=brush, size=10., pxMode=True))
        else:
            pos_array = np.array([spot for spot in spotsList[i]])
            s = gl.GLScatterPlotItem(pos=pos_array, color=colormap[i], size=10., pxMode=True)
            s.translate(*offset)
            if i < len(spotsList) - 1:
                s.setGLOptions("translucent")
            w.addItem(s)
    w.show()
    pg.exec()
