# Importe la classe printer qui se trouve dans le dossier phomemo_printer_master/phomemo_printer dans le documment ESCPOS_printer.py
try:
    from phomemo_printer_master.phomemo_printer.ESCPOS_printer import Printer 
except:
    from .phomemo_printer_master.phomemo_printer.ESCPOS_printer import Printer 

# création de la classe Imprimante qui permet de se connecter à l'imprimante et de lancer une impression
class Imprimante:
    # initialise les informations appeller dans les fonction de cette classe qui à comme parametre la partie IMPRIMANTE du dossier config
    def __init__(self,config):
        self.__bluetooth_address: str = config["adresse_mac"] # attribut l'adresse MAC de l'imprimante donner dans le dossier config
        self.__channel: int = int(config["channel"]) # attribut le cannal de communication de l'imprimante donner dans le dossier config
    

    # fonction permetant la connection à l'imprimante et le lancement de l'impression qui à comme parametre l'image créé dans la classe Qrcode
    def impretion_qrcode(self,image):
        printer = Printer(self.__bluetooth_address, self.__channel) # lance la phase de connection à l'imprimante
        printer.print_image(image) # envoi les données de l'image et lance l'impression
        printer.close() # coupe la connection