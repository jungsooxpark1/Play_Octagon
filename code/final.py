import sys
import time
import pygame
from pygame.constants import *
import RPi.GPIO as GPIO
import Adafruit_MPR121.MPR121 as MPR121

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Servo
GPIO.setup(23, GPIO.OUT)
p = GPIO.PWM(23, 50) 

# MPR121 (touch sensor)
# source from: https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial?view=all
cap = MPR121.MPR121()
if not cap.begin():
    print('Error initializing MPR121. Check your wiring!')
    sys.exit(1) 

# LEDS
led_pins = [24,5,6,12,13,16,25,20]

for pin in led_pins:
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, 0)

# Sounds-MP3 
# source from: https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/raspberry-pi-usage
# source from: https://www.pygame.org/docs/ref/mixer.html
pygame.mixer.pre_init(22050, -16, 2, 1024*4)
pygame.mixer.init() 
pygame.init()
pygame.mixer.set_num_channels(8) 
 
sound = [0,1,2,3,4,5,6,7]

# NOT USE: For loop causes delayed sounds
  # for s in range(8):
  #   sound[s] = pygame.mixer.Sound('song/c0'+ str(s) +'.wav')
  #   # pygame.mixer.set_num_channels(str(s)) 
  #   sound[s].play()
  #   sound[s].set_volume(0.2)

#A=September / C=YMCA
sound[0] = pygame.mixer.Sound('song/a00.wav')
sound[1] = pygame.mixer.Sound('song/a01.wav')
sound[2] = pygame.mixer.Sound('song/a02.wav')
sound[3] = pygame.mixer.Sound('song/a03.wav')
sound[4] = pygame.mixer.Sound('song/a04.wav')
sound[5] = pygame.mixer.Sound('song/a05.wav')
sound[6] = pygame.mixer.Sound('song/a06.wav')
sound[7] = pygame.mixer.Sound('song/a07.wav')
 
sound[0].play()
sound[0].set_volume(0.05)
sound[1].play()
sound[1].set_volume(0.05)
sound[2].play()
sound[2].set_volume(0.05)
sound[3].play()
sound[3].set_volume(0.05)
sound[4].play()
sound[4].set_volume(0.05)
sound[5].play()
sound[5].set_volume(0.05)
sound[6].play()
sound[6].set_volume(0.05)
sound[7].play()
sound[7].set_volume(0.05)

# time.sleep(240)

# MPR121 (touch sensor)
# source from: https://learn.adafruit.com/adafruit-mpr121-12-key-capacitive-touch-sensor-breakout-tutorial?view=all

def musik():
  last_touched = cap.touched()

  while True: 
      current_touched = cap.touched()

      for i in range(8):
          pin_bit = 1 << i
          if current_touched & pin_bit and not last_touched & pin_bit:
              if (sound[i]):
                  sound[i].set_volume(1)

              if (led_pins[i]):
                  GPIO.output(led_pins[i], 1)
                  #Servo
                  p.start(2.5)
                  p.ChangeDutyCycle(0 + 2.5 * i)
                  time.sleep(1)

          if not current_touched & pin_bit and last_touched & pin_bit:
              
              if (sound[i]):
                  sound[i].set_volume(0.05) 

              if (led_pins[i]):
                  GPIO.output(led_pins[i], 0) 

      last_touched = current_touched
      time.sleep(0.1)

# GPIO.cleanup()

if __name__ == '__main__':
    try:
        musik()
        # time.sleep(0.001) 
        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()
