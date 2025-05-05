# ----- IMPORTS -----
# --- Bibliothèques internes ---
from dl_binaire import Binaire

# --- Bibliothèques externes ---
import unittest
import torch

# ----- CLASSE -----
class Test_DLBinaire(unittest.TestCase):

    def setUp(self):
        self.__rn_test : Binaire = Binaire()


    def test_retour(self):
        """Test de la valeur de retour du réseau de neurones
        """
        self.assertEqual(self.__rn_test(torch.rand((1,3,32,32))).shape, torch.Tensor([[2,2]]).shape)