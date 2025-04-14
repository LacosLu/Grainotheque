# ----- IMPORTS -----
# --- Bibliothèques externes ---
import customtkinter as ctk

# --- Bibliothèques internes ---
from ..view import *
from ..model import *

# ----- CLASSES -----
class ControleurGrainotheque:
    def __init__(self, nom_grainotheque : str = "Centre Social et Socioculturel du Chemillois") -> None:
        """Contrôleur de l'application pour la station d'identification"""
        # --- Attributs ---
        self.__informations : dict[str, str|int] = {}

        # --- Initialisation des models ---
        self.__bdd : BDDGrainotheque = BDDGrainotheque(nom_grainotheque)
        self.__app_qr : ApplicationQR = ApplicationQR()

        # --- Initialisation des vues ---
        self.__accueil : Accueil = Accueil()
        self.__depot : Depot
        self.__retrait : Retrait
        self.__qr : QR

        # -- Bouttons de la vue d'accueil --
        self.__accueil._bouttons["recherche"].configure(command=self.__recherche)
        self.__accueil._bouttons["scan"].configure(command=self.__scan)

        # --- Lancement ---
        self.__accueil.run()

    def __recherche(self) -> None:
        """Recherche de la graine dans la base de données"""
        # --- Récupération des champs qui serviront pour la requête ---
        for key, object in self.__accueil._champs_entrees.items():
            self.__informations[key] = object.get().capitalize()

        # --- Besoin de réaliser la requête dans le modèle ---
        if self.__bdd.recherche_graine(self.__informations) :
            quantite_par_sachet : int = self.__bdd.recuperer_quantite_par_sachet(self.__informations)
        else :
            quantite_par_sachet : str = "Nouvelle graine"
        
        # --- Ajout de la quantité ---
        self.__informations["quantite_par_sachet"] = quantite_par_sachet

        # --- Création d'une nouvelle page pour le dépôt ---
        self.__depot : Depot = Depot(self.__informations)

        # --- Bouttons de cette nouvelle vue ---
        self.__depot._bouttons["nb_graines"].configure(command=self.__association_comptage_vue)
        self.__depot._bouttons["validation"].configure(command=self.__validation_depot)
        self.__depot._bouttons["annulation"].configure(command=self.__annuler_depot)

        # --- Lancement de la vue ---
        self.__depot.run()

    def __validation_depot(self) -> None:
        """Fonction de validation du dépôt"""
        # --- Récupération des entrées ---
        for key, object in self.__depot._champs_entrees.items():
            if key == "observations":
                self.__informations[key] = object.get("1.0", ctk.END)
            else:
                self.__informations[key] = object.get()
        self.__informations["prenom_depositaire"].capitalize()

        # --- Création du QR ---
        self.__qrcode : str = self.__app_qr._qr.creation_qrcode(self.__informations)

        # --- Génération de la page ---
        self.__qr : QR = QR()

        # --- Bouttons de la vue ---
        self.__qr._bouttons["impression"].configure(command=self.__imprimer_qr)
        self.__qr._bouttons["annulation"].configure(command=self.__annuler_impression)
        
        # --- Lancement de la vue ---
        self.__qr.run()

    def __imprimer_qr(self) -> None:
        """Impression du qr code"""
        self.__app_qr._imprimante.impretion_qrcode(self.__qrcode)
        self.__qr.fermer()
        self.__depot.fermer()

    def __annuler_impression(self) -> None:
        """Annulation de l'impression"""
        self.__qr.fermer()

    def __association_comptage_vue(self) -> None:
        """Méthode qui va faire le lien entre le compte de graines dans le modèle et le renvoie du résultat dans la vue"""
        Camera.photographier()

        compte_graines : int = ComptageGraines.comptage_contours()

        self.__depot._nb_graines.configure(text=compte_graines)

        print("Comptage")

    def __annuler_depot(self) -> None:
        """Méthode qui va annuler le depot"""
        self.__depot.fermer()

    def __scan(self) -> None:
        """Scan du QR code mis sous la caméra"""
        # --- Récupération des données du QR code dans le modèle et dans la base de données ---
        # -- Prise de photo --
        try:
            Camera.photographier("qr")
        except:
            print("Pas de caméra")

        # -- Récupération des informations du QR code --
        print(self.__app_qr._qr.lecture_qrcode())

        # --- Mise des informations dans un dictionnaire ---
        self.__informations : dict[str, str|int] = {
            "famille" : "famille",
            "espece" : "espece",
            "variete" : "variete",
            "quantite_par_sachet" : 20,
            "date_recolte" : "17/03/2025",
            "prenom_depositaire" : "Luka",
            "email_depositaire" : "toto@titi.com",
            "date_depot" : "18/03/2025",
            "nb_graines" : 400,
            "observations" : "Franchement je sais aps\noui",
            "quantite_sachets" : 20
        }

        # --- Génération de la page ---
        self.__retrait : Retrait = Retrait(self.__informations)

        # --- Bouttons de la vue ---
        self.__retrait._bouttons["validation"].configure(command=self.__validation_retrait)

        # --- Lancement de la vue ---
        self.__retrait.run()

    def __validation_retrait(self) -> None:
        """Validation du retrait"""
        self.__app_qr._retrait.mise_à_jour_bdd()
        self.__retrait.fermer()