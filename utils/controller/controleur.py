# ----- IMPORTS -----
# --- Bibliothèques externes ---
import customtkinter as ctk
import datetime
import re

# --- Bibliothèques internes ---
from ..view import *
from ..model import *
from ..deep_learning import *

# ----- CLASSES -----
class ControleurGrainotheque:
    # --- Constantes ---
    AT_CHIFFRES : list[str] = ["@","1","2","3","4","5","6","7","8","9"]
    REGEX : str = "^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$"

    def __init__(self, nom_grainotheque : str = "Centre Social et Socioculturel du Chemillois") -> None:
        """Contrôleur de l'application pour la station d'identification"""
        # --- Attributs ---
        self.__informations : dict[str, str|int] = {}

        # --- Initialisation des models ---
        self.__bdd : BDDGrainotheque = BDDGrainotheque(nom_grainotheque)
        self.__app_qr : ApplicationQR = ApplicationQR(nom_grainotheque)
        self.__comptage : CompterGraines = CompterGraines()

        # --- Initialisation des vues ---
        self.__accueil : Accueil = Accueil()
        self.__depot : Depot
        self.__retrait : Retrait
        self.__qr : QR
        self.__alert : Alert

        # -- Bouttons de la vue d'accueil --
        self.__accueil._bouttons["recherche"].configure(command=self.__recherche)
        self.__accueil._bouttons["scan"].configure(command=self.__scan)
        self.__accueil._bouttons["fermer"].configure(command=self.__accueil.fermer)

        # --- Lancement ---
        self.__accueil.run()

    def __recherche(self) -> None:
        """Recherche de la graine dans la base de données"""
        # --- Récupération des champs qui serviront pour la requête ---
        self.__informations["famille"] = self.__accueil._famille.get()
        for key, object in self.__accueil._champs_entrees.items():
            self.__informations[key] = object.get().capitalize()
            for carac in ControleurGrainotheque.AT_CHIFFRES:
                if carac in self.__informations[key]:
                    self.__alert : Alert = Alert(f"Erreur de saisie : {key}. \n Veuillez réessayer")

                    self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
                    self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)
                    return

        # --- Besoin de réaliser la requête dans le modèle ---
        if self.__bdd.recherche_graine(self.__informations) :
            quantite_par_sachet : int = self.__bdd.recuperer_graine(self.__informations)["quantite_graines_sachet"]
        else :
            quantite_par_sachet : str = "Nouvelle graine"
        
        # --- Ajout de la quantité ---
        self.__informations["quantite_par_sachet"] = quantite_par_sachet

        # --- Création d'une nouvelle page pour le dépôt ---
        self.__depot : Depot = Depot(self.__informations)

        # --- Bouttons de cette nouvelle vue ---
        self.__depot._bouttons["nb_graines"].configure(command=self.__association_comptage_vue)
        self.__depot._bouttons["validation"].configure(command=self.__validation_depot)
        self.__depot._bouttons["annulation"].configure(command=self.__depot.fermer)

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
        
        for carac in ControleurGrainotheque.AT_CHIFFRES:
            if carac in self.__informations["prenom_depositaire"]:
                self.__alert : Alert = Alert("Erreur sur le prénom. \n Veuillez réessayer")

                self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
                self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)
                return

        if not re.search(ControleurGrainotheque.REGEX, self.__informations["email_depositaire"]):
            self.__alert : Alert = Alert("Erreur sur le mail. \n Veuillez réessayer")

            self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
            self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)
            return

        self.__informations["prenom_depositaire"].capitalize()
        self.__informations["date_recolte"] = self.__depot._date_recolte.get_date()
        self.__informations["quantite_par_sachet"] = self.__depot._quantite_par_sachet.cget("text")

        try:
            self.__informations["quantite_graine"] = int(self.__depot._nb_graines.cget("text"))

            # --- Création du QR ---
            try:
                self.__qrcode : str = self.__app_qr._qr.creation_qrcode(self.__informations)

                # --- Génération de la page ---
                self.__qr : QR = QR()

                # --- Bouttons de la vue ---
                self.__qr._bouttons["impression"].configure(command=self.__imprimer_qr)
                self.__qr._bouttons["annulation"].configure(command=self.__qr.fermer)
                
                # --- Lancement de la vue ---
                self.__qr.run()
            except:
                self.__alert : Alert = Alert("Erreur de création du QR code. \n Veuillez réessayer")

                self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
                self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)
        except:
            self.__alert : Alert = Alert("Calcul des graines non fait. \n Veuillez réessayer")

            self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
            self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)

    def __imprimer_qr(self) -> None:
        """Impression du qr code"""
        # --- Requête famille ---
        if not self.__bdd.rechercher_famille(self.__informations):
            self.__bdd.ajouter_famille(self.__informations)

        # --- Requête espèce ---
        if not self.__bdd.rechercher_espece(self.__informations):
            self.__bdd.ajouter_espece(self.__informations)

        # --- Requête variété ---
        if not self.__bdd.rechercher_variete(self.__informations):
            self.__bdd.ajouter_variete(self.__informations)

        # --- Requête graine ---
        if not self.__bdd.recherche_graine(self.__informations):
            self.__bdd.ajouter_graine(self.__informations)
        else:
            nb_sachets : int = round(self.__informations["quantite_graine"]/self.__informations["quantite_par_sachet"],0)
            for i in range(nb_sachets):
                self.__bdd.incrementer_graine(self.__informations)
            if nb_sachets == 0:
                self.__bdd.incrementer_graine(self.__informations)

        # --- Requête dépositaire ---
        if not self.__bdd.rechercher_despositaire(self.__informations):
            self.__bdd.ajouter_depositaire(self.__informations)

        # --- Requête dépôt ---
        self.__bdd.ajouter_depot(self.__informations)

        # --- Fin de fonction ---
        try:
            self.__app_qr._imprimante.impretion_qrcode(self.__qrcode)
            self.__qr.fermer()
            self.__depot.fermer()
        except:
            self.__alert : Alert = Alert("Erreur d'impression du QR code. \n Veuillez réessayer")

            self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
            self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)

    def __association_comptage_vue(self) -> None:
        """Méthode qui va faire le lien entre le compte de graines dans le modèle et le renvoie du résultat dans la vue"""
        self.__alert = Alert("Déposez qu'une seule graine")

        self.__alert._bouttons["validation"].configure(command=self.__prendre_photo_taille)
        self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)

    def __prendre_photo_taille(self) -> None:
        """Prend une photo, l'enregistre sous le nom de img_taille et continuer la procédure de comptage"""
        try:
            Camera.photographier("img_taille")

            self.__alert.fermer()

            self.__alert = Alert("Déposez le reste des graines à plat")

            self.__alert._bouttons["validation"].configure(command=self.__prendre_photo_compter_graines)
            self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)
        except:
            self.__alert : Alert = Alert("Erreur de prise de photo. \n Veuillez réessayer")

            self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
            self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)

    def __prendre_photo_compter_graines(self) -> None:
        """Prend la photo de toutes les graines et les comptes"""
        try:
            Camera.photographier()

            self.__alert.fermer()

            nb_graines_par_sachet, compte_graines = self.__comptage.compter_graines()

            self.__depot._nb_graines.configure(text=compte_graines)
            if self.__depot._quantite_par_sachet._text == "Nouvelle graine":
                self.__depot._quantite_par_sachet.configure(text=nb_graines_par_sachet)
        except:
            self.__alert : Alert = Alert("Erreur de prise de photo. \n Veuillez réessayer")

            self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
            self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)

    def __scan(self) -> None:
        """Scan du QR code mis sous la caméra"""
        # --- Récupération des données du QR code dans le modèle et dans la base de données ---
        # -- Prise de photo --
        try:
            Camera.photographier("qr")
        except:
            self.__alert : Alert = Alert("Erreur de prise de photo. \n Veuillez réessayer")

            self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
            self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)

        # -- Récupération des informations du QR code --
        try:
            self.__informations = self.__app_qr._qr.lecture_qrcode()
        except:
            self.__alert : Alert = Alert("Erreur de lecture de QR code. \n Veuillez réessayer")

            self.__alert._bouttons["validation"].configure(command=self.__alert.fermer)
            self.__alert._bouttons["annulation"].configure(command=self.__alert.fermer)

        # --- Requête pour récupérer les informations supplémentaires ---
        info_graines : dict = self.__bdd.recuperer_graine(self.__informations)
        self.__informations["quantite_sachets"] = info_graines["quantite_sachet"]
        self.__informations["nb_graines"] = int(self.__informations["quantite_sachets"])*int(self.__informations["quantite_par_sachet"])

        # --- Génération de la page ---
        self.__retrait : Retrait = Retrait(self.__informations)

        # --- Bouttons de la vue ---
        self.__retrait._bouttons["validation"].configure(command=self.__validation_retrait)
        self.__retrait._bouttons["annulation"].configure(command=self.__retrait.fermer)

        # --- Lancement de la vue ---
        self.__retrait.run()

    def __validation_retrait(self) -> None:
        """Validation du retrait"""
        self.__app_qr._retrait.mise_à_jour_bdd(self.__informations)
        self.__retrait.fermer()