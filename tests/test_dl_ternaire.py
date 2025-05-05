# ----- IMPORTS -----
# --- Bibliothèques internes ---
from dl_ternaire import Ternaire

# --- Bibliothèques externes ---
import unittest
import torch

# ----- CLASSE -----
class Test_DLTernaire(unittest.TestCase):

    def setUp(self):
        self.__rn_test : Ternaire = Ternaire()


    def test_retour(self):
        """Test de la valeur de retour du réseau de neurones
        """
        self.assertEqual(self.__rn_test(torch.rand((1,3,32,32))).shape, torch.Tensor([[3,3,3]]).shape)