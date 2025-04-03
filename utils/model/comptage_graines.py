# ----- IMPORTS -----
# --- Bibliothèques externes ---
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# --- Bibliothèques internes ---
try:
    from camera import Camera
except:
    from .camera import Camera

# ----- CLASSE -----
class ComptageGraines:
    @staticmethod
    def comptage_contours(treshold : int = 95):
        """Fonction de comptage des graines en fonction des contours à plus ou moins 5 graines près"""
        # --- Chargement de l'image ---
        img = Camera.lire_photo()

        # --- Passage en nuance de gris ---
        gray_image=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

        # --- Passage en rgb ---
        rgb_image=cv.cvtColor(img,cv.COLOR_BGR2RGB)

        # --- Image binaire (tout noir ou tout blanc) ---
        _, binary_image= cv.threshold(gray_image, treshold, 255, 0)

        # --- Détection des contours ---
        contours, _ = cv.findContours(binary_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # --- Comptage des contours ---
        seed_number : int = 0
        for contour in contours:
            area_contour = cv.contourArea(contour)      # Calcul de l'aire du contour
            if 1_000 < area_contour < 50_000:           # Mettre l'air dans un intervalle permettant une approximation à +/- 5
                # -- Détour des graine dans l'image --
                hull = cv.convexHull(contour)
                cv.drawContours(rgb_image, [hull], 0, (0, 0, 255), 2)

                seed_number += 1

        # --- Retour ---
        plt.imshow(rgb_image)
        plt.text(10, 90,f"{seed_number}  coins detected" , color='blue', fontsize=15)
        plt.show()

        if seed_number > 0:
            return seed_number
        else:
            return ComptageGraines.comptage_contours(160)
    
# ----- PROGRAMME -----
if __name__ == "__main__":
    print(ComptageGraines.comptage_contours())