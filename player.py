import time

import pygame
from projectile import Projectile
import animation


class Player(animation.AnimateSprite):
    def __init__(self, game, w, h, facing, heart_x, sprite_name, proj_name):
        super().__init__(sprite_name, proj_name, facing, heart_x)
        self.game = game
        # hauteur et largeur de l'ecran
        self.w, self.h = w, h
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        # definir un groupe de projectile pour notre joueur
        self.all_projectiles = pygame.sprite.Group()
        self.stop = False
        self.is_dashing = False
        self.dash_cooldown = 0
        self.dash_timer = 0
        self.on_dash = pygame.mixer.Sound('assets/Music/Sounds/dash.wav')
        self.on_dash.set_volume(0.2)
        # ajouter le portail au joueur (pour la collision)
        self.portail_gr = pygame.sprite.Group()
        self.portail_gr.add(self.game.portail_1)
        self.portail_gr.add(self.game.portail_2)
        # le temps d'atterrir pour ne pas se retéléporter
        self.time_to_respawn = 0
        self.time_laps = 0
        self.n = 0

    def launch_projectiles(self, ennemy):
        """Charger une nouvelle instance de la classe Projectile"""
        self.all_projectiles.add(Projectile(self, self.game, self.w, self.h, self.facing, self.images_proj, ennemy))
    
    def update_winner(self):
        """Méthode quand le joueur gagne la partie"""
        self.winner()

    def update_loser(self):
        """Méthode quand le joueur perd la partie"""
        self.loser()

    def update(self, dt, tiles):
        """Anime le personnage"""
        # Lance les fonctions de mouvements
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)

        # les collisions avec le portail de téléportation
        if time.time() - self.time_laps > 0.2:
            for portail in self.game.check_collision(self, self.portail_gr):
                # regarder quel portail est touché
                if portail.name == 'portail 1':
                    if self.n > 0 and time.time() - self.time_to_respawn > 2:
                        self.rect.x = self.game.portail_2.rect.x + 50
                        self.rect.y = self.game.portail_2.rect.y
                        # pour éviter de se retéléporter quand on arrive à l'autre portail
                        self.time_to_respawn = time.time()
                        self.n = 0
                    else:
                        # enregistrer le temps
                        self.time_laps = time.time()
                        # pour savoir qu'on a touché le portail
                        self.n += 1

                elif portail.name == 'portail 2':
                    if self.n > 0 and time.time() - self.time_to_respawn > 2:
                        self.rect.x = self.game.portail_1.rect.x
                        self.rect.y = self.game.portail_1.rect.y
                        # pour éviter de se retéléporter quand on arrive à l'autre portail
                        self.time_to_respawn = time.time()
                        self.n = 0
                    else:
                        # enregistrer le temps
                        self.time_laps = time.time()
                        # pour savoir qu'on a touché le portail
                        self.n += 1

        # lancer la méthode qui anime le joueur
        self.animate(self.LEFT_KEY, self.RIGHT_KEY)

        # Si le dash est activé
        if self.is_dashing:
            # Durée du dash s'écoule
            self.dash_timer -= dt
            # Si la durée du dash s'est écoulée
            if self.dash_timer <= 0:
                # Cooldown réinitialisé à 2 secondes
                self.dash_cooldown = 120
                # Le joueur ne dash plus
                self.is_dashing = False
        # Sinon, le cooldown diminue
        else:
            self.dash_cooldown -= dt

    def dash(self):
        """Augmente la vitesse du joueur pendant une demi seconde
           pour creer un effet de dash"""
        # Si le joueur n'est pas deja en train de dash et que le cooldown est fini
        if not self.is_dashing and self.dash_cooldown <= 0:
            # Le dash dure une demi seconde
            self.dash_timer = 30
            # Effet
            self.on_dash.play()
            # Le joueur est en train de dash
            self.is_dashing = True
            if self.facing == 'L':
                self.velocity.x = -60
            else :
                self.velocity.x = 60

    def horizontal_movement(self, dt):
        # Acceleration par defaut = 0
        self.acceleration.x = 0
        # Si la flèche gauche vaut True
        if self.LEFT_KEY:
            self.acceleration.x -= 2
        # Si la flèche droite vaut True
        elif self.RIGHT_KEY:
            self.acceleration.x += 2
        # Augmentation de l'acceleration par la vélocité (vitesse et direction) multiplié par la friction (<1)
        self.acceleration.x += self.velocity.x * self.friction
        # Augmentation de la velocité x avec le temps
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        # Formule de Newton sur le mouvement
        self.rect.x += self.velocity.x * dt #+ (self.acceleration.x * .5) * (dt * dt)

    def vertical_movement(self, dt):
        # Augmentation de la velocité y avec le temps
        self.velocity.y += self.acceleration.y * dt
        # Limite de la hauteur du saut
        if self.velocity.y > 7:
            self.velocity.y = 7
        # Formule de Newton sur le mouvement
        # Simule la gravité en augmentant la position y
        self.rect.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
    
    def get_hits(self, tiles):
        """Liste contenant les collisions"""
        hits = []
        for tile in tiles:
            # Si il y a collision entre le joueur et une tile
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles):
        """Vérifie les collisions sur x"""
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0: # Si joueur touche une tuile en venant de gauche
                self.velocity.x = 0
                self.rect.x = tile.rect.left - self.rect.w # Bloque le joueur a gauche de la tuile + sa largeur
            elif self.velocity.x < 0: # Si joueur touche une tuile en venant de droite
                self.velocity.x = 0
                self.rect.x = tile.rect.right # Bloque le joueur a droite de la tuile
    
    def checkCollisionsy(self, tiles):
        """Vérifie les collisions sur y"""
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.rect.y = tile.rect.top
                self.rect.bottom = self.rect.y
            elif self.velocity.y < 0:  # Si joueur touche le bas d'une tuile
                self.velocity.y = 0  # Arrête le saut du joueur
                self.rect.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.rect.y

    def limit_velocity(self, max_vel):
        # Définit les valeurs minimale et maximale que peut prendre velocité
        min(-max_vel, max(self.velocity.x, max_vel))
        # Si la vélocité est < 0.01, la vélocité devient nulle
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def get_damage(self):
        if self.health > 0:
            self.health -= 1
                
    def no_heart(self):
        if self.health <= 0:
            return True
