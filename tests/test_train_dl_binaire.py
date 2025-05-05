# ----- IMPORTS -----
# --- Bibliothèques internes ---
from train_dl_binaire import TrainDLBinaire
from datasets import ComptageGraines

# --- Bibliothèques externes ---
import unittest
import torch
from torch.utils.data import DataLoader
from torchvision import transforms

# ----- CLASSE -----
class Test_TrainDLBinaire(unittest.TestCase):

    def setUp(self):
        self.__train_dl_binaire : TrainDLBinaire = TrainDLBinaire()
        self.__dataset : ComptageGraines = ComptageGraines("grosses\\blanches")

    
    def test_calcul_normalisation(self):
        """Test des calculs liés à la normalisation
        """
        self.__train_dl_binaire._calcul_normalisation([self.__dataset])
        self.assertEqual(type(self.__train_dl_binaire.norm), transforms.Normalize)
        self.assertEqual(type(self.__train_dl_binaire.unorm), transforms.Normalize)
    
    def test_normalisation(self):
        """Test de la fonction de normalisation des images
        """
        self.__train_dl_binaire._calcul_normalisation([self.__dataset])
        retour_normalisation : list = self.__train_dl_binaire._normalisation(self.__dataset, "grosses")
        self.assertEqual(type(retour_normalisation), list)
        self.assertEqual(type(retour_normalisation[0]), tuple)
        self.assertEqual(type(retour_normalisation[0][0]), torch.Tensor)
        self.assertEqual(type(retour_normalisation[0][1]), str)

    def test_chargement_donnees(self):
        """Test de la fonction de chargement des données
        """
        self.__train_dl_binaire._chargement_donnees([("grosses\\blanches",74,"blanches")])
        self.assertEqual(type(self.__train_dl_binaire._train_dataload), DataLoader)
        self.assertEqual(type(self.__train_dl_binaire._val_dataload), DataLoader)