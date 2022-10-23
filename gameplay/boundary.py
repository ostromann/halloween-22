import pygame
import pymunk


class Boundary(pymunk.Segment):
    def __init__(self):
        super().__init__()
