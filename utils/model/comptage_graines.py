# ----- IMPORTS -----
# --- Bibliothèques externes ---
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# --- Bibliothèques internes ---
from ..deep_learning import *
try:
    from camera import Camera
except:
    from .camera import Camera

# ----- CLASSE -----
class Graines:
    __chemin_photo : str = "./utils/temp/img.jpg"
    def __init__(self):
        self.__ternaire : TrainDLTernaire = TrainDLTernaire(f"ternaire.pt")
        self.__binaire : TrainDLBinaire = TrainDLBinaire(f"binaire.pt")
        self.__compte_gb : TrainDLCompte = TrainDLCompte(f"compte_grosses_blanches.pt")
        self.__compte_gn : TrainDLCompte = TrainDLCompte(f"compte_grosses_noirs.pt")
        self.__compte_mb : TrainDLCompte = TrainDLCompte(f"compte_moyennes_blanches.pt")
        self.__compte_mn : TrainDLCompte = TrainDLCompte(f"compte_moyennes_noirs.pt")
        self.__compte_pb : TrainDLCompte = TrainDLCompte(f"compte_petites_blanches.pt")
        self.__compte_pn : TrainDLCompte = TrainDLCompte(f"compte_petites_noirs.pt")

    def compter_graines(self):
        print(self.__ternaire.evaluate(Graines.__chemin_photo))
    
# ----- PROGRAMME -----
if __name__ == "__main__":
    graines = Graines()
    graines.compter_graines()