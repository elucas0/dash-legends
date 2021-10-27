import pygame
import json

class Spritesheet:
    """"""
    def __init__(self, filename):
        """Constructeur ouvrant les fichiers requis"""
        # recuperer le fichier et le transformer en '.json' pour analyser l'emplacement des sprites
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename) # .convert()
        self.meta_data = self.filename.replace("png", "json")
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        """Retourne la liste de sprite"""
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        """Retourne un sprite spécifique en fonction de ses coordonnées"""
        sprite = self.data["frames"][name]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image

    def get_data(self):
        """Retourne le fichier '.json contenant les coordonnées de chaque sprite du spritesheet'
        """
        return self.data
