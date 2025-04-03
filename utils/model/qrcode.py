import qrcode # Importe le paquet qrcode installer qui permet de créé un QR code 
from pyzbar.pyzbar import decode # Importe le paquet pyzbar installé pour la lecture de QR code
from PIL import ImageFont, ImageDraw, Image # Importe le paquet PIL qui permet l'ouverture, la manipulation et l'enregistrement de fichier


# création de la classe Qrcode qui permet de créé et de sauvegarder celui-ci
class Qrcode:
    # initialise les informations appeller dans les fonction de cette classe qui à comme parametre le dictionnaire de données et la partie QRCODE du dossier config
    def __init__(self,config):
        self.__chemin_png = config["chemin_image"] # inisialise le chemin du future QR code donnée par le fichier config
        self.__url = config["url"]
        # initialise les parametres de base du future QR code
        self.__qr = qrcode.QRCode(
            version =1, # la version 1 correspond à un QR code de 21x21 modules
            error_correction = qrcode.constants.ERROR_CORRECT_L, # définit le niveau de correction d'erreur
            box_size = 20, # définit la taille de chaque "boîte" (ou "module")
            border = 4 # définit la largeur du bord (le cadre autour du QR code)
        )
        self.__redim_image = (200,200) # dimention totale en pixel
        self.__taille_police = 13 # taille de la police
    

    # fonction permetant de créé le QR code et de le sauvegarder
    def creation_qrcode(self,donnee):
        # inisialise les informations du future QR code récupéré dans le dictionnaire
        self.__espece : str = donnee["espece"]
        self.__variete : str = donnee["variete"]
        self.__text : str = f"{self.__espece} {self.__variete}" # texte qui sera ajouter



        data =f'Famille : {donnee["famille"]}\nEspèce : {donnee["espece"]}\nVariété : {donnee["variete"]}\nRécolté le : {donnee["date_recolte"]}\nNombre de graine dans le sachet : {donnee["quantite_par_sachet"]}\n\nurl_aide : {self.__url}{self.__espece}' # informations dont le QR code à besoi et informations qu'il devra fournir
        self.__qr.add_data(data.encode("utf-8")) # convertir la chaîne en octets avant de l’ajouter au QR code en l'encodant en latin-1
        self.__qr.make(fit = True) # ne modifie pas la taille en fonction du nombre de donnée
        image_origine = self.__qr.make_image( fill_color = "black", back_color = "white") # défini les couleur de l'image
        image_origine = image_origine.resize(self.__redim_image) # redimentionne l'image
        # création du qrcode pour l'impression avec le texte
        image_texte = ImageDraw.Draw(image_origine) # recupere l'image créé précédement
        font = ImageFont.truetype("/home/pi/.fonts/arial.ttf", self.__taille_police)  # charge la police et sa taille
        text_size = image_texte.textbbox((0, 0), self.__text, font=font)  # calcule la taille du texte
        text_width = text_size[2] - text_size[0] # calcul de la largeur du texte
        text_height = text_size[3] - text_size[1] # calcul de la hauteur du texte

        img_width, img_height = image_origine.size # recupere la taille de l'image
        text_x = (img_width - text_width) / 2 # centre horizontalement le texte
        text_y = (img_height - text_height) / 2 # centre verticalement le texte
        # Dessiner un rectangle blanc derrière le texte pour le rendre lisible
        padding = 2
        image_texte.rectangle(
            [(text_x - padding, text_y - padding), (text_x + text_width + padding, text_y + text_height + padding)],
            fill="white"
        ) # dimentionne le rectengle
        image_texte.text((text_x, text_y), self.__text, fill="black", font=font) # Ajouter le texte
        png = f'{self.__chemin_png}/qr.png' # nomme l'image
        image_origine.save(png)
        return (png)




        # lire le QR code pris en photo
    def lecture_qrcode(self):
        self.__data = {} # dictionnaire qui récuperera les info du QR code
        img = Image.open(f"{self.__chemin_png}/qr.jpg") # ouverture du QR code
        decoded = decode(img) # décode l'image
        donnees = decoded[0].data.decode("utf-8") 
        # recupere les données et les met dans le dictionnaire
        for ligne in donnees.strip().split("\n"):
            if ligne =='':
                break
            key, value = ligne.split(" : ")
            self.__data[key.strip()] = value.strip()
        # récupert la variété pour la mise à jour de la BDD
        self.__variete = self.__data.get('variété')
        return self.__variete
