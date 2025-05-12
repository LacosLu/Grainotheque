# ----- IMPORTS -----
# --- Bibliothèques externes ---
import customtkinter as ctk

# --- Bibliothèques internes ---
if __name__ == "__main__":
    from base import Base
else:
    from .base import Base

# ----- CLASSES -----
class Alert(Base):
    def __init__(self, text : str) -> None:
        """Accueil de l'application de la station d'identification"""
        super().__init__()

        self._initialiser_champs(text)

    def _initialiser_champs(self, text : str = "") -> None:
        """Initialise les champs de la page"""
        # Entrée pour la famille
        alert = ctk.CTkLabel(self._canva,
                               text=text,
                               width=self._largeur_items,
                               font=self._font,
                               height=self._hauteur_items)
        alert.pack(padx=50, pady=5)

        # Champ vide afin de faire un espace entre les entrées et les bouttons
        vide = ctk.CTkLabel(self._canva, text="")
        vide.pack()

        # Boutton de recherche de la graine
        valider = ctk.CTkButton(self._canva,
                                  text="Valider",
                                  fg_color="green",
                                  hover_color="darkgreen",
                                  width=self._largeur_items,
                                  font=self._font,
                                  height=self._hauteur_items)
        valider.pack(padx=50, pady=5)
        self._bouttons["validation"] = valider

        # Boutton de scan d'un QR code
        annulation = ctk.CTkButton(self._canva,
                             text="Annuler",
                             fg_color="red",
                             hover_color="darkred",
                             width=self._largeur_items,
                             font=self._font,
                             height=self._hauteur_items)
        annulation.pack(padx=50, pady=5)
        self._bouttons["annulation"] = annulation

# ----- PROGRAMME -----
if __name__ == "__main__":
    Alert("oui").run()