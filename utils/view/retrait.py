# ----- IMPORTS -----
# --- Biblitohèques externes ---
import customtkinter as ctk

# --- Bibliothèques internes ---
try:
    from base import Base
except:
    from .base import Base

# ----- CLASSES -----
class Retrait(Base):
    def __init__(self, informations : dict[str, str|int]) -> None:
        """Page de l'application de la station où la graine est existante dans la base de données"""
        super().__init__()

        self._initialiser_champs(informations)

    def _initialiser_champs(self, infos : dict[str, str|int]) -> None:
        # Famille
        famille : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                              text=infos["famille"],
                                              width=self._largeur_items,
                                              height=self._hauteur_items,
                                              font=self._font,
                                              justify=ctk.LEFT)
        famille.grid(column=0, row=0, padx=5, pady=5)

        # Espèce
        espece : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                             text=infos["espece"],
                                             width=self._largeur_items,
                                             height=self._hauteur_items,
                                             font=self._font,
                                             justify=ctk.LEFT)
        espece.grid(column=0, row=1, padx=5, pady=5)

        # Variété
        variete : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                              text=infos["variete"],
                                              width=self._largeur_items,
                                              height=self._hauteur_items,
                                              font=self._font,
                                              justify=ctk.LEFT)
        variete.grid(column=0, row=2, padx=5, pady=5)

        # Quantité
        quantite_par_sachet : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                          text=infos["quantite_par_sachet"],
                                                          width=self._largeur_items,
                                                          height=self._hauteur_items,
                                                          font=self._font,
                                                          justify=ctk.LEFT)
        quantite_par_sachet.grid(column=0, row=3, padx=5, pady=5)

        # Date de récolte
        date_recolte : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                   text=infos["date_recolte"],
                                                   width=self._largeur_items,
                                                   height=self._hauteur_items,
                                                   font=self._font,
                                                   justify=ctk.LEFT)
        date_recolte.grid(column=1, row=0, padx=5, pady=5)

        # Prénom du dépositaire
        if "prenom_depositaire" in infos.keys():
            text : str = infos["prenom_depositaire"]
        else:
            text : str = "Prénom du dépositaire non disponible"
        prenom_depositaire : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                         text=text,
                                                         width=self._largeur_items,
                                                         height=self._hauteur_items,
                                                         font=self._font,
                                                         justify=ctk.LEFT)
        prenom_depositaire.grid(column=1, row=1, padx=5, pady=5)

        # E-mail du dépositaire
        if "email_depositaire" in infos.keys():
            text : str = infos["email_depositaire"]
        else:
            text : str = "E-mail du dépositaire non disponible"
        email_depositaire : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                        text=text,
                                                        width=self._largeur_items,
                                                        height=self._hauteur_items,
                                                        font=self._font,
                                                        justify=ctk.LEFT)
        email_depositaire.grid(column=1, row=2, padx=5, pady=5)
        
        # Date du dépôt
        if "date_depot" in infos.keys():
            text : str = infos["date_depot"]
        else:
            text : str = "Date du dépot non disponible"
        date_depot : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                 text=text,
                                                 width=self._largeur_items,
                                                 height=self._hauteur_items,
                                                 font=self._font,
                                                 justify=ctk.LEFT)
        date_depot.grid(column=1, row=3, padx=5, pady=5)

        # Nombre de graines
        if "nb_graines" in infos.keys():
            text : str = infos["nb_graines"]
        else:
            text : str = "Nombre de graines non disponible"
        nb_graines : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                 text=text,
                                                 width=self._largeur_items,
                                                 height=self._hauteur_items,
                                                 font=self._font,
                                                 justify=ctk.LEFT)
        nb_graines.grid(column=1, row=4, padx=5, pady=5)

        # Boutton de validation
        validation : ctk.CTkButton = ctk.CTkButton(self._canva,
                                                   text="Valider",
                                                   width=self._largeur_items*2,
                                                   font=self._font,
                                                   height=self._hauteur_items)
        validation.grid(column=0, columnspan=2, row=8, padx=5, pady=5)
        self._bouttons["validation"] = validation

        # Champ des observations
        if "observations" in infos.keys():
            text : str = infos["observations"]
        else:
            text : str = "Observations non disponible"
        observations : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                   text=text,
                                                   width=self._largeur_items*2,
                                                   font=self._font,
                                                   justify=ctk.LEFT)
        observations.grid(column=0, columnspan=2, row=5, rowspan=3, padx=5, pady=5)

        # Quantité de sachets
        if "quantite_sachets" in infos.keys():
            text : str = infos["quantite_sachets"]
        else:
            text : str = "Quantité de sachets non disponible"
        quantite_sachets : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                       text=text,
                                                       width=self._largeur_items,
                                                       height=self._hauteur_items,
                                                       font=self._font,
                                                       justify=ctk.LEFT)
        quantite_sachets.grid(column=0, row=4, padx=5, pady=5)