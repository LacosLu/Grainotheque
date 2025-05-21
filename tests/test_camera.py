# ----- IMPORTS -----
# --- Bibliothèques internes ---
from utils.model.camera import Camera

# --- Bibliothèques externes ---
import unittest
import cv2 as cv

# ----- CLASSE -----
class Test_Camera(unittest.TestCase):

    def setUp(self):
        pass

    
    def test_prendre_photo(self):
        """Test de la prise de photo
        """
        img_old = cv.imread(cv.samples.findFile("./utils/temp/img.jpg"))
        Camera.photographier()
        img = cv.imread(cv.samples.findFile("./utils/temp/img.jpg"))
        self.assertNotEqual(img_old.all(), img.all())

    def test_lire_photo(self):
        """Test de la lecture de la photo
        """
        img = cv.imread(cv.samples.findFile("./utils/temp/img.jpg"))
        self.assertEqual(img.all(), Camera.lire_photo().all())