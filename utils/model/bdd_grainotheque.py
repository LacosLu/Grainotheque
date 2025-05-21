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

    def recherche_graine(self, informations : dict[str,str|int]) -> bool|None:
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
        
    def recuperer_graine(self, informations : dict[str,str|int]) -> dict:
        """Récupère la quantité de graines par sachet d'une graine dans la base de données"""
        try:
            requete : str ="""
            SELECT quantite_sachet
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
            res : tuple[dict[str, Any]] = curseur.fetchone()
            curseur.close()

            return res
        except:
            print("Pas de connexion")
    
    def rechercher_famille(self, informations : dict[str, str|int]) -> bool|None:
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

    def rechercher_espece(self, informations : dict[str, str|int]) -> bool | None:
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

    def rechercher_variete(self, informations : dict[str, str|int]) -> bool | None:
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

    def ajouter_graine(self, informations : dict[str, str|int]) -> None:
        try:
            requete : str = """
            INSERT INTO graine(quantite_sachet, quantite_graines_sachet, id_variete, id_grainotheque)
            VALUES (1,
                    %s,
                    (SELECT id_variete
                    FROM variete
                    NATURAL JOIN espece
                    NATURAL JOIN famille
                    WHERE nom_variete = %s
                    AND nom_espece = %s
                    AND nom_famille = %s),
                    (SELECT id_grainotheque
                    FROM grainotheque
                    WHERE nom_grainotheque = %s));
            """

            parametres : tuple[Any] = (
                informations["quantite_par_sachet"],
                informations["variete"],
                informations["espece"],
                informations["famille"],
                self.__nom_grainotheque
            )

            curseur : DictCursor = self.__connexion.cursor(DictCursor)
            curseur.execute(requete, parametres)
            self.__connexion.commit()
            curseur.close()
        except:
            raise LookupError("Grain déjà existente")

    def incrementer_graine(self, informations : dict[str, str|int]) -> None:
        requete : str = """
        UPDATE graine 
        SET quantite_sachet = quantite_sachet + 1 
        WHERE id_variete = (
            SELECT id_variete
            FROM variete
            NATURAL JOIN espece
            NATURAL JOIN famille
            WHERE nom_variete = %s
            AND nom_espece = %s
            AND nom_famille = %s
        )
        AND id_grainotheque = (
            SELECT id_grainotheque
            FROM grainotheque
            WHERE nom_grainotheque = %s
        );
        """

        parametres : tuple[Any] = (
            informations["variete"],
            informations["espece"],
            informations["famille"],
            self.__nom_grainotheque
        )

        curseur : DictCursor = self.__connexion.cursor(DictCursor)
        curseur.execute(requete, parametres)
        self.__connexion.commit()
        curseur.close()

    def rechercher_despositaire(self, informations : dict[str, str|int]) -> bool:
        requete : str = """
        SELECT *
        FROM depositaire
        WHERE nom_depositaire = %s
        AND email_depositaire = %s;
        """

        parametres : tuple[Any] = (
            informations["prenom_depositaire"],
            informations["email_depositaire"]
        )

        curseur : DictCursor = self.__connexion.cursor(DictCursor)
        curseur.execute(requete, parametres)
        res : tuple[dict[str, Any]] = curseur.rowcount
        curseur.close()

        if res == 1:
            return True
        else:
            return False
        
    def ajouter_depositaire(self, informations : dict[str, str|int]) -> None:
        requete : str = """
        INSERT INTO depositaire(nom_depositaire, email_depositaire)
        VALUES (%s, %s)
        """

        parametres : tuple[Any] = (
            informations["prenom_depositaire"],
            informations['email_depositaire']
        )

        curseur : DictCursor = self.__connexion.cursor(DictCursor)
        curseur.execute(requete, parametres)
        self.__connexion.commit()
        curseur.close()

    def ajouter_depot(self, informations : dict[str, str|int]) -> None:
        requete : str = """
        INSERT INTO depot(date_depot, date_recolte, quantite_graine,id_depositaire,id_variete, observations)
        VALUES (%s,
                %s,
                %s,
                (SELECT id_depositaire
                FROM depositaire
                WHERE nom_depositaire = %s
                AND email_depositaire = %s),
                (SELECT id_variete
                FROM variete
                NATURAL JOIN espece
                NATURAL JOIN famille
                WHERE nom_variete = %s
                AND nom_espece = %s
                AND nom_famille = %s),
                %s);
        """
        
        parametres : tuple[Any] = (
            informations["date_depot"],
            informations["date_recolte"],
            informations["quantite_graine"],
            informations["prenom_depositaire"],
            informations["email_depositaire"],
            informations["variete"],
            informations["espece"],
            informations["famille"],
            informations["observations"]
        )

        curseur : DictCursor = self.__connexion.cursor(DictCursor)
        curseur.execute(requete, parametres)
        self.__connexion.commit()
        curseur.close()
    
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
        "variete" : "Grappe",
        "quantite_par_sachet" : 20,
        "prenom_depositaire" : "Luka",
        "email_depositaire" : "luka@gmail.com",
        "date_depot" : "2025-04-28",
        "date_recolte" : "2025-04-27",
        "quantite_graine" : 15,
        "observations" : "Observations"
    }

    """print(bdd.recherche_graine(informations))

    #print(bdd.recuperer_quantite_par_sachet(informations))

    print(bdd.rechercher_famille(informations))
    bdd.ajouter_famille(informations)

    print(bdd.rechercher_espece(informations))
    bdd.ajouter_espece(informations)

    print(bdd.rechercher_variete(informations))
    bdd.ajouter_variete(informations)"""

    #bdd.ajouter_graine(informations)
    #bdd.incrementer_graine(informations)

    if not bdd.rechercher_despositaire(informations):
        bdd.ajouter_depositaire(informations)

    bdd.ajouter_depot(informations)