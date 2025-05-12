# ----- IMPORTS -----
# --- Bibliothèques externes ---
import torch
from torchvision import transforms
import cv2 as cv

# --- Bibliothèques internes ---
try:
    from train_dl_binaire import TrainDLBinaire
    from train_dl_compte import TrainDLCompte
    from train_dl_ternaire import TrainDLTernaire
    from datasets import ComptageGraines
except:
    from .train_dl_binaire import TrainDLBinaire
    from .train_dl_compte import TrainDLCompte
    from .train_dl_ternaire import TrainDLTernaire
    from .datasets import ComptageGraines

# ----- CLASSE -----
class CompterGraines:
    __chemin_photo_compte : str = "./temp/img.jpg"
    __chemin_photo_taille : str = "./temp/img_taille.jpg"
    __repertoires_rns : list[list[tuple[str,int,str]]] = [
        [
            ("grosses\\blanches",    74),
            ("grosses\\blanches2",   74),
            ("moyennes\\blanches",   74),
            ("moyennes\\blanches2",  74),
            ("petites\\blanches",    74),
            ("petites\\blanches2",   74)
        ],
        [
            ("grosses\\noirs",       74),
            ("grosses\\noirs2",      74),
            ('moyennes\\noirs',      74),
            ("moyennes\\noirs2",     74),
            ("petites\\noirs",       36),
            ("petites\\noirs2",      36)
        ],
        [
            ("grosses\\blanches",    74),
            ("grosses\\blanches2",   74),
            ("grosses\\noirs",       74),
            ("grosses\\noirs2",      74),
            ("moyennes\\blanches",   74),
            ("moyennes\\blanches2",  74),
            ('moyennes\\noirs',      74),
            ("moyennes\\noirs2",     74),
            ("petites\\blanches",    74),
            ("petites\\blanches2",   74),
            ("petites\\noirs",       36),
            ("petites\\noirs2",      36)
        ],
        [
            ("grosses\\blanches",    74),
            ("grosses\\blanches2",   74)
        ],
        [
            ("grosses\\noirs",       74),
            ("grosses\\noirs2",      74)
        ],
        [
            ("moyennes\\blanches",   74),
            ("moyennes\\blanches2",  74)
        ],
        [
            ('moyennes\\noirs',      74),
            ("moyennes\\noirs2",     74)
        ],
        [
            ("petites\\blanches",    74),
            ("petites\\blanches2",   74)
        ],
        [
            ("petites\\noirs",       36),
            ("petites\\noirs2",      36)
        ]
        ]
    
    def __init__(self):
        self.__rns : list[TrainDLBinaire|TrainDLCompte|TrainDLTernaire] = []
        self.__ternaire_b : TrainDLTernaire = TrainDLTernaire(f"ternaire_b.pt")
        self.__rns.append(self.__ternaire_b)
        self.__ternaire_n : TrainDLTernaire = TrainDLTernaire(f'ternaire_n.pt')
        self.__rns.append(self.__ternaire_n)
        self.__binaire : TrainDLBinaire = TrainDLBinaire(f"binaire.pt")
        self.__rns.append(self.__binaire)
        self.__compte_gb : TrainDLCompte = TrainDLCompte(f"compte_grosses_blanches.pt")
        self.__rns.append(self.__compte_gb)
        self.__compte_gn : TrainDLCompte = TrainDLCompte(f"compte_grosses_noirs.pt")
        self.__rns.append(self.__compte_gn)
        self.__compte_mb : TrainDLCompte = TrainDLCompte(f"compte_moyennes_blanches.pt")
        self.__rns.append(self.__compte_mb)
        self.__compte_mn : TrainDLCompte = TrainDLCompte(f"compte_moyennes_noirs.pt")
        self.__rns.append(self.__compte_mn)
        self.__compte_pb : TrainDLCompte = TrainDLCompte(f"compte_petites_blanches.pt")
        self.__rns.append(self.__compte_pb)
        self.__compte_pn : TrainDLCompte = TrainDLCompte(f"compte_petites_noirs.pt")
        self.__rns.append(self.__compte_pn)

        for idx in range(len(CompterGraines.__repertoires_rns)):
            self.__calcul_normalisation(CompterGraines.__repertoires_rns[idx], self.__rns[idx])

    def __calcul_normalisation(self, noms_nombres_fichiers : list[tuple[str,int]], rn : TrainDLBinaire|TrainDLCompte|TrainDLTernaire):
        # --- Récupération des datasets ---
        datasets : list[ComptageGraines] = []
        for chemin, nb_photos in noms_nombres_fichiers:
            datasets.append(ComptageGraines(chemin, nb_photos))

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
        norm = transforms.Normalize(moyenne, ecart_type)

        unorm = transforms.Normalize(
            mean=[-1*moyenne[0]/ecart_type[0],
                  -1*moyenne[1]/ecart_type[1],
                  -1*moyenne[2]/ecart_type[2]],
            std=[1/ecart_type[0],
                 1/ecart_type[1],
                 1/ecart_type[2]]
            )
        
        rn.norm = norm
        rn.unorm = unorm

    def compter_graines(self):
        nb_binaire : int = int(self.__binaire.evaluate(CompterGraines.__chemin_photo_compte))
        match nb_binaire:
            case 0:
                nb_ternaire_b : int = int(self.__ternaire_b.evaluate(CompterGraines.__chemin_photo_taille))
                match nb_ternaire_b:
                    case 0:
                        nb_graines_par_sachet : int = 20
                        nb_graines : int = int(self.__compte_gb.evaluate(CompterGraines.__chemin_photo_compte)) + 1
                    case 1:
                        nb_graines_par_sachet : int = 30
                        nb_graines : int = int(self.__compte_mb.evaluate(CompterGraines.__chemin_photo_compte)) + 1
                    case 2:
                        nb_graines_par_sachet : int = 40
                        nb_graines : int = int(self.__compte_pb.evaluate(CompterGraines.__chemin_photo_compte)) + 1
            case 1:
                nb_ternaire_n : int = int(self.__ternaire_n.evaluate(CompterGraines.__chemin_photo_taille))
                match nb_ternaire_n:
                    case 0:
                        nb_graines_par_sachet : int = 20
                        nb_graines : int = int(self.__compte_gn.evaluate(CompterGraines.__chemin_photo_compte)) + 1
                    case 1:
                        nb_graines_par_sachet : int = 30
                        nb_graines : int = int(self.__compte_mn.evaluate(CompterGraines.__chemin_photo_compte)) + 1
                    case 2:
                        nb_graines_par_sachet : int = 40
                        nb_graines : int = (int(self.__compte_pn.evaluate(CompterGraines.__chemin_photo_compte)) + 1) * 5
        return nb_graines_par_sachet,nb_graines

# ----- TEST -----
if __name__ == "__main__":
    cg : CompterGraines = CompterGraines()
    print(cg.compter_graines())