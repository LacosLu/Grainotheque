from utils.model import Qrcode_grainotheque

from unittest import TestCase,main
from configparser import ConfigParser
import os 



class test_Qrcode_grainotheque(TestCase):

    def setUp(self):
        self.__chemin_image = './utils/temp'
        self.__config = ConfigParser()
        self.__config.read('./utils/config/bdd.cnf')
        self.__config_qrcode = self.__config["QRCODE"]
        self.__qr = Qrcode_grainotheque(config = self.__config_qrcode)



    def test_creation_qrcode(self):
        """ Test de la création d'un Qr code  """
        nom_image_cree = 'qr.png'
        donnee : dict = {"famille": "Solanacées", "espece": "Tomate", "variete": "Grappe","date_recolte":"01.01.2025","quantite_par_sachet" : "20"}
        fichier_image = f'{self.__config_qrcode['chemin_image']}/{nom_image_cree}'
        self.assertFalse(os.path.exists(fichier_image))
        image = self.__qr.creation_qrcode(donnee,nom_image_cree)
        self.assertEqual(f'{self.__config_qrcode['chemin_image']}/{nom_image_cree}',image)
        self.assertTrue(os.path.exists(fichier_image))
        os.remove(image)
        self.assertFalse(os.path.exists(fichier_image))




    def test_lecture_qrcode_lisible(self):
        """ Test de la lecture d'un QR code  """
        nom_image_lu = "qr.jpg"
        dictionnaire_voulu :  dict = {'famille': 'Solanacées', 'espece': 'Tomate', 'variete': 'Grappe', 'date_recolte': '01.01.2025', 'quantite_par_sachet': '20', 'url_aide': ''}
        fichier_image = f"{self.__chemin_image}/{nom_image_lu}"
        self.assertTrue(os.path.exists(fichier_image))
        dictionnaire = self.__qr.lecture_qrcode(nom_image_lu)
        self.assertEqual(dictionnaire,dictionnaire_voulu)
       



    def test_lecture_qrcode_non_lisible(self):
        """ Test de l'erreur lors que le QR code n'est pas lisible """
        nom_image_lu = "qr_non_lisible.jpg"
        fichier_image = f'{self.__chemin_image}/{nom_image_lu}'
        self.assertTrue(os.path.exists(fichier_image))

        try:
            self.assertRaises(Exception, lambda: self.__qr.lecture_qrcode(nom_image_lu))
        except Exception as e:
            self.assertEqual(str(e),"QR code illisible !")
        
            



if __name__ == '__main__':
    main(verbosity=2)

   