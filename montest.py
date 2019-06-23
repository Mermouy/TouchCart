# Copyright (c) 2014 Adafruit Industries
# Origin Author: Tony DiCola
# Author: Mermouy
# CopyWrong 2018

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import time
import pygame.mixer
import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ogg_zic = "/home/pi/TouchCart/ogg/"
wav_zic = "/home/pi/TouchCart/wav/"
musique_fond = ogg_zic + "Truck_soundscape_v2.ogg"

# Fonction volume + et -
def vol_up():
	new_vol = round(pygame.mixer.music.get_volume(), 1) + 0.1
	if new_vol >= 0.7:
		return 0.7
	return new_vol

def vol_down():
	new_vol = round(pygame.mixer.music.get_volume(), 1) - 0.1
	if new_vol <= 0.0:
		return 0.0
	return new_vol

# Create sound library to avoid redundance load
_sound_library = {}
def play_sound(path):
	global _sound_library
	sound = _sound_library.get(path)
	if sound == None:
		sound = pygame.mixer.Sound(path)
		_sound_library[path] = sound
	sound.play()

# Thanks to Scott Garner & BeetBox!
# https://github.com/scottgarner/BeetBox/

print 'Adafruit MPR121 Capacitive Touch Audio Player Mon Test'

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
	print 'Error initializing MPR121.  Check your wiring!'
	sys.exit(1)

# Alternatively, specify a custom I2C address such as 0x5B (ADDR tied to 3.3V),
# 0x5C (ADDR tied to SDA), or 0x5D (ADDR tied to SCL).
#cap.begin(address=0x5B)

# Also you can specify an optional I2C bus with the bus keyword parameter.
#cap.begin(bus=1)

pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

# Lancement fond sonore
pygame.mixer.music.load(musique_fond)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Init sounds volume
def get_vol():
	return round(pygame.mixer.music.get_volume(),1) + 0.3

# Define mapping of capacitive touch pin presses to sound files
# tons more sounds are available in /opt/sonic-pi/etc/samples/ and
# /usr/share/scratch/Media/Sounds/
SOUND_MAPPING = {
	0: ogg_zic + 'baby.ogg',
	1: ogg_zic + 'attention.ogg',
	2: ogg_zic + 'boite.ogg',
	3: ogg_zic + 'buddha.ogg',
	4: ogg_zic + 'klaxons.ogg',
	5: ogg_zic + 'helpyou.ogg',
	6: ogg_zic + 'lazer.ogg',
	7: ogg_zic + 'modem.ogg',
	8: ogg_zic + 'police.ogg',
	9: ogg_zic + 'recul.ogg',
	10: ogg_zic + 'yeah.ogg',
	11: ogg_zic + 'whatru.ogg',
}

sounds = [0,0,0,0,0,0,0,0,0,0,0,0]

for key,soundfile in SOUND_MAPPING.iteritems():
	sounds[key] =  pygame.mixer.Sound(soundfile)
	sounds[key].set_volume(get_vol());

# Main loop to print a message every time a pin is touched.
print 'Press Ctrl-C to quit.'
last_touched = cap.touched()
running = True
while running:
	current_touched = cap.touched()
	# Check each pin's last and current state to see if it was pressed or released.
	for i in range(12):
        # Each pin is represented by a bit in the touched value.  A value of 1
        # means the pin is being touched, and 0 means it is not being touched.
		pin_bit = 1 << i
        # First check if transitioned from not touched to touched.
		if current_touched & pin_bit and not last_touched & pin_bit:
			print '{0} touched!'.format(i)
			if (sounds[i]):
				sounds[i].play()
		# Check 11 & 10 pour modification volume
			if cap.is_touched(11):
				new_vol = vol_up()
				vol = new_vol + 0.3
				pygame.mixer.music.set_volume(new_vol)
				print("Volume est maintenant: " + str(vol))
				print("Volume de la zique est maintenant de: " + str(new_vol))
                                GPIO.setup(19,GPIO.OUT)
				GPIO.output(19,GPIO.HIGH)
                                print("Solenoid Out")
				time.sleep(3)
				print("Solenoid In")
				GPIO.output(19,GPIO.LOW)
			if cap.is_touched(10):
				new_vol = vol_down()
				vol = new_vol + 0.3
				pygame.mixer.music.set_volume(new_vol)
				print("Volume est maintenant: " + str(vol))
				print("Volume de la zique est maintenant de: " + str(new_vol))
		if not current_touched & pin_bit and last_touched & pin_bit:
			print '{0} released!'.format(i)

    # Update last state and wait a short period before repeating.
	last_touched = current_touched
	time.sleep(0.1)

    # Alternatively, if you only care about checking one or a few pins you can
    # call the is_touched method with a pin number to directly check that pin.
    # This will be a little slower than the above code for checking a lot of pins.
    #if cap.is_touched(0):
    #    print 'Pin 0 is being touched!'

    # If you're curious or want to see debug info for each pin, uncomment the
    # following lines:
    #print '\t\t\t\t\t\t\t\t\t\t\t\t\t 0x{0:0X}'.format(cap.touched())
    #filtered = [cap.filtered_data(i) for i in range(12)]
    #print 'Filt:', '\t'.join(map(str, filtered))
    #base = [cap.baseline_data(i) for i in range(12)]
    #print 'Base:', '\t'.join(map(str, base))
