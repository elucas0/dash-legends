import pygame
from player import Player
"""
Class fille de la class Player
Le Dino est une sorte de Player (avec des caractéristiques personnelles)
"""


class Dino(Player):
    def __init__(self, game, w, h, pos_x, pos_y, facing, heart_x, sprite_name, proj_name):
        # charger les elements de base de la Class player
        Player.__init__(self, game, w, h, facing, heart_x, sprite_name, proj_name)
        # charger les images du sprite static
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y


class Knight(Player):
    def __init__(self, game, w, h, pos_x, pos_y, facing, heart_x, sprite_name, proj_name):
        # charger les elements de base de la Class player
        Player.__init__(self, game, w, h, facing, heart_x, sprite_name, proj_name)
        # charger les images du sprite static
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
