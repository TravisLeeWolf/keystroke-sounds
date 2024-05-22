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

L_VOLUME = [1.0, 0.9, 0.7, 0.5, 0.3, 0.2, 0.0, random.uniform(0.7, 1.0)]
R_VOLUME = [0.0, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0, random.uniform(0.7, 1.0)]

pygame.init()

keypress = pygame.mixer.Sound('./assets/keypress.wav')
spacebar = pygame.mixer.Sound('./assets/space.wav')
mouseclick = pygame.mixer.Sound('./assets/mouse.wav')
channels = [pygame.mixer.Channel(i) for i in range(5)]

def play_sound(sound, left_volume, right_volume):
    """
    Plays a sound with optional random volume.

    Args:
        sound (pygame.mixer.Sound): The sound to play.
        left_volume (float, optional): The volume for the left channel. Defaults to "random".
        right_volume (float, optional): The volume for the right channel. Defaults to "random".

    Raises:
        Exception: If there is an error playing the sound.

    Returns:
        None
    """

    for channel in channels:
        if not channel.get_busy():
            try:
                channel.set_volume(left_volume, right_volume)
                channel.play(sound)
                return
            except Exception as e:
                print(f"Error playing sound: {e}")

def on_press(key):
    """
    Called when a key is pressed.

    If the key is the spacebar, the spacebar sound is played.
    Otherwise, the keypress sound is played with a volume that depends on the
    location of the key on the keyboard.

    Args:
        key (Key): The key that was pressed.

    Raises:
        Exception: If there is an error playing the sound.

    Returns:
        None
    """
    try:
        if key == pynput.keyboard.Key.space:
            play_sound(spacebar, L_VOLUME[7], R_VOLUME[7])
        else:
            indexLR = get_LR_volume(key)
            play_sound(keypress, L_VOLUME[indexLR], R_VOLUME[indexLR])
    except Exception as e:
        print(f"Error playing sound: {e}")

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
        try:
            for i in range(len(KEY_ROW)):
                if key in KEY_ROW[i]:
                    return i
        except TypeError:
            return 7

def on_click(_x, _y, _button, pressed):
    """
    Called when the mouse is clicked.

    If the mouse is clicked, the mouseclick sound is played.
    """
    if pressed:
        play_sound(mouseclick, L_VOLUME[7], R_VOLUME[7])


with pynput.keyboard.Listener(on_press=on_press) as keyboard_listener, \
    pynput.mouse.Listener(on_click=on_click) as mouse_listener:
    keyboard_listener.join()
    mouse_listener.join()

