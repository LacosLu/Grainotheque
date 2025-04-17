# ----- IMPORTS -----
# --- Bibliothèques externes ---
import customtkinter as ctk

# --- Bibliothèques internes ---
if __name__ == "__main__":
    from base import Base
else:
    from .base import Base

# ----- CLASSES -----
class Accueil(Base):
    def __init__(self) -> None:
        """Accueil de l'application de la station d'identification"""
        super().__init__()

        self._initialiser_champs()

    def _initialiser_champs(self) -> None:
        """Initialise les champs de la page"""
        # Entrée pour la famille
        famille = ctk.CTkEntry(self._canva,
                               placeholder_text='Famille',
                               width=self._largeur_items,
                               font=self._font,
                               height=self._hauteur_items)
        famille.pack(padx=50, pady=5)
        famille.bind("<1>", lambda event: Base.ouvrir_clavier(event, famille))
        self._champs_entrees['famille'] = famille

        # Entrée pour l'espèce
        espece = ctk.CTkEntry(self._canva,
                              placeholder_text="Espèce",
                              width=self._largeur_items,
                              font=self._font,
                              height=self._hauteur_items)
        espece.pack(padx=50, pady=5)
        espece.bind("<1>", lambda event: Base.ouvrir_clavier(event, espece))
        self._champs_entrees['espece'] = espece

        # Entrée pour la variété
        variete = ctk.CTkEntry(self._canva,
                               placeholder_text='Variété',
                               width=self._largeur_items,
                               font=self._font,
                               height=self._hauteur_items)
        variete.pack(padx=50, pady=5)
        variete.bind("<1>", lambda event: Base.ouvrir_clavier(event, variete))
        self._champs_entrees["variete"] = variete

        # Champ vide afin de faire un espace entre les entrées et les bouttons
        vide = ctk.CTkLabel(self._canva, text="")
        vide.pack()

        # Boutton de recherche de la graine
        recherche = ctk.CTkButton(self._canva,
                                  text="Rechercher",
                                  width=self._largeur_items,
                                  font=self._font,
                                  height=self._hauteur_items)
        recherche.pack(padx=50, pady=5)
        self._bouttons["recherche"] = recherche

        # Boutton de scan d'un QR code
        scan = ctk.CTkButton(self._canva,
                             text="Scanner un QR code",
                             fg_color="green",
                             hover_color="darkgreen",
                             width=self._largeur_items,
                             font=self._font,
                             height=self._hauteur_items)
        scan.pack(padx=50, pady=5)
        self._bouttons["scan"] = scan

# ----- PROGRAMME -----
if __name__ == "__main__":
    Accueil().run()