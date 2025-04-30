# ----- IMPORTS -----
# --- Bibliothèques internes ---
# -- Torch --
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# -- Torchvision --
from torchvision import transforms

# -- DateTime --
import datetime

# -- OpenCV --
import cv2 as cv

# -- Matplotlib --
import matplotlib.pyplot as plt

# -- Classe abtraite --
from abc import abstractmethod, ABC

# --- Bibliothèques externes ---
try:
    from dl_binaire import Binaire
    from dl_compte import Compte
    from dl_ternaire import Ternaire
except:
    from .dl_binaire import Binaire
    from .dl_compte import Compte
    from .dl_ternaire import Ternaire

# ----- CLASSE -----
class TrainDL(ABC):
    # --- Attributs de classes ---
    __loss_fn : nn.CrossEntropyLoss = nn.CrossEntropyLoss()
    _rotations : list[int] = [cv.ROTATE_90_CLOCKWISE, cv.ROTATE_180, cv.ROTATE_90_COUNTERCLOCKWISE]

    # --- Méthodes
    def __init__(self):
        """Classe d'entrainement de réseaux de neurones
        """
        # --- Model ---
        self._net : Compte | Binaire | Ternaire

        # --- Fonction d'optimisation ---
        self._optimizer : optim.SGD 

        # --- Données ---
        self._train_dataload : DataLoader
        self._val_dataload : DataLoader

        self.norm : transforms.Normalize
        self.unorm : transforms.Normalize
                
    @abstractmethod
    def _normalisation(self) -> list:
        """Fonction de normalisation du dataset
        """

    @abstractmethod
    def _chargement_donnees(self, noms_nombres_fichiers : list[tuple[str,int]]):
        """Chargement des photos d'entrainement

        :param noms_nombres_fichiers: Liste des répertoires avec leurs nombre de photos
        :type noms_nombres_fichiers: list[tuple[str,int]]
        """

    def _training_loop(self, n_epochs : int) -> None:
        """Boucle d'entrainement du réseau de neurones

        :param n_epochs: Nombre d'epochs
        :type n_epochs: int
        """
        for epoch in range(1, n_epochs + 1):
            loss_train = 0.0

            for imgs, labels in self._train_dataload:
                outputs = self._net(imgs)
                loss = TrainDL.__loss_fn(outputs, labels)
                self._optimizer.zero_grad()
                loss.backward()
                self._optimizer.step()
                loss_train += loss.item()

            if epoch == 1 or epoch % 10 == 0:
                print('{} Epoch {}, Training loss {}'.format(datetime.datetime.now(),
                                                             epoch,
                                                             loss_train / len(self._train_dataload)))
                
    def _calcul_normalisation(self, datasets : list) -> None:
        """Calcul de la moyenne et de l'écart-type des données afin de 
        générer les fonctions de normalisation et de dénormalisation

        :param datasets: Liste des datasets de données
        :type datasets: list
        """
        # - Création de la liste d'images -
        imgs : list = []

        for dataset in datasets:
            for img,_ in dataset:
                imgs.append(torch.Tensor(cv.resize(img, (32,32))))

        imgs : torch.Tensor = torch.stack(imgs).type(torch.float32)

        # - Calcul de moyenne et écart-type -
        moyenne = imgs.view(3,-1).mean(dim=1)
        ecart_type = imgs.view(3,-1).std(dim=1)

        # - Fonction de normalisation -
        self.norm = transforms.Normalize(moyenne, ecart_type)

        self.unorm = transforms.Normalize(
            mean=[-1*moyenne[0]/ecart_type[0],
                  -1*moyenne[1]/ecart_type[1],
                  -1*moyenne[2]/ecart_type[2]],
            std=[1/ecart_type[0],
                 1/ecart_type[1],
                 1/ecart_type[2]]
            )
    
    def _validate(self):
        """Fonction de test de pourcentage de bonnes réponses
        """
        for name, loader in [("train", self._train_dataload), ("val", self._val_dataload)]:
            correct = 0
            total = 0
            with torch.no_grad():
                for imgs, labels in loader:
                    outputs = self._net(imgs)
                    _, predicted = torch.max(outputs, dim=1)
                    total += labels.shape[0]
                    correct += int((predicted == labels).sum())

        print("Accuracy {}: {:.2f}".format(name , correct / total))

    def _sauvegarder_model(self, nom_model : str):
        """Sauvegarde du model

        :param nom_model: Nom du model
        :type nom_model: str
        """
        torch.save(self._net.state_dict(), f".\\models\\{nom_model}.pt")

    @abstractmethod
    def run(self, noms_nombres_fichiers : list[tuple[str|int]], n_epochs : int, nom_model : str):
        """Lance l'entrainement du réseau de neurones

        :param noms_nombres_fichiers: Liste des répertoires avec leurs nombre de photos
        :type noms_nombres_fichiers: list[tuple[str | int]]
        :param n_epochs: Nombre d'epochs d'entrainement
        :type n_epochs: int
        :param nom_model: Nom à donner au model
        :type nom_model: str
        """
        self._training_loop(n_epochs)
        self._validate()
        self._sauvegarder_model(nom_model)

    def evaluate(self, chemin_img : str) -> torch.Tensor:
        """Fonction d'évaluation avec une image

        :param chemin_img: chemin de l'image d'évaluation
        :type chemin_img: str
        :return: Nombre de graines
        :rtype: torch.Tensor
        """
        img = cv.imread(cv.samples.findFile(chemin_img))
        img : torch.Tensor = torch.tensor(cv.resize(img, (32,32))).type(torch.float32)

        self._net.eval()

        with torch.no_grad():
            out_data = self._net(self.norm(img.view(3,32,32)))

        return (out_data == max(out_data[0])).nonzero(as_tuple=False)[0][1]