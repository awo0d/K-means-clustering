import random
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets  # 2D
import pyqtgraph.opengl as gl  # 3D
import csv

def parseCSVfile(filePath, separator=','):
    data = []
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=separator)
            next(reader)  # Skip the header row
            for row in reader:
                data.append([float(x) for x in row])
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier : {e}")
    return data

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
    colormap = [pg.intColor(i, hues=len(centroidsMap), alpha=150) for i in range(len(centroidsMap))]
    random.shuffle(colormap)

    # Adding centroids, if present:
    if () not in centroidsMap:
        spotsList.append([createCoord(c) for c in centroidsMap])
        colormap.append((255, 255, 255, 255))

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
            p.addItem(pg.ScatterPlotItem(spots=spotsList[i], brush=colormap[i], size=10., pxMode=True))
        else:
            s = gl.GLScatterPlotItem(pos=spotsList[i], color=colormap[i], size=10., pxMode=True)
            s.translate(*offset)
            if i < len(spotsList) - 1:
                s.setGLOptions("translucent")
            w.addItem(s)
    w.show()
    pg.exec()

# Charger les données à partir du fichier CSV
data = parseCSVfile("C:/Users/Utilisateur/OneDrive - yncréa/Documents/CIN2/python/Python/Projet/data/3d_data.csv")

# Afficher les données
draw(data)
