# ----- IMPORTS -----
# --- Bibliothèques internes ---
# -- Torch --
import torch
import torch.optim as optim
from torch.utils.data import DataLoader

# -- OpenCV --
import cv2 as cv

# --- Bibliothèques externes ---
try:
    from train_dl import TrainDL
    from dl_compte import Compte
    from datasets import ComptageGraines
except:
    from .train_dl import TrainDL
    from .dl_compte import Compte
    from .datasets import ComptageGraines

# ----- CLASSE -----
class TrainDLCompte(TrainDL):
    # --- Méthodes
    def __init__(self, net : str =""):
        """Classe d'entrainement de réseaux de neurones

        :param net: nom du model pré-entrainé, defaults to ""
        :type net: str, optional
        """
        super().__init__()
        # --- Model ---
        self._net : Compte = Compte()

        if net != "":
            self._net.load_state_dict(torch.load(f".\\models\\{net}", weights_only=False))

        # --- Fonction d'optimisation ---
        self._optimizer : optim.SGD = optim.SGD(self._net.parameters(), lr=1e-2)
                
    def _normalisation(self, dataset : ComptageGraines, rotation : int = None) -> list:
        """Fonction de normalisation du dataset

        :param dataset: Dataset
        :type dataset: ComptageGraines
        :param rotation: Si les images doivent être tournées, defaults to None
        :type rotation: int, optional
        :return: Liste des images normalisées
        :rtype: list
        """
        # - Chargement des images -
        if rotation == None:
            imgs = [torch.Tensor(cv.resize(img, (32,32))) for img,_ in dataset]
            imgs = torch.stack(imgs).type(torch.float32)
        else:
            imgs = [torch.Tensor(cv.rotate(cv.resize(img, (32,32)),rotation)) for img,_ in dataset]
            imgs = torch.stack(imgs).type(torch.float32)

        # - Normalisation -
        liste_norms = []
        for i in range(len(imgs)):
            liste_norms.append((self.norm(imgs[i].view((3,32,32))),i))

        return liste_norms

    def _chargement_donnees(self, noms_nombres_fichiers : list[tuple[str,int]]):
        """Chargement des photos d'entrainement

        :param noms_nombres_fichiers: Liste des répertoires avec leurs nombre de photos
        :type noms_nombres_fichiers: list[tuple[str,int]]
        """
        # --- Récupération des datasets ---
        datasets : list[ComptageGraines] = []
        for chemin, nb_photos in noms_nombres_fichiers:
            datasets.append(ComptageGraines(chemin, nb_photos))

        self._calcul_normalisation(datasets)

        # --- Normalisations ---
        datasets_norm : list = []
        for dataset in datasets:
            datasets_norm += self._normalisation(dataset)
            for rotation in TrainDL._rotations:
                datasets_norm += self._normalisation(dataset, rotation)

        self._train_dataload : DataLoader = DataLoader(datasets_norm, batch_size=1, shuffle=True)
        self._val_dataload : DataLoader = DataLoader(datasets_norm, batch_size=1, shuffle=False)

    def run(self, noms_nombres_fichiers, n_epochs, nom_model):
        self._chargement_donnees(noms_nombres_fichiers)
        super().run(noms_nombres_fichiers, n_epochs, nom_model)

# ----- PROGRAMME -----
if __name__ == "__main__":
    # -- Initialisation des éléments --
    rn_train = TrainDLCompte("compte_grosses_noirs.pt")

    # -- Lancement --
    # - Paramètres -
    repertoires : list[tuple[str,int]] = [
        ("grosses\\noirs",    74),
        ("grosses\\noirs2",   74),
        ("grosses\\noirs3",   74),
        ("grosses\\noirs4",   74)
        ]
    
    """Répertoires possibles :
    [
        ("grosses\\noirs",    74),
        ("grosses\\noirs2",   74),
        ("grosses\\noirs3",   74),
        ("grosses\\noirs4",   74)
        ]
    [
        ("grosses\\blanches",    74),
        ("grosses\\blanches2",   74),
        ("grosses\\blanches3",   74),
        ("grosses\\blanches4",   74)
        ]
    [
        ("moyennes\\noirs",    74),
        ("moyennes\\noirs2",   74),
        ("moyennes\\noirs3",   74),
        ("moyennes\\noirs4",   74)
        ]
    [
        ("moyennes\\blanches",    74),
        ("moyennes\\blanches2",   74),
        ("moyennes\\blanches3",   74),
        ("moyennes\\blanches4",   74)
        ]
    [
        ("petites\\noirs",    36),
        ("petites\\noirs2",   36),
        ("petites\\noirs3",   32),
        ("petites\\noirs4",   33)
        ]
    [
        ("petites\\blanches",    74),
        ("petites\\blanches2",   74),
        ("petites\\blanches3",   74),
        ("petites\\blanches4",   74)
        ]
    """

    nb_epochs : int = 1_000
    model_name : str = "compte_grosses_noirs"

    # - run -
    rn_train.run(repertoires, nb_epochs, model_name)

    # -- Test --
    chemin : str = ".\\temp\\test_grosses_noirs.jpeg" #6
    #chemin :str = ".\\data\\grosses\\blanches\\20.jpg"
    print(rn_train.evaluate(chemin)+1)