import time
from rpi_ws281x import PixelStrip, Color
import random

# LED strip configuration:
LED_COUNT = 8         
LED_PIN = 18         
LED_FREQ_HZ = 800000  
LED_DMA = 10          
LED_BRIGHTNESS = 255 
LED_INVERT = False   
LED_CHANNEL = 0      

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def color_fade(start_color, end_color, duration=1.0, steps=50):
    start_red, start_green, start_blue = start_color
    end_red, end_green, end_blue = end_color

    for step in range(steps):
        red = int(start_red + (end_red - start_red) * step / steps)
        green = int(start_green + (end_green - start_green) * step / steps)
        blue = int(start_blue + (end_blue - start_blue) * step / steps)

        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(red, green, blue))
        strip.show()
        time.sleep(duration / steps)

def light_up_all(color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def light_down_all():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

def sway_leds():
    for _ in range(4):
        for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(255, 255, 255))
                if i > 0:
                    strip.setPixelColor(i-1, Color(128, 128, 128))
                if i > 1:
                    strip.setPixelColor(i-2, Color(64, 64, 64))
                if i > 2:
                    strip.setPixelColor(i-3, Color(32, 32, 32))
                strip.show()
                time.sleep(0.1)
                if i > 3:
                    strip.setPixelColor(i-4, Color(0, 0, 0))
            
        for i in range(strip.numPixels()-1, -1, -1):
            strip.setPixelColor(i, Color(255, 255, 255))
            if i < strip.numPixels()-1:
                strip.setPixelColor(i+1, Color(128, 128, 128))
            if i < strip.numPixels()-2:
                strip.setPixelColor(i+2, Color(64, 64, 64))
            if i < strip.numPixels()-3:
                strip.setPixelColor(i+3, Color(32, 32, 32))
            strip.show()
            time.sleep(0.1)
            if i < strip.numPixels()-4:
                strip.setPixelColor(i+4, Color(0, 0, 0))
    light_up_all(Color(255,255,255))

def random_flash():
    for _ in range(20):
        for i in range(strip.numPixels()):
            brightness = random.randint(20, 255)
            strip.setPixelColor(i, Color(brightness, brightness, brightness))
        strip.show()
        time.sleep(0.1)
    

def cleanup():
    light_down_all()
    strip._cleanup()


