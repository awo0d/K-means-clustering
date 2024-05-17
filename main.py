import random
import numpy as np
import csv
from drawing import draw  # Importer la fonction draw depuis drawing.py

def parseCSVfile(filePath, separator=None):
    data = []
    fileData = []
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            content = file.read()
            if separator is None:
                separator = analyseCSV(content)
            
            subContent = content
            while subContent:
                if "\n" in subContent:
                    ligne = subContent[:subContent.find("\n")]
                    ligne = ligne.split(separator)
                    fileData.append(ligne)
                    subContent = subContent[subContent.find("\n") + 1:]
                else:
                    subContent = subContent.split(separator)
                    fileData.append(subContent)
                    break
            
            for coordonnates in fileData:
                if coordonnates != fileData[0]:
                    temporary = list(map(float, coordonnates))
                    data.append(temporary)
    except FileNotFoundError:
        print(f"Erreur : le fichier {filePath} est introuvable.")
    except Exception as e:
        print(f"Erreur lors de l'ouverture du fichier : {e}")
    
    return data

def analyseCSV(CSVcontent):
    dictionnary = {}
    for i in CSVcontent:
        if i in dictionnary:
            dictionnary[i] += 1
        else:
            dictionnary[i] = 1
    
    values = list(dictionnary.values())
    keys = list(dictionnary.keys())
    number = max(values)
    character = keys[values.index(number)]

    return character

def findMaxDistance(data):
    maxDistance = 0
    for d in data:
        distance = distanceCalculation(d, [0] * len(d))
        if distance > maxDistance:
            maxDistance = distance
    return maxDistance

def initCentroide(data, nCentr): #nCentr is the number of centroids
    centroids = []
    try:
        i = 0
        verif = True
        maxDistance = findMaxDistance(data)
        while i < nCentr:
            hasard = data[random.randint(0, len(data) - 1)]
            isIncentroid = hasard in centroids
            for c in centroids:
                if distanceCalculation(hasard, c) < maxDistance/5.5:
                    verif = False
                    break
            if not isIncentroid and verif:
                centroids.append(hasard.copy())
                i += 1
            verif = True
    except Exception as e:
        print(f"Error when the initialisation occurred : {e}")
    return data, centroids

def distanceCalculation(pointA, pointB):
    return sum((a - b) ** 2 for a, b in zip(pointA, pointB)) ** 0.5

def distanceCalc(point, centroids): # calculate the distance between the point and the nearest centroid
    distances = [distanceCalculation(point, c) for c in centroids]
    min_distance = min(distances)
    closest_centroid = centroids[distances.index(min_distance)]
    return min_distance, closest_centroid

def affectCentroid(data, centroids):
    distances = []
    for i in range(len(data)):
        if len(data[i]) > len(centroids[0]): # centroids already affected
            data[i] = data[i][:len(centroids[0])]
        distance, centroid = distanceCalc(data[i], centroids)
        distances.append(distance)
        data[i].extend(centroid)
    return data, distances

def defineClusters(data, centroids):
    clusters = {tuple(c): [] for c in centroids}
    for d in data:
        centroid = tuple(d[len(d)//2:])
        clusters[centroid].append(d[:len(d)//2])
    return clusters

def defineGravityCenters(clusters):
    gravityCentres = []
    for points in clusters.values():
        gravityCentres.append([sum(coord) / len(points) for coord in zip(*points)])
    return gravityCentres

def changeCentroids(data, centroids):
    clusters = defineClusters(data, centroids)
    new_centroids = defineGravityCenters(clusters)
    if new_centroids == centroids:
        return centroids, clusters
    return new_centroids, clusters

def evalClusterQuality(clusters, distances):
    qualities = []
    index = 0
    for cluster in clusters.values():
        if cluster:
            quality = sum(distances[index:index + len(cluster)]) / len(cluster)
            qualities.append(quality)
            index += len(cluster)
    return qualities

def clustering():
    iteration = 0
    verif = 0
    clusters = []
    distances = []
    qualities = []

    dataFormat = int(input("Please choose between 2D or 3D (2 or 3) : "))

    if dataFormat == 2:
        pathFile = "./data/2d_data.csv" # depend of the structure
    else:
        pathFile = "./data/3d_data.csv" # depend of the structure

    k = int(input("Please enter the number of k-means : "))
    data = parseCSVfile(pathFile, ',')
    if not data:
        print("Erreur : Aucun échantillon reçu. Vérifiez le fichier CSV.")
        return

    data, centroids = initCentroide(data, k)

    while iteration is not None:
        saveDistances = distances.copy() # comparison with the previous distances
        data, distances = affectCentroid(data, centroids)
        centroids, clusters = changeCentroids(data, centroids)

        qualities = evalClusterQuality(clusters, distances)

        if distances == saveDistances:
            distances = None

        if iteration >= 100 or clusters is None or distances is None:  # Limiting the iterations to avoid infinite loops
            iteration = None

        if iteration is not None:
            iteration += 1

    draw(data)

clustering()

def printData(data):
    if isinstance(data, list):
        for i in data:
            print(i)
    else:
        print("Error, data is not a list!")
