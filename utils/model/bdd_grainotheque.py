# ----- IMPORTS -----
from pymysql import connect, Connection
from pymysql.cursors import DictCursor
from typing import Any

# ----- CLASSES -----
class BDDGrainotheque:
    def __init__(self, nom_grainotheque : str = ""):
        """Lien avec la base de données de la Grainothèque"""
        try:
            self.__connexion : Connection = connect(read_default_file="./utils/config/bdd.cnf")
        except:
            print("Connexion non réussie")
        self.__nom_grainotheque : str = nom_grainotheque

    def recherche_graine(self, informations : dict[str,str|int]) -> bool:
        """Fonction de recherche de la graine dans la base de données"""
        try:
            requete : str = """
            SELECT nom_famille, nom_espece, nom_variete 
            FROM graine
            NATURAL JOIN famille
            NATURAL JOIN espece
            NATURAL JOIN variete
            NATURAL JOIN grainotheque
            WHERE nom_famille = %s
            AND nom_espece = %s
            AND nom_variete = %s
            AND nom_grainotheque = %s;
            """

            parametres : tuple[Any] = (
                informations["famille"],
                informations["espece"],
                informations["variete"],
                self.__nom_grainotheque
            )

            curseur : DictCursor = self.__connexion.cursor(DictCursor)
            curseur.execute(requete, parametres)
            res : int = curseur.rowcount
            curseur.close()

            if res == 1:
                return True
            else:
                return False
        except:
            print("Pas de connexion")
        
    def recuperer_quantite_par_sachet(self, informations : dict[str,str|int]) -> int:
        """Récupère la quantité de graines par sachet d'une graine dans la base de données"""
        try:
            requete : str ="""
            SELECT quantite_graines_sachet
            FROM graine
            NATURAL JOIN famille
            NATURAL JOIN espece
            NATURAL JOIN variete
            NATURAL JOIN grainotheque
            WHERE nom_famille = %s
            AND nom_espece = %s
            AND nom_variete = %s
            AND nom_grainotheque = %s;
            """
            
            parametres : tuple[Any] = (
                informations["famille"],
                informations["espece"],
                informations["variete"],
                self.__nom_grainotheque
            )

            curseur : DictCursor = self.__connexion.cursor(DictCursor)
            curseur.execute(requete, parametres)
            res : tuple[dict[str, Any]] = curseur.fetchall()
            curseur.close()

            return res[0]["quantite_graines_sachet"]
        except:
            print("Pas de connexion")
    
    def rechercher_famille(self, informations : dict[str, str|int]) -> None:
        """Recherche une famille dans la BDD"""
        try:
            requete = """
            SELECT nom_famille
            FROM famille
            WHERE nom_famille = %s;
            """

            parametres : tuple[Any] = (
                informations["famille"],
            )

            curseur : DictCursor = self.__connexion.cursor(DictCursor)
            curseur.execute(requete, parametres)
            res : tuple[dict[str, Any]] = curseur.rowcount
            curseur.close()

            if res == 1:
                return True
            else:
                return False
        except:
            print("Pas de connexion")
    
    def ajouter_famille(self, informations : dict[str, str|int]) -> None:
        """Ajoute une famille dans la BDD"""
        try:
            if not self.rechercher_famille(informations):
                requete = """
                INSERT INTO famille (nom_famille)
                VALUES (%s);
                """
                parametres : tuple[Any] = (informations['famille'],)

                curseur : DictCursor = self.__connexion.cursor(DictCursor)
                curseur.execute(requete, parametres)
                self.__connexion.commit()
                curseur.close()
        except:
            print("Pas de connexion")

    def rechercher_espece(self, informations : dict[str, str|int]) -> None:
        """Recherche une esoèce dans la BDD"""
        try:
            requete = """
            SELECT nom_espece
            FROM espece
            NATURAL JOIN famille
            WHERE nom_espece = %s
            AND nom_famille = %s;
            """

            parametres : tuple[Any] = (
                informations["espece"],
                informations['famille']
            )

            curseur : DictCursor = self.__connexion.cursor(DictCursor)
            curseur.execute(requete, parametres)
            res : tuple[dict[str, Any]] = curseur.rowcount
            curseur.close()

            if res == 1:
                return True
            else:
                return False
        except:
            print("Pas de connexion")

    def ajouter_espece(self, informations : dict[str, str|int]) -> None:
        """Ajoute une espèce dans la BDD"""
        try:
            if not self.rechercher_espece(informations):
                requete = """
                INSERT INTO espece (nom_espece, id_famille)
                VALUES (
                    %s,
                    (SELECT id_famille FROM famille WHERE nom_famille = %s)
                )
                """

                parametres : tuple[Any] = (
                    informations["espece"],
                    informations["famille"]
                )

                curseur : DictCursor = self.__connexion.cursor(DictCursor)
                curseur.execute(requete, parametres)
                self.__connexion.commit()
                curseur.close()
        except:
            print("Pas de connexion")

    def rechercher_variete(self, informations : dict[str, str|int]) -> None:
        """Recherche d'une variété dans la BDD"""
        try:
            requete = """
            SELECT nom_variete
            FROM variete
            NATURAL JOIN espece
            NATURAL JOIN famille
            WHERE nom_variete = %s
            AND nom_espece = %s
            AND nom_famille = %s;
            """

            parametres : tuple[Any] = (
                informations["variete"],
                informations["espece"],
                informations['famille']
            )

            curseur : DictCursor = self.__connexion.cursor(DictCursor)
            curseur.execute(requete, parametres)
            res : tuple[dict[str, Any]] = curseur.rowcount
            curseur.close()

            if res == 1:
                return True
            else:
                return False
        except:
            print("Pas de connexion")
        
    def ajouter_variete(self, informations : dict[str, str|int]) -> None:
        """Ajoute une variété dans la BDD"""
        try:
            if not self.rechercher_variete(informations):
                requete = """
                INSERT INTO variete (nom_variete, id_espece)
                VALUES (
                    %s,
                    (   SELECT id_espece
                        FROM espece
                        NATURAL JOIN famille
                        WHERE nom_espece = %s
                        AND nom_famille = %s
                    )
                )
                """

                parametres : tuple[Any] = (
                    informations["variete"],
                    informations["espece"],
                    informations["famille"]
                )

                curseur : DictCursor = self.__connexion.cursor(DictCursor)
                curseur.execute(requete, parametres)
                self.__connexion.commit()
                curseur.close()
        except:
            print("Pas de connexion")
    
    def __del__(self):
        """Actions à la destruction"""
        try:
            self.__connexion.close()
        except:
            pass

# ----- PROGRAMME -----
if __name__ == "__main__":
    bdd = BDDGrainotheque("Centre Social et Socioculturel du Chemillois")
    
    informations : dict[str, str] = {
        "famille" : "Solanacées",
        "espece" : "Tomate",
        "variete" : "Grappe"
    }

    print(bdd.recherche_graine(informations))

    #print(bdd.recuperer_quantite_par_sachet(informations))

    print(bdd.rechercher_famille(informations))
    bdd.ajouter_famille(informations)

    print(bdd.rechercher_espece(informations))
    bdd.ajouter_espece(informations)

    print(bdd.rechercher_variete(informations))
    bdd.ajouter_variete(informations)