# ----- IMPORTS -----
# --- Bibliothèques externes ---
import cv2 as cv

# --- Bibliothèques internes ---
from datasets import ComptageGraines

# ----- CONSTANTES ------
repertoires : list[tuple[str,int,str]] = [
    ("grosses\\blanches",    74),
    ("grosses\\blanches2",   74),
    ("grosses\\blanches3",   74),
    ("grosses\\blanches4",   74),
    ("grosses\\noirs",       74),
    ("grosses\\noirs2",      74),
    ("grosses\\noirs3",      74),
    ("grosses\\noirs4",      74),
    ("moyennes\\blanches",   74),
    ("moyennes\\blanches2",  74),
    ("moyennes\\blanches3",  74),
    ("moyennes\\blanches4",  74),
    ('moyennes\\noirs',      74),
    ("moyennes\\noirs2",     74),
    ("moyennes\\noirs3",     74),
    ("moyennes\\noirs4",     74),
    ("petites\\blanches",    74),
    ("petites\\blanches2",   74),
    ("petites\\blanches3",   74),
    ("petites\\blanches4",   74),
    ("petites\\noirs",       36),
    ("petites\\noirs2",      36),
    ("petites\\noirs3",   32),
    ("petites\\noirs4",   33),
    ("ternaire\\noirs\\grosses",    10),
    ("ternaire\\noirs\\moyennes",   10),
    ("ternaire\\noirs\\petites",    10),
    ("ternaire\\blanches\\grosses",    10),
    ("ternaire\\blanches\\moyennes",   10),
    ("ternaire\\blanches\\petites",    10)
    ]

# ----- FONCTIONS -----
def resize_data(noms_nombres_fichiers) -> None:
    # --- Récupération des datasets ---
    datasets : list[ComptageGraines] = []
    for chemin, nb_photos in noms_nombres_fichiers:
        datasets.append(ComptageGraines(chemin, nb_photos))

    for i in range(len(datasets)):
        for img,label in datasets[i]:
            chemin : str = f"data_resized\\{noms_nombres_fichiers[i][0]}\\{label}.jpg"
            cv.imwrite(chemin, cv.resize(img, (32,32)))

# ----- PROGRAMME PRINCIPAL -----
resize_data(repertoires)