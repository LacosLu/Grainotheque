# ----- IMPORTS -----
# --- Bibliothèques internes ---
from dl_binaire import Binaire

# --- Bibliothèques externes ---
import unittest
import torch

class Test_TestDLBinaire(unittest.TestCase):
    
    def test_retour(self):
        rn_test : Binaire = Binaire()
        self.assertEqual(rn_test(torch.rand((1,3,32,32))).shape, torch.Tensor([[2,2]]).shape)