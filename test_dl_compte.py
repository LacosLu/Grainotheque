# ----- IMPORTS -----
# --- Bibliothèques internes ---
from dl_compte import Compte

# --- Bibliothèques externes ---
import unittest
import torch

# ----- CLASSE -----
class Test_TestDLCompte(unittest.TestCase):
    
    def test_retour(self):
        rn_test : Compte = Compte()
        self.assertEqual(rn_test(torch.rand((1,3,32,32))).shape, torch.Tensor([[i for i in range(74)]]).shape)