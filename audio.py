import sys
import os
import pygame

def _base():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.abspath('.')

_BASE = _base()
MUSIC_PATH = os.path.join(_BASE, "assets", "sounds", "corridor_ambient.mp3")

door_sound    = None
book_sound    = None
correct_sound = None
wrong_sound   = None

def init_audio():
    global door_sound, book_sound, correct_sound, wrong_sound
    door_sound    = pygame.mixer.Sound(os.path.join(_BASE, "assets", "sounds", "door.mp3"))
    book_sound    = pygame.mixer.Sound(os.path.join(_BASE, "assets", "sounds", "book.mp3"))
    correct_sound = pygame.mixer.Sound(os.path.join(_BASE, "assets", "sounds", "correct.mp3"))
    wrong_sound   = pygame.mixer.Sound(os.path.join(_BASE, "assets", "sounds", "wrong.mp3"))
