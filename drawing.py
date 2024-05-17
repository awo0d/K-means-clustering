# Installation:
# (Linux) sudo apt-get install python-opengl python3-pyqt5 pyqt5-dev-tools qttools5-dev-tools
# (All) pip install pyqtgraph pyopengl PyQt5

# Documentation:
# - https://pyqtgraph.readthedocs.io/en/latest/api_reference/index.html#pyqtgraph-api-ref
# - https://pyqtgraph.readthedocs.io/en/pyqtgraph-0.13.0/index.html

# Running examples:
# import pyqtgraph.examples
# pyqtgraph.examples.run()
import sys
print(sys.path)

import random
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets # 2D
import pyqtgraph.opengl as gl # 3D

# Samples content: (x, y) or (x, y, centroid_x, centroid_y) or (x, y, z) or
# (x, y, z, centroid_x, centroid_y, centroid_z). Offset: for translating the 3D data.
def draw(samples, windowSize=1000, offset=(0, 0, 0)):
	random.seed(42)
	dimMap = { 2: 2, 3: 3, 4: 2, 6: 3 }
	assert len(samples) > 0, "Received 0 samples."
	assert len(samples[0]) in dimMap, "Unsupported samples size."
	dim = dimMap[len(samples[0])]
	createCoord = lambda c : { "pos": c } if dim == 2 else c

	# Grouping samples in clusters for faster rendering.
	# Note: clusters number defaults to 1 if no centroids are in the data.
	centroidsMap, spotsList = {}, []
	for c in samples:
		centroid = tuple(c[dim:])
		if centroid not in centroidsMap:
			centroidsMap[centroid] = len(centroidsMap)
			spotsList.append([])
		spotsList[centroidsMap[centroid]].append(createCoord(c[:dim]))
	colormap = [ pg.intColor(i, hues=len(centroidsMap), alpha=150) for i in range(len(centroidsMap)) ]
	random.shuffle(colormap) # so close clusters are less likely to have close colors.

	# Adding centroids, if present:
	if () not in centroidsMap:
		spotsList.append([ createCoord(c) for c in centroidsMap ])
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
			if i < len(spotsList)-1:
				s.setGLOptions("translucent")
			w.addItem(s)
	w.show()
	pg.exec()
