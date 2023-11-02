import os
from deepface import DeepFace
from deepface.commons import functions, realtime, distance as dst


models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

backends = [
    "retinaface",
]


def getEmbeddingVector(path: str):
    embed = []
    data = DeepFace.represent(path, model_name=models[2], enforce_detection=True, detector_backend=backends[0])
    for imgdata in data:
        embed.append(imgdata['embedding'])
    
    return embed

def extractFace(path: str):
    data = DeepFace.represent(path, model_name=models[2], enforce_detection=True, detector_backend=backends[0])
    return data

def getDistance(source, target):
    dist = dst.findCosineDistance(source, target)
    return dist

def getTreshold():
    threshold = dst.findThreshold(models[2], "cosine")
    return threshold