import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, tilesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = tilesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        """Dessiner les tiles"""
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet, map_tiles):
        self.tile_size = 64
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename, map_tiles)
        # Surface aux dimensions de la map servant d'image pour afficher les tuiles
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def load_map(self):
        """Dessine chaque tuile sur la surface"""
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def draw_map(self, surface, shake):
        """Affiche la surface contenant toutes les tuiles"""
        surface.blit(self.map_surface, shake)

    def read_csv(self, filename):
        """Lis le csv contenant les donnees de la map"""
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename, map_tiles):
        """Charge les tuiles et associe leurs coordonnees dans la liste tiles"""
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == "0":
                    self.start_x, self.start_y = x * self.tile_size, y* self.tile_size
                elif tile != "-1":
                    tiles.append(Tile(map_tiles[tile], x * self.tile_size, y * self.tile_size, self.spritesheet))
                    # Déplacement a la tuile x + 1, même colonne
                x += 1
                # Déplacement a la tuile y + 1, différente colonne
            y += 1
            # Stocke la taille de la map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
