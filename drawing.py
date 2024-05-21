import random
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets  # Importation pour le dessin en 2D
import pyqtgraph.opengl as gl  # Importation pour le dessin en 3D

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

# Exemple d'appel de la fonction draw
# draw(samples, windowSize=1000, offset=(0, 0, 0)) 

"""
Fonctionnalités :
- draw(samples, windowSize=1000, offset=(0, 0, 0)): La fonction principale pour dessiner les données de clustering en 2D ou 3D.
- random.seed(42): Initialise le générateur de nombres aléatoires pour assurer la reproductibilité des couleurs des clusters.
- dimMap: Dictionnaire reliant la taille des échantillons au nombre de dimensions.
- createCoord(c): Une fonction lambda pour créer des coordonnées pour le traçage. Renvoie un dictionnaire pour les données 2D.
- centroidsMap: Un dictionnaire pour mapper les centroids aux indices de clusters.
- spotsList: Une liste de listes où chaque sous-liste contient les points appartenant à un cluster.
- colors et colormap:
    - colors: Une liste de couleurs définies pour les clusters (rouge, bleu, vert).
    - colormap: Une liste des couleurs appliquées aux clusters, cyclant à travers les couleurs définies.
- app = pg.mkQApp("PyQtGraph app"): Crée une instance de l'application PyQtGraph.
- w.show() et pg.exec(): Affiche la fenêtre et exécute la boucle d'événements PyQtGraph pour afficher les graphiques.
"""
