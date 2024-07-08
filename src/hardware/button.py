import RPi.GPIO as GPIO
import time

# Pin setup
button_pin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button_pressed_callback(channel):
    print("Button pressed!")

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated")

finally:
    GPIO.cleanup() 


