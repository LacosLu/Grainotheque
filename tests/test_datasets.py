# ----- IMPORTS -----
# --- Bibliothèques internes ---
from datasets import ComptageGraines

# --- Bibliothèques externes ---
import unittest

# ----- CLASSE -----
class Test_ComptageGraines(unittest.TestCase):

    def setUp(self):
        self.__dataset : ComptageGraines = ComptageGraines("grosses\\blanches")

    def test_len(self):
        self.assertEqual(len(self.__dataset), 74)

    def test_getitem(self):
        retour_getitem = self.__dataset[0]
        self.assertEqual(type(retour_getitem), tuple)
        self.assertEqual(type(retour_getitem[1]), str)

    def test_iteration(self):
        i : int = 0
        for img,label in self.__dataset:
            self.assertEqual(img.all(), self.__dataset[i][0].all())
            self.assertEqual(label, self.__dataset[i][1])
            i += 1