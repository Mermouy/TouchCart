# Copyright (c) 2014 Adafruit Industries
# Origin Author: Tony DiCola
# Author: Mermouy
# CopyWrong 2019

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
import alsaaudio
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

### Variables

# Dossiers et fichiers
ogg_zic = "/home/pi/TouchCart/ogg/"
wav_zic = "/home/pi/TouchCart/wav/"
musique_fond = ogg_zic + "Truck_soundscape_v2.ogg"

# Volume
#vol_max = 0.8
#min_vol = 0.0
vol_max = 100
min_vol = 30
vol_step = 5
bg_vol = 0.8

### Fonctions

m = alsaaudio.Mixer('PCM')
current_volume = m.getvolume() # Get the current Volume
m.setvolume(70)
os.system('espeak -v french-mbrola-1 --stdout -f penitence.txt -a 200 -s 130 -p 30 | oggenc -q 7 --resample 44100 -o ogg/penitence.ogg - && sleep 1')
os.system('espeak -v french-mbrola-1 --stdout -f bienvenue.txt -a 200 -s 130 -p 30 | oggenc -q 7 --resample 44100 -o ogg/bienvenue.ogg - ')
os.system('espeak -v french-mbrola-1 --stdout -f aider.txt -a 200 -s 130 -p 30 | oggenc -q 7 --resample 44100 -o ogg/aider.ogg - ')

# Fonction volume + et -
def vol_up():
#	new_vol = round(pygame.mixer.music.get_volume(), 1) + 0.1
	current_volume = m.getvolume() # Get the current Volume
	new_vol = current_volume[0] + vol_step
	if new_vol >= vol_max:
		return vol_max
	else:
		return new_vol

def vol_down():
#	new_vol = round(pygame.mixer.music.get_volume(), 1) - 0.1
	current_volume = m.getvolume() # Get the current Volume
	new_vol = current_volume[0] - vol_step
	if new_vol <= min_vol:
		return min_vol
	else:
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

print 'Truck a trucs Touch Audio Player Test'

# Create MPR121 instance.
cap = MPR121.MPR121()

# Initialize communication with MPR121 using default I2C bus of device, and
# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
if not cap.begin():
	print 'Error initializing MPR121.  Check wiring!'
	sys.exit(1)

pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

# Lancement fond sonore
pygame.mixer.music.load(musique_fond)
pygame.mixer.music.set_volume(bg_vol)
pygame.mixer.music.play(-1)

# Init sounds volume
def get_vol():
	return round(pygame.mixer.music.get_volume(),1) + 0.2

# Define mapping of capacitive touch pin presses to sound files
# tons more sounds are available in /opt/sonic-pi/etc/samples/ and
# /usr/share/scratch/Media/Sounds/
SOUND_MAPPING = {
	0: ogg_zic + 'bouchon.ogg',
	1: ogg_zic + 'applause0.ogg',
	2: ogg_zic + 'aidezmoi.ogg',
	3: ogg_zic + 'brass.ogg',
	4: ogg_zic + 'penitence.ogg',
	5: ogg_zic + 'bienvenue.ogg',
	6: ogg_zic + 'aider.ogg',
	7: ogg_zic + 'sirene.ogg',
	8: ogg_zic + 'yeah.ogg',
	9: ogg_zic + 'recul.ogg',
	10: ogg_zic + 'foraine.ogg',
	11: ogg_zic + 'truckatrucs.ogg',
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
				# vol = new_vol + 0.3
				m.setvolume(new_vol) #pygame.mixer.music.set_volume(new_vol)
				print("Volume de la zique est maintenant de: " + str(new_vol))
			if cap.is_touched(10):
				new_vol = vol_down()
				m.setvolume(new_vol) #pygame.mixer.music.set_volume(new_vol)
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
