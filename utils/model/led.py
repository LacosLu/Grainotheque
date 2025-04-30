try:
    from rpi5_ws2812.ws2812 import Color, WS2812SpiDriver
except:
    pass

class Led:

    def __init__(self, spi_bus=0, spi_device=0, led_count=160):
        self.strip = WS2812SpiDriver(spi_bus=spi_bus, spi_device=spi_device, led_count=led_count).get_strip()
        self.is_turn_on = False

    def turn_on(self):
        if not self.is_turn_on:
            self.strip.set_all_pixels(Color(255, 255, 255))
            self.strip.show()
            self.is_turn_on = True
            print("LED : Allumer")

    def turn_off(self):
        if self.is_turn_on:
            self.strip.set_all_pixels(Color(0, 0, 0))
            self.strip.show()
            self.is_turn_on = False
            print("LED : Eteinte")

    def toggle(self):
        if self.is_turn_on:
            self.turn_off()
        else:
            self.turn_on()

def main():
    led = Led()

    print("Appuie sur '1' pour allumer les LEDs, '2' pour les éteindre, et 'q' pour quitter")

    while True:
        user_input = input("> ")
        if user_input == '1':
            led.turn_on()
        elif user_input == '2':
            led.turn_off()
        elif user_input == 'q':
            break
        else:
            print("Commande inconnue. Utilisez '1', '2' ou 'q'")

if __name__ == "__main__":
    main()
