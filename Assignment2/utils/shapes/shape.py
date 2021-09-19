from abc import ABC, abstractmethod
import pygame
from pygame import draw

white = (255,255,255)
green = (0,255,0)

class Shape(ABC):
    @abstractmethod
    def contains(self, point):
        """Check if this shape contains specify point"""
    
    @abstractmethod
    def is_overlap(self, shape):
        """Check if this shape overlap another shape"""
    
    @abstractmethod
    def draw(self, shape):
        """Draw this shape using pygame draw engine"""



