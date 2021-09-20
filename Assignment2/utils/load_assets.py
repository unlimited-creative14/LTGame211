import os
import pygame

GAME_FOLDER = os.path.dirname(__file__)
IMG_FOLDER = os.path.join(GAME_FOLDER, '..', "images")
SND_FOLDER = os.path.join(GAME_FOLDER, '..', "sounds")

file_cache = {}


def load_img(name, scale=1):
    """ Load image and return image object"""
    fullname = os.path.join(IMG_FOLDER, name)
    try:
        if file_cache.get(fullname) is not None:
            image = file_cache.get(fullname)
        else:
            image = pygame.image.load(fullname)
            file_cache[fullname] = image

        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()

        image = pygame.transform.scale(image,
                                       (int(image.get_rect().width * scale), int(image.get_rect().height * scale)))
    except (pygame.error):
        print('Cannot load image:', fullname)
        raise SystemExit
    return image, image.get_rect()


def load_sound(name):
    fullname = os.path.join(SND_FOLDER, name)
    try:
        if file_cache.get(fullname) is not None:
            sound = file_cache.get(fullname)
        else:
            sound = pygame.mixer.Sound(fullname)
            file_cache[fullname] = sound
    except (pygame.error):
        print('Cannot load sound:', fullname)
        raise SystemExit
    return sound


def contains(rect, point):
    if rect.left > point[0]:
        return False
    if rect.top > point[1]:
        return False
    if rect.top + rect.height < point[1]:
        return False
    if rect.left + rect.width < point[0]:
        return False
    return True
