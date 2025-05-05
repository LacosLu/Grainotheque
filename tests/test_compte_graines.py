# ----- IMPORTS -----
# --- Bibliothèques internes ---
from utils.deep_learning import CompterGraines

# --- Bibliothèques externes ---
import unittest

# ----- CLASSE -----
class Test_CompterGraine(unittest.TestCase):

    def setUp(self):
        self.__comptage : CompterGraines = CompterGraines()

    
    def test_compter_graine(self):
        """Test du comptage de graines
        """
        nb_graines_sachet, nb_graines = self.__comptage.compter_graines()
        self.assertIn(nb_graines_sachet, [20,30,40])
        self.assertEqual(type(nb_graines),int)