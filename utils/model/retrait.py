from pymysql import connect,Connection # Importe le paquet pymysql installé pour la connection et la manipulation d'une BDD
from pymysql.cursors import DictCursor


# création de la classe Retrait qui permet la lecture d'un QR code et la mise à jour de la base de donnée
class RetraitBDD :
    # initialise les informations appeller dans les fonction de cette classe
    def __init__(self,nom_centre_social):
        try:
            self.__connexion : Connection = connect(read_default_file="./utils/config/bdd.cnf") # element de connection à la BDD
        except:
            print("Connexion non réussie")
        self.__nom_centre_social = nom_centre_social

    # mettre à jour la BDD
    def mise_à_jour_bdd(self,dictionnaire):
        # récupere la variété dans le dictionnaire 
        variete = dictionnaire.get('variete')

        # requete pour retire un sachet du stock de la variété dans la BDD
        requete ="""
                UPDATE graine 
                SET quantite_sachet = quantite_sachet - 1 
                WHERE id_variete = (
                    SELECT id_variete FROM variete WHERE nom_variete = %s
                )
                AND WHERE id_grainotheque = (
                    SELECT id_grainotheque FROME grainotheque WHERE nom_grainotheque = %s
                )
                """
        param = (variete,self.__nom_centre_social,)

        try:
            # se connecte à la BDD et déclanche la requete 
            curseur: DictCursor= self.__connexion.cursor(DictCursor)
            curseur.execute(requete,param)
            self.__connexion.commit() # met à jour la base
            self.__connexion.close()
        except:
            # en cas déchèque à la connexion 
            raise("Pas de connexion")
