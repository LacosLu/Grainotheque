# ----- IMPORTS -----
# --- Bibliothèques externes ---
import customtkinter as ctk

# ----- CLASSES -----
class Clavier:
    __buttons = [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
        ['q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm'],
        ['w', 'x', 'c', 'v', 'b', 'n', ',', ';', '.', '/'],
        ['é', 'è', 'ê', 'ë', 'à', 'ç', 'ù', '@', "'"],
        ['Space', '<--', 'Terminer']
    ]

    __largeur_bouttons : int = 150
    __hauteur_bouttons : int = 50

    __font : tuple = ("Baloo da 2", 25)

    def __init__(self, entree : ctk.CTkEntry):
        """Fenêtre de clavier avec tkinter"""
        self.__root : ctk.CTk = ctk.CTk()
        self.__root.title("Clavier")

        self.__entry : ctk.CTkEntry = entree

        self.__placement_bouttons()

    def __placement_bouttons(self) -> None:
        """Placement des bouttons du clavier
        """
        for row, keys in enumerate(Clavier.__buttons):
            for col, key in enumerate(keys):
                if key == 'Space':
                    button = ctk.CTkButton(self.__root,
                                           text=key,
                                           width=Clavier.__largeur_bouttons*2,
                                           height=Clavier.__hauteur_bouttons,
                                           font=Clavier.__font,
                                           command=self.__add_space)
                    button.grid(row=row + 1, column=col, columnspan=3, padx=5, pady=5)
                elif key == '<--':
                    button = ctk.CTkButton(self.__root,
                                           text=key,
                                           width=Clavier.__largeur_bouttons*2,
                                           height=Clavier.__hauteur_bouttons,
                                           font=Clavier.__font,
                                           command=self.__backspace)
                    button.grid(row=row + 1, column=col+2, columnspan=3, padx=5, pady=5)
                elif key == "Terminer":
                    button = ctk.CTkButton(self.__root,
                                           text=key,
                                           width=Clavier.__largeur_bouttons*2,
                                           height=Clavier.__hauteur_bouttons,
                                           font=Clavier.__font,
                                           command=self.__terminer)
                    button.grid(row=row+1, column=col+4, columnspan=3, padx=5, pady=5)
                else:
                    button = ctk.CTkButton(self.__root,
                                           text=key,
                                           width=Clavier.__largeur_bouttons,
                                           height=Clavier.__hauteur_bouttons,
                                           font=Clavier.__font,
                                           command=lambda key=key: self.__press(key))
                    button.grid(row=row + 1, column=col, padx=5, pady=5)

    def __press(self, key : str) -> None:
        """Action à réaliser si une touche du clavier est pressée

        :param key: caractère
        :type key: str
        """
        self.__entry.insert(ctk.END, key)

    def __backspace(self) -> None:
        """Action à réaliser en cas de suppression de caractère
        """
        current_text = self.__entry.get()
        self.__entry.delete(len(current_text) - 1, ctk.END)

    def __add_space(self) -> None:
        """Action à réaliser si la barre Espace est pressée
        """
        self.__entry.insert(ctk.END, " ")

    def __terminer(self) -> None:
        """Action à réaliser si l'utilisateur à terminer
        """
        self.__root.destroy()

    def run(self) -> None:
        """Lancement de la fenêtre
        """
        self.__root.mainloop()

# ----- PROGRAMME -----
if __name__ == "__main__":
    Clavier().run()