import random
import numpy as np
import csv
from drawing import draw  # Importer la fonction draw depuis drawing.py

def parseCSVfile(filePath, separator=None):
    # Parse un fichier CSV et renvoie les données sous forme de liste de listes de floats
    data = []
    fileData = []
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            content = file.read()
            if separator is None:
                separator = analyseCSV(content)  # Détermine le séparateur le plus courant
            
            subContent = content
            while subContent:
                if "\n" in subContent:
                    ligne = subContent[:subContent.find("\n")]  # Extrait une ligne jusqu'à la première nouvelle ligne
                    ligne = ligne.split(separator)  # Sépare les valeurs en utilisant le séparateur
                    fileData.append(ligne)
                    subContent = subContent[subContent.find("\n") + 1:]  # Mise à jour du contenu pour la prochaine itération
                else:
                    subContent = subContent.split(separator)
                    fileData.append(subContent)
                    break
            
            for coordonnates in fileData:
                if coordonnates != fileData[0]:  # Ignore l'en-tête
                    temporary = list(map(float, coordonnates))  # Convertit les valeurs en float
                    data.append(temporary)
    except FileNotFoundError:
        print(f"Erreur : le fichier {filePath} est introuvable.")
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier : {e}")
    
    return data

def analyseCSV(CSVcontent):
    # Analyse le contenu du CSV pour déterminer le séparateur le plus courant
    dictionnary = {}
    for i in CSVcontent:
        if i in dictionnary:
            dictionnary[i] += 1  # Incrémente le compteur pour le caractère existant
        else:
            dictionnary[i] = 1  # Ajoute le caractère au dictionnaire avec un compteur de 1
    
    values = list(dictionnary.values())
    keys = list(dictionnary.keys())
    number = max(values)  # Trouve le nombre maximum d'occurrences
    character = keys[values.index(number)]  # Trouve le caractère correspondant
    
    return character

def findMaxDistance(data):
    # Trouve la distance max des points par rapport à l'origine
    maxDistance = 0
    for d in data:
        distance = distanceCalculation(d, [0] * len(d))  # Calcule la distance à l'origine
        if distance > maxDistance:
            maxDistance = distance  # Met à jour la distance max si une plus grande distance est trouvée
    return maxDistance

def initCentroide(data, nCentr):  # nCentr est le nombre de centroids
    # Initialise les centroids pour l'algorithme k-means
    centroids = []
    try:
        i = 0
        verif = True
        maxDistance = findMaxDistance(data)  # Trouve la distance max pour la validation
        while i < nCentr:
            hasard = data[random.randint(0, len(data) - 1)]  # Sélectionne un point aléatoire
            isIncentroid = hasard in centroids
            for c in centroids:
                if distanceCalculation(hasard, c) < maxDistance / 5.5:  # Vérifie que les centroids sont suffisamment éloignés
                    verif = False
                    break
            if not isIncentroid and verif:
                centroids.append(hasard.copy())  # Ajoute le point comme un centroid
                i += 1
            verif = True
    except Exception as e:
        print(f"Error when the initialisation occurred: {e}")
    return data, centroids

def distanceCalculation(pointA, pointB):
    # Calcule la distance euclidienne entre deux points
    return sum((a - b) ** 2 for a, b in zip(pointA, pointB)) ** 0.5  # Somme des carrés des différences et racine carrée

def distanceCalc(point, centroids):
    # Calcule la distance entre un point et le centroid le plus proche et renvoie cette distance ainsi que le centroid le plus proche
    distances = [distanceCalculation(point, c) for c in centroids]  # Calcule les distances à chaque centroid
    min_distance = min(distances)  # Trouve la distance minimale
    closest_centroid = centroids[distances.index(min_distance)]  # Trouve le centroid le plus proche
    return min_distance, closest_centroid

def affectCentroid(data, centroids):
    # Assigne chaque point de données au centroid le plus proche et met à jour les distances
    distances = []
    for i in range(len(data)):
        if len(data[i]) > len(centroids[0]):  # Garde uniquement les coordonnées des points, pas des centroids
            data[i] = data[i][:len(centroids[0])]
        distance, centroid = distanceCalc(data[i], centroids)
        distances.append(distance)
        data[i].extend(centroid)  # Ajoute les coordonnées du centroid au point
    return data, distances

def defineClusters(data, centroids):
    # Définit les clusters en assignant chaque point de données à son centroid respectif
    clusters = {tuple(c): [] for c in centroids}  # Initialisation des clusters
    for d in data:
        centroid = tuple(d[len(d) // 2:])  # Sépare les points des centroids
        clusters[centroid].append(d[:len(d) // 2])
    return clusters

def defineGravityCenters(clusters):
    # Calcule les centres de gravité pour chaque cluster
    gravityCentres = []
    for points in clusters.values():
        gravityCentres.append([sum(coord) / len(points) for coord in zip(*points)])  # Moyenne des coordonnées pour chaque dimension
    return gravityCentres

def changeCentroids(data, centroids):
    # Met à jour les centroids en calculant les nouveaux centres de gravité et retourne les nouveaux centroids et les clusters
    clusters = defineClusters(data, centroids)
    new_centroids = defineGravityCenters(clusters)
    if new_centroids == centroids:
        return centroids, clusters
    return new_centroids, clusters

def evalClusterQuality(clusters, distances):
    # Évalue la qualité des clusters en calculant la distance moyenne entre les points de chaque cluster et leur centroid respectif
    qualities = []
    index = 0
    for cluster in clusters.values():
        if cluster:
            quality = sum(distances[index:index + len(cluster)]) / len(cluster)  # Moyenne des distances pour le cluster
            qualities.append(quality)
            index += len(cluster)  # Mise à jour de l'index pour le prochain cluster
    return qualities

def clustering():
    # Gère l'ensemble du processus de clustering, y compris l'initialisation, l'affectation des centroids, la mise à jour des centroids, et le traçage des résultats
    iteration = 0
    clusters = []
    distances = []
    qualities = []

    dataFormat = int(input("Choose 2D or 3D (2 or 3): "))  # Demande à l'utilisateur de choisir entre 2D et 3D

    if dataFormat == 2:
        pathFile = "./data/2d_data.csv"  # Chemin du fichier pour les données 2D
    else:
        pathFile = "./data/3d_data.csv"  # Chemin du fichier pour les données 3D

    k = int(input("Please enter the number of k-means: "))  # Demande à l'utilisateur le nombre de clusters
    data = parseCSVfile(pathFile, ',')
    if not data:
        print("Erreur : Aucun échantillon reçu. Vérifiez le fichier CSV.")
        return

    data, centroids = initCentroide(data, k)

    while iteration is not None:
        saveDistances = distances.copy()  # Sauvegarde des distances pour la comparaison avec les distances précédentes
        data, distances = affectCentroid(data, centroids)
        centroids, clusters = changeCentroids(data, centroids)

        qualities = evalClusterQuality(clusters, distances)

        if distances == saveDistances:
            distances = None  # Stoppe l'itération si les distances ne changent plus

        if iteration >= 100 or clusters is None or distances is None:  # Limite le nombre d'itérations pour éviter les boucles infinies
            iteration = None

        if iteration is not None:
            iteration += 1

    draw(data)  # Dessine les clusters

def printData(data):
    # Imprime les données si elles sont sous forme de liste
    if isinstance(data, list):
        for i in data:
            print(i)
    else:
        print("Error, data is not a list!")

clustering()
