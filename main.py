"""
Script to play sounds on keyboard and mouse events

This script plays a different sound for each key press, space bar press, and mouse click.
The volume of the sound is randomized between 0.9 and 1.1.

The script uses the pynput library to listen for keyboard and mouse events.
"""

import random
import pynput
import pygame
import simpleaudio

pygame.init()

try:
    keypress = pygame.mixer.Sound('./assets/keypress.wav')
    spacebar = pygame.mixer.Sound('./assets/space.wav')
    mouseclick = pygame.mixer.Sound('./assets/mouse.wav')
except FileNotFoundError:
    print("Error: unable to find sound files. Make sure they exist in the assets directory.")
except pygame.error:
    print("Error: unable to initialize pygame mixer. Check that pygame is installed correctly.")
except Exception as e:
    print(f"An error occurred while initializing sound: {e}")

def play_sound(sound):
    """
    Play a sound with a randomized volume.
    """
    try:
        volume = random.uniform(0.8, 1.2)
        sound.set_volume(volume)
        sound.play()
    except Exception as e:
        print(f"An error occurred while playing sound: {e}")

def on_press(key):
    """
    Play a sound on key press event.
    """
    try:
        if key is None:
            print("Error: null pointer reference in on_press")
            return
        if key == pynput.keyboard.Key.space:
            play_sound(spacebar)
        else:
            play_sound(keypress)
    except Exception as e:
        print(f"An error occurred in on_press: {e}")

def on_click(_x, _y, _button, pressed):
    """
    Play a sound on mouse click event.
    """
    try:
        if pressed:
            play_sound(mouseclick)
    except Exception as e:
        print(f"An error occurred in on_click: {e}")

try:
    with pynput.keyboard.Listener(on_press=on_press) as keyboard_listener, \
        pynput.mouse.Listener(on_click=on_click) as mouse_listener:
        keyboard_listener.join()
        mouse_listener.join()
except Exception as e:
    print(f"An error occurred: {e}")
