# ----- IMPORTS -----
# --- Biblitohèques externes ---
import customtkinter as ctk
import datetime

# --- Bibliothèques internes ---
try:
    from base import Base
except:
    from .base import Base

# ----- CLASSES -----
class Depot(Base):
    def __init__(self, informations : dict[str, str|int]) -> None:
        """Page de l'application de la station où la graine est existante dans la base de données"""
        super().__init__()

        self._initialiser_champs(informations)

    def _initialiser_champs(self, informations : dict[str, str|int]) -> None:
        # Famille
        famille : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                              text=informations["famille"],
                                              width=self._largeur_items,
                                              height=self._hauteur_items,
                                              font=self._font,
                                              justify=ctk.LEFT)
        famille.grid(column=0, row=0, padx=5, pady=5)

        # Espèce
        espece : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                             text=informations["espece"],
                                             width=self._largeur_items,
                                             height=self._hauteur_items,
                                             font=self._font,
                                             justify=ctk.LEFT)
        espece.grid(column=0, row=1, padx=5, pady=5)

        # Variété
        variete : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                              text=informations["variete"],
                                              width=self._largeur_items,
                                              height=self._hauteur_items,
                                              font=self._font,
                                              justify=ctk.LEFT)
        variete.grid(column=0, row=2, padx=5, pady=5)

        # Quantité
        self._quantite_par_sachet : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                          text=informations["quantite_par_sachet"],
                                                          width=self._largeur_items,
                                                          height=self._hauteur_items,
                                                          font=self._font,
                                                          justify=ctk.LEFT)
        self._quantite_par_sachet.grid(column=0, row=3, padx=5, pady=5)

        # Date de récolte
        date_recolte : ctk.CTkEntry = ctk.CTkEntry(self._canva,
                                                   placeholder_text="Date de récolte",
                                                   width=self._largeur_items,
                                                   font=self._font,
                                                   height=self._hauteur_items)
        date_recolte.grid(column=1, row=0, padx=5, pady=5)
        date_recolte.bind("<1>", lambda event: Base.ouvrir_clavier(event, date_recolte))
        self._champs_entrees['date_recolte'] = date_recolte

        # Prénom du dépositaire
        prenom_depositaire : ctk.CTkEntry = ctk.CTkEntry(self._canva,
                                                         placeholder_text="Prénom du dépositaire",
                                                         width=self._largeur_items,
                                                         font=self._font,
                                                         height=self._hauteur_items)
        prenom_depositaire.grid(column=1, row=1, padx=5, pady=5)
        prenom_depositaire.bind("<1>", lambda event: Base.ouvrir_clavier(event, prenom_depositaire))
        self._champs_entrees['prenom_depositaire'] = prenom_depositaire

        # E-mail du dépositaire
        email_depositaire : ctk.CTkEntry = ctk.CTkEntry(self._canva,
                                                        placeholder_text='E-mail du dépositaire',
                                                        width=self._largeur_items,
                                                        font=self._font,
                                                        height=self._hauteur_items)
        email_depositaire.grid(column=1, row=2, padx=5, pady=5)
        email_depositaire.bind("<1>", lambda event: Base.ouvrir_clavier(event, email_depositaire))
        self._champs_entrees['email_depositaire'] = email_depositaire
        
        # Date du dépôt
        date_depot : ctk.CTkEntry = ctk.CTkLabel(self._canva,
                                                 text=datetime.date.today(),
                                                 width=self._largeur_items,
                                                 font=self._font,
                                                 height=self._hauteur_items)
        date_depot.grid(column=1, row=3, padx=5, pady=5)

        # Nombre de graines
        self._nb_graines : ctk.CTkLabel = ctk.CTkLabel(self._canva,
                                                       text="Nombre de graines",
                                                       width=self._largeur_items,
                                                       height=self._hauteur_items,
                                                       font=self._font,
                                                       justify=ctk.LEFT)
        self._nb_graines.grid(column=0, row=4, padx=5, pady=5)

        # Boutton d'action de compte du nombre de graines
        compte_nb_graines : ctk.CTkButton = ctk.CTkButton(self._canva,
                                                          text="Compter nombre de graines",
                                                          width=self._largeur_items,
                                                          font=self._font,
                                                          height=self._hauteur_items)
        compte_nb_graines.grid(column=1, row=4, padx=5, pady=5)
        self._bouttons["nb_graines"] = compte_nb_graines

        # Champ des observations
        observations : ctk.CTkTextbox = ctk.CTkTextbox(self._canva,
                                                       width=self._largeur_items*2,
                                                       font=self._font)
        observations.grid(column=0, columnspan=2, row=5, rowspan=3, padx=5, pady=5)
        observations.bind("<1>", lambda event: Base.ouvrir_clavier(event, observations))
        self._champs_entrees['observations'] = observations

        # Boutton de validation
        validation : ctk.CTkButton = ctk.CTkButton(self._canva,
                                                   text="Valider",
                                                   width=self._largeur_items*2,
                                                   font=self._font,
                                                   height=self._hauteur_items)
        validation.grid(column=0, columnspan=2, row=8, padx=5, pady=5)
        self._bouttons["validation"] = validation

        # Boutton d'annulation
        annulation : ctk.CTkButton = ctk.CTkButton(self._canva,
                                                   text="Annuler",
                                                   width=self._largeur_items*2,
                                                   height=self._hauteur_items,
                                                   font=self._font,
                                                   fg_color="red",
                                                   hover_color="darkred")
        annulation.grid(column=0, columnspan=2, row=9, padx=5, pady=5)
        self._bouttons["annulation"] = annulation

# ----- PROGRAMME -----
if __name__ == "__main__":
    Depot("oui", "non", "peut-être", "20").run()