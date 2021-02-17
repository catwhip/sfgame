import pygame, math

SURFACE_SIZE = (960, 540)
WINDOW_SIZE = (960, 540)

joysticks = []
JOYSTICKTEST = True

def controlEqual(event, key, button):
	return ("key" in event.__dict__ and event.key == key) or ("button" in event.__dict__ and event.button == button)