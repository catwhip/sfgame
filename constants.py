import pygame, math

SURFACE_SIZE = (960, 540)
WINDOW_SIZE = (960, 540)

joysticks = []
JOYSTICKTEST = False

def controlEqual(event, key, button):
	return ("key" in event.__dict__ and event.key == key and not event.type == pygame.KEYUP) or ("button" in event.__dict__ and event.button == button and not event.type == pygame.JOYBUTTONUP)