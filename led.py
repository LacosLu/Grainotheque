# Importation des classes nécessaires pour contrôler les LEDs WS2812 via SPI
from rpi5_ws2812.ws2812 import Color, WS2812SpiDriver

class Led:
    # Constructeur de la classe Led, initialise les LEDs avec les paramètres SPI
    def __init__(self, spi_bus=0, spi_device=0, led_count=160):
        # Création de l'objet WS2812SpiDriver pour contrôler la bande de LEDs
        self.strip = WS2812SpiDriver(spi_bus=spi_bus, spi_device=spi_device, led_count=led_count).get_strip()
        self.is_turn_on = False  # Variable pour suivre l'état des LEDs (allumées ou éteintes)

    def turn_on(self):
        # Allume toutes les LEDs de la bande avec une couleur blanche (RGB = 255, 255, 255)
        if not self.is_turn_on:
            self.strip.set_all_pixels(Color(255, 255, 200))  # Définit toutes les LEDs sur blanc
            self.strip.set_brightness(1) # Déinit l'intensité lumineuse des LEDs
            self.strip.show()  # Affiche les changements sur la bande de LEDs
            self.is_turn_on = True  # Met à jour l'état de l'LEDs (allumées)

    def turn_off(self):
        # Éteint toutes les LEDs de la bande (mettre les pixels à noir, RGB = 0, 0, 0)
        if self.is_turn_on:
            self.strip.set_all_pixels(Color(0, 0, 0))  # Définit toutes les LEDs sur éteint (noir)
            self.strip.show()  # Applique les changements
            self.is_turn_on = False  # Met à jour l'état des LEDs (éteintes)

    def toggle(self):
        # Bascule l'état des LEDs entre allumé et éteint
        if self.is_turn_on:
            self.turn_off()  # Si les LEDs sont allumées, les éteindre
        else:
            self.turn_on()  # Si les LEDs sont éteintes, les allumer

    def clear(self):
        self.strip.clear()

# Fonction principale qui gère l'interaction avec l'utilisateur
def main():
    # Création de l'objet Led
    try:
        led = Led()

    # Affiche un message d'instructions à l'utilisateur
        print("Appuie sur '1' pour allumer les LEDs, '2' pour les éteindre, et 'q' pour quitter")

        while True:
            # Demande à l'utilisateur de saisir une commande
            user_input = input("> ")

            # Si l'utilisateur entre '1', on allume les LEDs
            if user_input == '1':
                led.turn_on()
            # Si l'utilisateur entre '2', on éteint les LEDs
            elif user_input == '2':
                led.turn_off()
            # Si l'utilisateur entre 'q', on quitte le programme
            elif user_input == 'q':
                break
            # Si l'entrée est invalide, on affiche un message d'erreur
            else:
                print("Commande inconnue. Utilisez '1', '2' ou 'q'")
    except:
        led.clear()
        print("Erreur")
# Exécution de la fonction principale lorsque le script est lancé
if __name__ == "__main__":
    main()
