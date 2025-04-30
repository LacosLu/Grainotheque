# ----- IMPORTS -----
# --- Bibliothèques externes ---
import customtkinter as ctk
from tkinter import PhotoImage

# --- Bibliothèques internes ---
try:
    from base import Base
except:
    from .base import Base

# ----- CLASSES -----
class QR(Base):
    def __init__(self):
        """Page tkinter affichant le qr code"""
        super().__init__()

        self.__photo = PhotoImage(master= self._canva,file="./utils/temp/qr.png")

        self._initialiser_champs()

    def _initialiser_champs(self):
        """Initialisation des éléments de la page"""
        # QR code
        image : ctk.CTkLabel = ctk.CTkLabel(self._canva,text="", image=self.__photo)
        image.pack()

        # Bouton d'impression
        imprimer : ctk.CTkButton = ctk.CTkButton(self._canva,
                                                 text="Imprimer",
                                                 width=self._largeur_items,
                                                 height=self._hauteur_items,
                                                 font=self._font)
        imprimer.pack(padx=5, pady=5)
        self._bouttons["impression"] = imprimer

        # Boutton d'annulation
        annulation : ctk.CTkButton = ctk.CTkButton(self._canva,
                                                   text="Annuler",
                                                   width=self._largeur_items,
                                                   height=self._hauteur_items,
                                                   font=self._font,
                                                   fg_color="red",
                                                   hover_color="darkred")
        annulation.pack(padx=5, pady=5)
        self._bouttons["annulation"] = annulation