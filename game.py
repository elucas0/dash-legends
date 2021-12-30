import pygame
import random
import time
import animation
from dino import Dino, Knight
from tiles import Tile, TileMap
from spritesheet import Spritesheet
from thread import MyThread

# Création d'une classe qui va representer notre jeu


class Game:
    def __init__(self, name_player_1='blue_dino', name_player_2='red_dino', name_proj_1='Spark', name_proj_2='Bolt', background_name='assets/Background/sunset_mountain/mountain.png'):
        # definir si la partie à commencé ou non
        self.is_playing = False
        self.over = False
        # Hauteur et largeur de l'ecran fixées
        self.surface = pygame.Surface((1920, 1080))
        self.w, self.h = self.surface.get_size()

        # portail de téléportation
        self.portail_1 = animation.AnimatePortail(self, 'portail 1', background_name)
        self.portail_2 = animation.AnimatePortail(self, 'portail 2', background_name)

        # Initialisation du temps entre chaque tir des joueurs
        self.tps_player_2 = 0
        self.tps_player_1 = 0
        # Création du sprite et du groupe de sprites
        self.moving_sprites = pygame.sprite.Group()
        self.player_1 = Knight(self, self.w, self.h, self.w//2.5, self.h//2, 'R', self.w - 200, name_player_1, name_proj_1)
        self.player_2 = Dino(self, self.w, self.h, self.w//1.6, self.h//2, 'L', 50, name_player_2, name_proj_2)
        self.moving_sprites.add(self.player_1)
        self.moving_sprites.add(self.player_2)
        # dictionnaire pour stocker les touches appuyées
        # (la touche appuyée est mise sur True)
        self.pressed = {}
        self.screen_shake = 0
        # on recupère les images des joueurs pour les choisir
        self.persos = animation.get_perso(animation.animations['persos'])
        # l'indice du joueur dans la liste
        self.perso_1_chosen = 0
        self.perso_2_chosen = 0
        # dedans ce sera le nom des joueurs
        self.players_chosen = ["", ""]
        # on recupère les images des projectiles pour les choisir
        self.projectiles = animation.get_projectile(animation.animations['projectiles']['projectile'])
        # l'indice du joueur dans la liste
        self.proj_1_chosen = 0
        self.proj_2_chosen = 0
        # dedans ce sera le nom des joueurs
        self.proj_chosen = ["", ""]


        # Fond d'écran
        self.background = pygame.image.load(background_name).convert()
        self.background = pygame.transform.scale(self.background, (1920, 1080))

        if self.background_name == 'assets/Background/sunset_mountain/mountain.png':
            self.load_sunset_mountain()
        elif self.background_name == 'assets/Background/icy_arena/arena.png':
            self.load_icy_arena()
        elif self.background_name == 'assets/Background/neo_lagos/neo.png':
            self.load_neo_lagos()

    def load_icy_arena(self):
        #Chargement des tuiles associées au background de la map
        arena_tiles = {}
        with open('worlds/icy_arena/icy_arena_tiles.txt') as tiles:
            for line in tiles:
                (key, val) = line.split()
                arena_tiles[key] = val
        spritesheet = Spritesheet('assets/Platform/tiles/icy_arena/tileset_ice_64x.png')
        self.map = TileMap('worlds/icy_arena/icy_arena_64x.csv', spritesheet, arena_tiles)

    def load_sunset_mountain(self):
        # dictionnaires des tile sheet et de leur valeur dans le csv
        mountain_tiles = {}
        with open('worlds/sunset_mountain/sunset_mountain_tiles.txt') as tiles:
            for line in tiles:
                (key, val) = line.split()
                mountain_tiles[key] = val
        spritesheet = Spritesheet('assets/Platform/tiles/tileset_mountains_64x.png')
        self.map = TileMap('worlds/sunset_mountain/sunset_mountain/sunset_mountain_64x.csv', spritesheet, mountain_tiles)

    def load_neo_lagos(self):
        neo_tiles = {}
        with open('worlds/neo_lagos/neo_lagos_tiles.txt') as tiles:
            for line in tiles:
                (key, val) = line.split()
                neo_tiles[key] = val
        spritesheet = Spritesheet('assets/Platform/tiles/tileset_city_64x.png')
        self.map = TileMap('worlds/neo_lagos/neo_lagos/neo_lagos_64x.csv', spritesheet, neo_tiles)
    
    def get_name_proj(self):
        """Retourne le nom des deux projectiles choisi

        --> name_proj1, name_proj2
        """
        return self.proj_chosen[0], self.proj_chosen[1]

    def choose_proj(self, screen, w, h):
        """Choix des projectiles

        Cette méthode est applée dans la fonction qui gère le choix des projectiles dans le fichier game (choose())
        """
        proj_1 = self.projectiles[self.proj_1_chosen]
        proj_2 = self.projectiles[self.proj_2_chosen]

        # affichage des persos
        screen.blit(proj_1[1], (round(w / 3.05) - proj_1[1].get_width()/2, h // 1.5))
        screen.blit(proj_2[1], (round(w / 1.50) - proj_2[1].get_width()/2, h // 1.5))

        # enregistrer le nom du perso du joueur 1 et 2
        self.proj_chosen[0] = proj_1[2]
        self.proj_chosen[1] = proj_2[2]

    def proj_at_left(self, proj_1, proj_2):
        """Changer le projectile"""
        if proj_1:
            self.proj_1_chosen -= 1
            if self.proj_1_chosen < 0:
                self.proj_1_chosen = len(self.projectiles) - 1
        elif proj_2:
            self.proj_2_chosen -= 1
            if self.proj_2_chosen < 0:
                self.proj_2_chosen = len(self.projectiles) - 1

    def proj_at_right(self, proj_1, proj_2):
        """Changer le projectile"""
        if proj_1:
            self.proj_1_chosen += 1
            if self.proj_1_chosen > len(self.projectiles) - 1:
                self.proj_1_chosen = 0
        elif proj_2:
            self.proj_2_chosen += 1
            if self.proj_2_chosen > len(self.projectiles) - 1:
                self.proj_2_chosen = 0

    def get_name_players(self):
        """Retourne le nom des deux joueur

        --> name_player1, name_player2
        """
        return self.players_chosen[0], self.players_chosen[1]

    def choose_players(self, screen, w, h):
        """Choix des personnages

        Cette méthode est applée dans la fonction qui gère le choix des personnages dans le fichier game (choose())
        """
        perso_1 = self.persos[self.perso_1_chosen]
        perso_2 = self.persos[self.perso_2_chosen]

        # affichage des persos
        screen.blit(perso_1[1], (round(w / 3.05) - perso_1[1].get_width()/2, h // 2.3))
        screen.blit(perso_2[1], (round(w / 1.50) - perso_2[1].get_width()/2, h // 2.3))

        # enregistrer le nom du perso du joueur 1 et 2
        self.players_chosen[0] = perso_1[2]
        self.players_chosen[1] = perso_2[2]

    def perso_at_left(self, perso_1, perso_2):
        """Changer le perso"""
        if perso_1:
            self.perso_1_chosen -= 1
            if self.perso_1_chosen < 0:
                self.perso_1_chosen = len(self.persos) - 1
        elif perso_2:
            self.perso_2_chosen -= 1
            if self.perso_2_chosen < 0:
                self.perso_2_chosen = len(self.persos) - 1

    def perso_at_right(self, perso_1, perso_2):
        """Changer le perso"""
        if perso_1:
            self.perso_1_chosen += 1
            if self.perso_1_chosen > len(self.persos) - 1:
                self.perso_1_chosen = 0
        elif perso_2:
            self.perso_2_chosen += 1
            if self.perso_2_chosen > len(self.persos) - 1:
                self.perso_2_chosen = 0

    def change_perso_keyboard(self):
        """Change le perso choisi"""
        if self.pressed.get(pygame.K_d):
            self.perso_1_chosen += 1
            if self.perso_1_chosen > len(self.persos) - 1:
                self.perso_1_chosen = 0
        if self.pressed.get(pygame.K_q):
            self.perso_1_chosen -= 1
            if self.perso_1_chosen < 0:
                self.perso_1_chosen = len(self.persos) - 1

        if self.pressed.get(pygame.K_RIGHT):
            self.perso_2_chosen += 1
            if self.perso_2_chosen > len(self.persos) - 1:
                self.perso_2_chosen = 0
        if self.pressed.get(pygame.K_LEFT):
            self.perso_2_chosen -= 1
            if self.perso_2_chosen < 0:
                self.perso_2_chosen = len(self.persos) - 1

    def game_over(self):
        """Reset le jeu"""
        self.is_playing = False

    def update_player_1(self):
        """Joueur 1"""
        if self.pressed.get(pygame.K_q) and self.player_1.rect.x - 40 > 0:
            self.player_1.LEFT_KEY = True
        else:
            self.player_1.LEFT_KEY = False

        # faire avancer à droite le joueur 1
        if self.pressed.get(
                pygame.K_d) and self.player_1.rect.x + self.player_1.rect.width + 40 < self.surface.get_width():
            self.player_1.RIGHT_KEY = True
        else:
            self.player_1.RIGHT_KEY = False

        # faire dash le joueur 1
        if self.pressed.get(pygame.K_s) :
            self.player_1.dash()

        # faire sauter le joueur 1
        if self.pressed.get(pygame.K_z):
            self.player_1.jump()

        elif self.player_1.is_jumping:
            # Divise la velocite par 1 si la flèce du haut est relachee
            self.player_1.velocity.y *= .5
            self.player_1.is_jumping = False

        if self.pressed.get(pygame.K_SPACE) and (time.time() - self.tps_player_1) > 1:
            self.player_1.launch_projectiles(self.player_2)
            self.tps_player_1 = time.time()
        # recuperer les projectiles du joueur 1
        for projectile in self.player_1.all_projectiles:
            self.screen_shake = projectile.move(self.screen_shake)
            projectile.checkCollisions(self.map.tiles)

        # appliquer l'ensemble des images du groupe de projectiles du joueur 1
        self.player_1.all_projectiles.draw(self.surface)

    def update_player_2(self):
        """Joueur 2"""
        # faire avancer à gauche le joueur 2
        if self.pressed.get(pygame.K_LEFT) and self.player_2.rect.x - 40 > 0:
            self.player_2.LEFT_KEY = True
        else:
            self.player_2.LEFT_KEY = False

        # faire avancer à droite le joueur 2
        if self.pressed.get(
                pygame.K_RIGHT) and self.player_2.rect.x + self.player_2.rect.width + 40 < self.surface.get_width():
            self.player_2.RIGHT_KEY = True
        else:
            self.player_2.RIGHT_KEY = False

        # faire dash le joueur 2
        if self.pressed.get(pygame.K_DOWN) :
            self.player_2.dash()

        # faire sauter le joueur 2
        if self.pressed.get(pygame.K_UP):
            self.player_2.jump()

        elif self.player_2.is_jumping:
            # Divise la velocite par 2 si la flèce du haut est relachee
            self.player_2.velocity.y *= .5
            self.player_2.is_jumping = False

        if (self.pressed.get(pygame.K_KP0)) and (time.time() - self.tps_player_2) > 1:
            # charger les projectiles du joueur
            self.player_2.launch_projectiles(self.player_1)
            self.tps_player_2 = time.time()
        # recuperer les projectiles du joueur 2
        for projectile in self.player_2.all_projectiles:
            self.screen_shake = projectile.move(self.screen_shake)
            projectile.checkCollisions(self.map.tiles)

        # appliquer l'ensemble des images du groupe de projectiles du joueur 2
        self.player_2.all_projectiles.draw(self.surface)

    def update(self, dt):
        """Methode principale du jeu"""
        # Permet d'appliquer un effet de tremblement
        render_offset = [0, 0]
        if self.screen_shake > 0:
            self.screen_shake -= 1
            if self.screen_shake:
                render_offset[0] = random.randint(0, 30) - 5
                render_offset[1] = random.randint(0, 30) - 5

        # Affichage de l'arrière-plan
        self.surface.blit(self.background, render_offset)

        # animer les portails de téléportation
        self.portail_1.animate()
        self.portail_2.animate()
        # afficher les portails de téléportation
        self.surface.blit(self.portail_1.image, (self.portail_1.rect.x, self.portail_1.rect.y))
        self.surface.blit(self.portail_2.image, (self.portail_2.rect.x, self.portail_2.rect.y))

        # Mettre à jour les joueurs en lancant leur fonction en meme temps (en parallèle)
        th1 = MyThread(self.update_player_1)
        th2 = MyThread(self.update_player_2)
        # lancer en parallèle leur fonction de mise à jour
        th1.start()
        th2.start()
        # attendre que les fonctions se finissent pour continuer la suite du code
        th1.join()
        th2.join()

        # Affichage des joueurs
        self.moving_sprites.draw(self.surface)
        # Physique des joueurs
        self.moving_sprites.update(dt, self.map.tiles)

        # Affichage du décor
        self.map.draw_map(self.surface, render_offset)

        # HUD (coeurs)
        self.player_1.empty_hearts(self.surface)
        self.player_2.empty_hearts(self.surface)

        check_1 = self.player_1.no_heart()
        check_2 = self.player_2.no_heart()

        return check_1, check_2

    def check_collision(self, sprite, group):
        """Méthode pour les collisions"""
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)


class EndGame(Game):

    def __init__(self, winner, loser, name_player_1, name_player_2, name_proj_1, name_proj_2, map_background):
        Game.__init__(self, name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)
        self.winner = winner
        self.loser = loser
        # mettre la position de fin
        self.player_1.rect.x = self.w // 2.1 - self.player_1.rect.width // 2
        self.player_2.rect.x = self.w // 1.9 - self.player_2.rect.width // 2

    def animate(self):
        """Méthode for the winner"""
        if self.winner == "Joueur 1":
            self.player_1.update_winner()
            self.player_2.update_loser()
        else:
            self.player_2.update_winner()
            self.player_1.update_loser()
