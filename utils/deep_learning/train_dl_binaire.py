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
    from dl_binaire import Binaire
    from datasets import ComptageGraines
except:
    from .train_dl import TrainDL
    from .dl_binaire import Binaire
    from .datasets import ComptageGraines

# ----- CLASSE -----
class TrainDLBinaire(TrainDL):
    # --- Méthodes
    def __init__(self, net : str = ""):
        """Classe d'entrainement de réseaux de neurones

        :param net: nom du model pré-entrainé, defaults to ""
        :type net: str, optional
        """
        super().__init__()
        # --- Model ---
        self._net : Binaire = Binaire()

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
    rn_train = TrainDLBinaire("binaire.pt")

    # -- Lancement --
    # - Paramètres -
    repertoires : list[tuple[str,int,str]] = [
        ("grosses\\blanches",    74,     "grosses"),
        ("grosses\\blanches2",   74,     "grosses"),
        ("grosses\\noirs",       74,     "grosses"),
        ("grosses\\noirs2",      74,     "grosses"),
        ("moyennes\\blanches",   74,     "grosses"),
        ("moyennes\\blanches2",  74,     "grosses"),
        ('moyennes\\noirs',      74,     "petites"),
        ("moyennes\\noirs2",     74,     "petites"),
        ("petites\\blanches",    74,     "petites"),
        ("petites\\blanches2",   74,     "petites"),
        ("petites\\noirs",       36,     "petites"),
        ("petites\\noirs2",      36,     "petites")
        ]
    nb_epochs : int = 10
    model_name : str = "binaire"

    # - run -
    rn_train.run(repertoires, nb_epochs, model_name)

    # -- Test --
    chemin : str = ".\\temp\\test_grosses_noirs.jpeg"
    print(rn_train.evaluate(chemin))