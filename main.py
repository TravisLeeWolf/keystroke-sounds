"""
This script uses the pynput library to listen for keyboard and mouse events.
It then plays a sound when a key is pressed or the mouse is clicked.

The sounds are played using the pygame library, and the volume of the sound
varies depending on the key that was pressed.
"""
import random
import pynput
import pygame

from pynput.keyboard import Key

KEY_ROW = [
    [Key.esc, '`', Key.tab, Key.caps_lock, Key.shift, Key.ctrl_l, '1', 'q', 'a', 'z', Key.alt_l],
    ['2', 'w', 's', 'x', '3', 'e', 'd', 'c'],
    ['4', 'r', 'f', 'v', '5', 't', 'g', 'b', '6'],
    ['7', 'y', 'h', 'n', '8', 'u', 'j', 'm'],
    ['9', 'i', 'k', ',', Key.alt_gr, '0', 'o', 'l', '.'],
    ['-', 'p', ';', '/', Key.ctrl_r, '=', '[', "'", Key.shift_r, Key.left],
    [Key.delete, Key.backspace, ']', '\\', Key.enter, Key.up, Key.down, Key.home, Key.page_up, Key.page_down, Key.end, Key.right]
]

L_VOLUME = [1.0, 0.9, 0.7, 0.5, 0.3, 0.2, 0.0]
R_VOLUME = [0.0, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]

pygame.init()


keypress = pygame.mixer.Sound('./assets/keypress.wav')
spacebar = pygame.mixer.Sound('./assets/space.wav')
mouseclick = pygame.mixer.Sound('./assets/mouse.wav')
channel = pygame.mixer.Channel(0)

def play_sound(sound, left_volume="random", right_volume="random"):
    """
    Plays a sound through pygame's mixer module.

    If the left_volume or right_volume arguments are set to "random", a
    random volume between 0.7 and 1.0 will be used instead.

    Args:
        sound (pygame.mixer.Sound): The sound to play.
        left_volume (float, optional): The volume of the sound on the left
            speaker. Defaults to "random".
        right_volume (float, optional): The volume of the sound on the right
            speaker. Defaults to "random".
    """
    if left_volume == "random":
        left_volume = random.uniform(0.7, 1.0)
        right_volume = random.uniform(0.7, 1.0)

    channel.set_volume(left_volume, right_volume)
    channel.play(sound)

def on_press(key):
    """
    Called when a key is pressed.

    If the key is the spacebar, the spacebar sound is played.
    Otherwise, the keypress sound is played with a volume that depends on the
    location of the key on the keyboard.
    """
    if key == pynput.keyboard.Key.space:
        play_sound(spacebar)
    else:
        indexLR = get_LR_volume(key)
        play_sound(keypress, L_VOLUME[indexLR], R_VOLUME[indexLR])

def get_LR_volume(key):
    """
    Returns the index in the L_VOLUME and R_VOLUME lists that corresponds to the
    given key.

    Args:
        key (Key): The key to get the index for.

    Returns:
        int: The index in the L_VOLUME and R_VOLUME lists.
    """
    try:
        for i in range(len(KEY_ROW)):
            if key.char in KEY_ROW[i]:
                return i
    except AttributeError:
        for i in range(len(KEY_ROW)):
            if key in KEY_ROW[i]:
                return i

def on_click(_x, _y, _button, pressed):
    """
    Called when the mouse is clicked.

    If the mouse is clicked, the mouseclick sound is played.
    """
    if pressed:
        play_sound(mouseclick)


with pynput.keyboard.Listener(on_press=on_press) as keyboard_listener, \
    pynput.mouse.Listener(on_click=on_click) as mouse_listener:
    keyboard_listener.join()
    mouse_listener.join()

