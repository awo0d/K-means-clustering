import random
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets  # Importation pour le dessin en 2D
import pyqtgraph.opengl as gl  # Importation pour le dessin en 3D

def draw(samples, windowSize=1000, offset=(0, 0, 0)):
    """
    La fonction principale pour dessiner les données de clustering en 2D ou 3D.
    """
    random.seed(42)  # Initialise le générateur de nombres aléatoires pour assurer la reproductibilité des couleurs des clusters.
    
    # Dictionnaire reliant la taille des échantillons au nombre de dimensions
    dimMap = {2: 2, 3: 3, 4: 2, 6: 3}
    assert len(samples) > 0, "Received 0 samples."  # Vérifie qu'il y a des échantillons
    assert len(samples[0]) in dimMap, "Unsupported samples size."  # Vérifie que la taille des échantillons est supportée
    dim = dimMap[len(samples[0])]  # Détermine le nombre de dimensions à partir de la taille des échantillons
    
    # Une fonction lambda pour créer des coordonnées pour le traçage. Renvoie un dictionnaire pour les données 2D.
    createCoord = lambda c: {"pos": c} if dim == 2 else c

    # Groupement des échantillons en clusters pour un rendu plus rapide
    centroidsMap, spotsList = {}, []
    for c in samples:
        centroid = tuple(c[dim:])  # Extrait les coordonnées du centroid
        if centroid not in centroidsMap:
            centroidsMap[centroid] = len(centroidsMap)  # Associe chaque centroid à un indice unique
            spotsList.append([])  # Initialise une nouvelle liste pour ce cluster
        spotsList[centroidsMap[centroid]].append(createCoord(c[:dim]))  # Ajoute les coordonnées du point au cluster correspondant

    # Définition des couleurs spécifiques pour les clusters
    colors = [(255, 0, 0, 255), (0, 0, 255, 255), (0, 255, 0, 255)]  # Rouge, Bleu, Vert
    colormap = [colors[i % len(colors)] for i in range(len(centroidsMap))]  # Applique les couleurs de manière cyclique aux clusters

    # Ajout des centroids, si présents
    if () not in centroidsMap:
        spotsList.append([createCoord(c) for c in centroidsMap])  # Ajoute les centroids à la liste des spots
        colormap.append((255, 255, 255, 255))  # Blanc pour les centroids

    # Création d'un contexte graphique
    app = pg.mkQApp("PyQtGraph app")  # Crée une instance de l'application PyQtGraph
    
    if dim == 2:
        # Configuration pour une vue 2D
        w = QtWidgets.QMainWindow()
        view = pg.GraphicsLayoutWidget()
        w.setCentralWidget(view)
        p = view.addPlot()  # Ajoute une zone de traçage
    else:
        # Configuration pour une vue 3D
        w = gl.GLViewWidget()
        w.setCameraPosition(distance=20.)  # Positionne la caméra
        g = gl.GLGridItem()
        w.addItem(g)  # Ajoute une grille pour la référence visuelle
    
    w.setWindowTitle("Clustering data")  # Définit le titre de la fenêtre
    w.resize(windowSize, windowSize)  # Redimensionne la fenêtre

    # Dessin des clusters
    for i in range(len(spotsList)):
        if dim == 2:
            brush = pg.mkBrush(colormap[i])  # Crée un pinceau avec la couleur du cluster
            p.addItem(pg.ScatterPlotItem(spots=spotsList[i], brush=brush, size=10., pxMode=True))  # Ajoute les points au graphique 2D
        else:
            pos_array = np.array([spot for spot in spotsList[i]])  # Convertit les spots en un tableau numpy
            s = gl.GLScatterPlotItem(pos=pos_array, color=colormap[i], size=10., pxMode=True)  # Crée un élément de dispersion pour le graphique 3D
            s.translate(*offset)  # Applique un décalage si nécessaire
            if i < len(spotsList) - 1:
                s.setGLOptions("translucent")  # Rend les points translucides sauf le dernier
            w.addItem(s)  # Ajoute les points au graphique 3D
    
    w.show()  # Affiche la fenêtre
    pg.exec()  # Exécute la boucle d'événements PyQtGraph pour afficher les graphiques

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
