import pygame
from pygame.locals import *

def load_img(name, scale = 1):
    """ Load image and return image object"""
    fullname = './Assignment1/images/' + name
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()

        
        image = pygame.transform.scale(image, (int(image.get_rect().width * scale), int(image.get_rect().height * scale)))
    except (pygame.error):
        print('Cannot load image:', fullname)
        raise SystemExit
    return image, image.get_rect()

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
