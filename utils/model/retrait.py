from pymysql import connect,Connection # Importe le paquet pymysql installé pour la connection et la manipulation d'une BDD
from pymysql.cursors import DictCursor


# création de la classe Retrait qui permet la lecture d'un QR code et la mise à jour de la base de donnée
class RetraitBDD :
    # initialise les informations appeller dans les fonction de cette classe
    def __init__(self):
        try:
            self.__connexion : Connection = connect(read_default_file="./utils/config/bdd.cnf") # element de connection à la BDD
        except:
            print("Connexion non réussie")

    # mettre à jour la BDD
    def mise_à_jour_bdd(self,dictionnaire):
        variete = dictionnaire.get('variete')
        # requete permetant de retiré un sachet au stock
        try:
            requete ="""
                UPDATE graine 
                SET quantite_sachet = quantite_sachet - 1 
                WHERE id_variete = (
                    SELECT id_variete FROM variete WHERE nom_variete = %s
                )
                """
            curseur: DictCursor= self.__connexion.cursor(DictCursor)
            curseur.execute(requete, (variete,))
            curseur.fetchall()
            self.__connexion.commit() # met à jour la base
            self.__connexion.close()
        except:
            print("Pas de connexion")
