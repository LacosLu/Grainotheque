# ----- IMPROTS -----
# --- Bibliothèques externes ---
from abc import abstractmethod
import customtkinter as ctk

# --- Bibliothèques internes ---
try:
    from clavier import Clavier
except:
    from .clavier import Clavier

# ----- CLASSES -----
class Base:
    def __init__(self) -> None:
        """Base des pages de l'application de la grainothèque"""
        # Création et nommage de la fenêtre
        self._root = ctk.CTk()
        self._root.title("Grainothèque")
        
        # Détermination de la taille et mise en non redimensionnable
        largeur, hauteur = self._root.winfo_screenwidth(), self._root.winfo_screenheight()
        self._root.geometry("%dx%d+0+0" % (largeur, hauteur))
        self._root.resizable(False, False)

        # Création du canva centré des données
        self._canva = ctk.CTkCanvas(self._root)
        self._canva.place(relx=0.5, rely=0.5, anchor="center")

        # Paramétrage de la taille d'un champ
        self._largeur_items : int = 400
        self._hauteur_items : int = 60
        self._font : tuple = ("Baloo da 2", 20)

        # Listes des éléments de la page
        self._champs_entrees : dict[str,ctk.CTkEntry] = {}
        self._bouttons : dict[str,ctk.CTkButton] = {}

    @staticmethod
    def ouvrir_clavier(event, entree : ctk.CTkEntry) -> None:
        """Fonction d'ouverture du clavier tactile"""
        sortie = Clavier(entree)
        print(sortie)

    @abstractmethod
    def _initialiser_champs(self) -> None:
        """Initialise les champs de la page"""
        pass

    def fermer(self) -> None:
        """Ferme la fenêtre"""
        self._root.destroy()

    def run(self) -> None:
        """Lancer l'application"""
        self._root.mainloop()

# ----- PROGRAMME -----
if __name__ == "__main__":
    Base().run()