import pygame
import sys
pygame.display.set_mode((900, 500 ) )

vol_zic = 0.5
vol = vol_zic + 0.3

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init

mazic = "/home/mermouy/test.mp3"
pygame.mixer.music.load(mazic)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(vol_zic)

def vol_up():
    new_vol= round(pygame.mixer.music.get_volume(), 1) + 0.1 
    if new_vol >= 0.7:
	return 0.7
    return new_vol
    

def vol_down():
    new_vol = round(pygame.mixer.music.get_volume(), 1) - 0.1
    if new_vol <= 0.0:
	return 0.0
    return new_vol

print("Volume de la zique: " + str(vol_zic))
print("Volume general: " + str(vol))

running = True

while running:
    for event in pygame.event.get():
	if event.type == pygame.QUIT:
	    running = False
	elif event.type == pygame.KEYUP:
	    if event.key == pygame.K_UP:
		vol_zic = vol_up()
		vol = vol_zic + 0.3
		pygame.mixer.music.set_volume(vol_zic)
	        print("Volume de la zique: " + str(vol_zic))
	        print("Volume general: " + str(vol))
	    elif event.key == pygame.K_DOWN:
		vol_zic = vol_down()
		vol = vol_zic + 0.3
		pygame.mixer.music.set_volume(vol_zic)
		print("Volume de la zique: " + str(vol_zic))
		print("Volume general: " + str(vol))

