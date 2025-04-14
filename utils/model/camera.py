# ----- IMPORTS -----
# --- Bibliothèques externes ---
import cv2 as cv
import subprocess
from os import system

# --- Bibliothèques internes ---
try:
    from led import Led
except:
    from .led import Led

# ----- CLASSE -----
class Camera:
    @staticmethod
    def photographier(nom_img : str = "img"):
        """Prend une photo à l'aide de la caméra"""
        leds = Led()
        leds.toggle()
        subprocess.run(['libcamera-jpeg', '-o', f'./utils/temp/{nom_img}.jpg'])
        leds.toggle()
        system("clear")

    @staticmethod
    def lire_photo():
        """Récupère la photo sous forme de matrice"""
        img = cv.imread(cv.samples.findFile("./utils/temp/img.jpg"))

        return img

# ----- PROGRAMME -----
if __name__ == "__main__":
    Camera.photographier()