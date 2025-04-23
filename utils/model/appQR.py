from configparser import ConfigParser # Importation d'un packet permettent de lire et d'intégré un fichier config
import os # Importation d'un packet permettent de modifier des document (dans le cas présent, suprimer une image)

try:
    from qrcode import Qrcode
    from retrait import RetraitBDD
    from imprimante import Imprimante
except:
    from .qrcode import Qrcode
    from .retrait import RetraitBDD
    from .imprimante import Imprimante

# création de la classe Application qui permettera de géré l'ensemble du code
class ApplicationQR:
    # initialise les informations appeller dans les fonction de cette classe
    def __init__(self):
        # importe le fichier configuration
        self.__config = ConfigParser()
        self.__config.read("./utils/config/bdd.cnf")
        self.__donnee : dict = {"famille": "Solanacées", "espece": "tomate", "variete": "grappe","date_recolte":"01.01.2025","quantite_par_sachet" : "20"} # créé un dictionnaire avec les informations présent dans le future QR code
        # relie les partits de config aux partit du code concerner 
        self._qr = Qrcode(config = self.__config["QRCODE"])
        self._imprimante = Imprimante(config = self.__config["IMPRIMANTE"])
        self._retrait = RetraitBDD()


    # lance les fonctions en leurs donnent les données nécessaire
    def run(self):
        image = self._qr.creation_qrcode(self.__donnee) # appelle la fonction creation_qrcode de la classe Qrcode
        self._imprimante.impretion_qrcode(image) # appelle la fonction impretion_qrcode de la classe Imprimante
        os.remove(image) # suprime l'image
        dictionnaire = self._qr.lecture_qrcode() # appelle la fonction lecture_qrcode de la classe Retrait
        self._retrait.mise_à_jour_bdd(dictionnaire) # appelle la fonction mise_à_jour_bdd de la classe Retrait
    

# lance les fonction du main
if __name__ == "__main__":
    ap = ApplicationQR()
    ap.run()