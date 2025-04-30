# ----- IMPORTS -----
from torch.utils.data import Dataset
import cv2 as cv

# ----- PROGRAMME -----
class ComptageGraines(Dataset):
    # --- Méthodes ---
    def __init__(self, taille_couleur : str, nb_photos : int = 74) -> None:
        """Dataset regroupant les images du compte des graines jusqu'à 144
        """
        super().__init__()
        self.__root_dir : str = f"data\\{taille_couleur}"
        self.__nb_photos : int = nb_photos

        # --- Itérateur ---
        self.__actuel : int = 0
        self.__fin : int = self.__nb_photos
    
    def __len__(self) -> int:
        """Taille de la dataset
        """
        return self.__nb_photos
    
    def __getitem__(self, idx : int):
        """Renvoie la photo à l'index idx graines

        :param idx: index
        :type idx: int
        """
        if idx < 0 or idx >= self.__nb_photos:
            raise ValueError
        else:
            try:
                img_path : str = f"{self.__root_dir}\\{idx+1}.jpg"
                img = cv.imread(cv.samples.findFile(img_path))
                return img,str(idx+1)
            except:
                raise FileNotFoundError(f"Image non trouvé : {img_path}")
            
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__actuel >= self.__fin:
            self.__actuel = 0
            raise StopIteration
        actuel = self.__actuel
        self.__actuel += 1 
        return self[actuel]
            
# ----- TESTS -----
if __name__ == "__main__":
    dataset_test = ComptageGraines("noirs")

    img = dataset_test[0][0]

    # --- Affichage d'une photo ---
    cv.imshow("Image", img)
    k = cv.waitKey(0)