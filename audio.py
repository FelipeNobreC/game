import pygame

MUSIC_PATH = "assets/sounds/corridor_ambient.mp3"

door_sound    = None
book_sound    = None
correct_sound = None
wrong_sound   = None

def init_audio():
    global door_sound, book_sound, correct_sound, wrong_sound
    door_sound    = pygame.mixer.Sound("assets/sounds/door.mp3")
    book_sound    = pygame.mixer.Sound("assets/sounds/book.mp3")
    correct_sound = pygame.mixer.Sound("assets/sounds/correct.mp3")
    wrong_sound   = pygame.mixer.Sound("assets/sounds/wrong.mp3")
