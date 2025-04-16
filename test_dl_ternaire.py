# ----- IMPORTS -----
# --- Bibliothèques internes ---
from dl_ternaire import Ternaire

# --- Bibliothèques externes ---
import unittest
import torch

# ----- CLASSE -----
class Test_TestDLTernaire(unittest.TestCase):
    
    def test_retour(self):
        rn_test : Ternaire = Ternaire()
        self.assertEqual(rn_test(torch.rand((1,3,32,32))).shape, torch.Tensor([[3,3,3]]).shape)