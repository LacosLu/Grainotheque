# ----- IMPORTS -----
# --- Bibliothèques internes ---
from dl_compte import Compte

# --- Bibliothèques externes ---
import unittest
import torch

# ----- CLASSE -----
class Test_DLCompte(unittest.TestCase):

    def setUp(self):
        self.__rn_test : Compte = Compte()


    def test_retour(self):
        """Test de la valeur de retour du réseau de neurones
        """
        self.assertEqual(self.__rn_test(torch.rand((1,3,32,32))).shape, torch.Tensor([[i for i in range(74)]]).shape)