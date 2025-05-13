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
    from dl_ternaire import Ternaire
    from datasets import ComptageGraines
except:
    from .train_dl import TrainDL
    from .dl_ternaire import Ternaire
    from .datasets import ComptageGraines

# ----- CLASSE -----
class TrainDLTernaire(TrainDL):
    # --- Méthodes
    def __init__(self, net : str = ""):
        """Classe d'entrainement de réseaux de neurones

        :param net: nom du model pré-entrainé, defaults to ""
        :type net: str, optional
        """
        super().__init__()
        # --- Model ---
        self._net : Ternaire = Ternaire()

        if net != "":
            self._net.load_state_dict(torch.load(f".\\models\\{net}", weights_only=False))

        # --- Fonction d'optimisation ---
        self._optimizer : optim.SGD = optim.SGD(self._net.parameters(), lr=1e-2)
                
    def _normalisation(self, dataset : ComptageGraines, label : int, rotation : int = None) -> list:
        """Fonction de normalisation du dataset

        :param dataset: Dataste à normaliser
        :type dataset: ComptageGraines
        :param label: label
        :type label: int
        :param rotation: si l'image doit être tourner et de combien de degrés, defaults to None
        :type rotation: int, optional
        :return: list des images normalisées
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
            liste_norms.append((self.norm(imgs[i].view((3,32,32))),label))

        return liste_norms

    def _chargement_donnees(self, noms_nombres_fichiers : list[tuple[str,int,str]]):
        """Chargement des photos d'entrainement

        :param noms_nombres_fichiers: Liste des répertoires avec leurs nombre de photos
        :type noms_nombres_fichiers: list[tuple[str,int]]
        """
        # --- Récupération des datasets ---
        datasets : list[ComptageGraines] = []
        liste_labels : list[str] = []
        liste_labels_unique : list[str] = []
        for chemin, nb_photos, label in noms_nombres_fichiers:
            datasets.append(ComptageGraines(chemin, nb_photos))
            liste_labels.append(label)
            if label not in liste_labels_unique:
                liste_labels_unique.append(label)

        self._calcul_normalisation(datasets)

        # --- Normalisations ---
        datasets_norm : list = []
        for dataset in range(len(datasets)):
            datasets_norm += self._normalisation(datasets[dataset],
                                                  liste_labels_unique.index(liste_labels[dataset]))
            for rotation in TrainDL._rotations:
                datasets_norm += self._normalisation(datasets[dataset],
                                                      liste_labels_unique.index(liste_labels[dataset]),
                                                      rotation)

        self._train_dataload : DataLoader = DataLoader(datasets_norm, batch_size=1, shuffle=True)
        self._val_dataload : DataLoader = DataLoader(datasets_norm, batch_size=1, shuffle=False)

    def run(self, noms_nombres_fichiers, n_epochs, nom_model):
        self._chargement_donnees(noms_nombres_fichiers)
        super().run(noms_nombres_fichiers, n_epochs, nom_model)

# ----- PROGRAMME -----
if __name__ == "__main__":
    # -- Initialisation des éléments --
    rn_train = TrainDLTernaire()

    # -- Lancement --
    # - Paramètres -
    repertoires : list[tuple[str,int,str]] = [
        ("ternaire\\noirs\\grosses",    10,     "grosses"),
        ("ternaire\\noirs\\moyennes",   10,     "moyennes"),
        ("ternaire\\noirs\\petites",    10,     "petites"),
        ("grosses\\noirs",       5,     "grosses"),
        ("grosses\\noirs2",      5,     "grosses"),
        ('moyennes\\noirs',      5,     "moyennes"),
        ("moyennes\\noirs2",     5,     "moyennes"),
        ("petites\\noirs",       5,     "petites"),
        ("petites\\noirs2",      5,     "petites")
        ]
    
    """Répertoires possibles :
    [
        ("ternaire\\blanches\\grosses",    10,     "grosses"),
        ("ternaire\\blanches\\moyennes",   10,     "moyennes"),
        ("ternaire\\blanches\\petites",    10,     "petites"),
        ("grosses\\blanches",               5,     "grosses"),
        ("grosses\\blanches2",              5,     "grosses"),
        ("moyennes\\blanches",              5,     "moyennes"),
        ("moyennes\\blanches2",             5,     "moyennes"),
        ("petites\\blanches",               5,     "petites"),
        ("petites\\blanches2",              5,     "petites")
        ]

    [
        ("ternaire\\noirs\\grosses",    10,     "grosses"),
        ("ternaire\\noirs\\moyennes",   10,     "moyennes"),
        ("ternaire\\noirs\\petites",    10,     "petites"),
        ("grosses\\noirs",       5,     "grosses"),
        ("grosses\\noirs2",      5,     "grosses"),
        ('moyennes\\noirs',      5,     "moyennes"),
        ("moyennes\\noirs2",     5,     "moyennes"),
        ("petites\\noirs",       5,     "petites"),
        ("petites\\noirs2",      5,     "petites")
        ]
    """
    
    nb_epochs : int = 100
    model_name : str = "ternaire_n"

    # - run -
    rn_train.run(repertoires, nb_epochs, model_name)

    # -- Test --
    chemin : str = ".\\temp\\test_grosses_noirs_taille.jpeg"
    #chemin : str = ".\\data\\grosses\\blanches\\1.jpg"
    print(rn_train.evaluate(chemin))