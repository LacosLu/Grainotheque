from configparser import ConfigParser # Importation d'un packet permettent de lire et d'intégré un fichier config
import os # Importation d'un packet permettent de modifier des document (dans le cas présent, suprimer une image)

try:
    from utils.model.qrcode_grainotheque import Qrcode_grainotheque
    from utils.model.bdd_retrait import RetraitBDD
    from utils.model.imprimante import Imprimante
except:
    from qrcode_grainotheque import Qrcode_grainotheque
    from bdd_retrait import RetraitBDD
    from imprimante import Imprimante

# création de la classe Application qui permettera de géré l'ensemble du code
class ApplicationQR:
    # initialise les informations appeller dans les fonction de cette classe
    def __init__(self, nom_centre_social : str = "Centre Social et Socioculturel du Chemillois"):
        # importe le fichier configuration
        self.__config = ConfigParser()
        self.__config.read("./utils/config/bdd.cnf")
        self.__donnee : dict = {"famille": "Solanacées", "espece": "Tomate", "variete": "Grappe","date_recolte":"01.01.2025","quantite_par_sachet" : "20"} # créé un dictionnaire avec les informations présent dans le future QR code
        self.__nom_centre_social = nom_centre_social
        # relie les partits de config aux partit du code concerner 
        self._qr = Qrcode_grainotheque(config = self.__config["QRCODE"])
        self._imprimante = Imprimante(config = self.__config["IMPRIMANTE"])
        self._retrait = RetraitBDD(self.__nom_centre_social)


    # lance les fonctions en leurs donnent les données nécessaire
    def run(self):
        image = self._qr.creation_qrcode(self.__donnee) # appelle la fonction creation_qrcode de la classe Qrcode
        # self._imprimante.impretion_qrcode(image) # appelle la fonction impretion_qrcode de la classe Imprimante
        # os.remove(image) # suprime l'image
        # dictionnaire = self._qr.lecture_qrcode() # appelle la fonction lecture_qrcode de la classe Retrait
        # print(dictionnaire)
        #self._retrait.mise_à_jour_bdd(dictionnaire) # appelle la fonction mise_à_jour_bdd de la classe Retrait
    

# lance les fonction du main
if __name__ == "__main__":
    ap = ApplicationQR()
    ap.run()