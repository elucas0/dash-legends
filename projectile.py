import pygame

# definir la classe qui va gerer le projectile de notre joueur


class Projectile(pygame.sprite.Sprite):

    # definir le constructeur de cette classe
    def __init__(self, player, game, w, h, sens, proj, ennemy):
        super().__init__()
        self.game = game
        # hauteur et largeur de l'ecran
        self.w, self.h = w, h
        # on lui passe les caracterisques du joueur
        self.player = player
        # Les projectiles du joueur (sous forme de liste d'image)
        self.proj = proj
        # on peut maintenant definir la premiere image (de base)
        self.image = self.proj[0]
        # on obtient sa position
        self.rect = self.image.get_rect()
        # sens du projectile --> ('L' ou 'R')
        self.sens = sens
        # determiner la position d'origine du projectile
        self.origin_pos_proj(self.sens)
        # sa vitesse
        self.vitesse = 10
        # compte les images
        self.frame = 0
        # Effet
        self.get_hit = pygame.mixer.Sound('assets/Music/Sounds/hit.wav')
        # pour savoir qui est l'ennemi (qui sera le player_1 ou player_2)
        self.ennemy_gr = pygame.sprite.Group()
        self.ennemy_gr.add(ennemy)

    def origin_pos_proj(self, sens):
        """Déterminer la position d'origine du projectile
        C'est à dire au niveau du joueur
        """
        # tire vers la droite
        if sens == 'R':
            # centrer le projectile sur le joueur
            self.rect.center = self.player.rect.center
            self.rect.y -= self.player.rect.height // 6
        # tire vers la gauche
        elif sens == 'L':
            # centrer le projectile sur le joueur
            self.rect.center = self.player.rect.center
            self.rect.y -= self.player.rect.height // 6

    def remove(self):
        """Supprimer le projectile en question"""
        self.player.all_projectiles.remove(self)

    def move(self, screen_shake):
        """Lancer le projectile"""
        self.frame += 1
        if self.frame >= len(self.proj) * 5:
            self.frame = 0

        if self.sens == 'L':
            self.rect.x -= self.vitesse
            self.image = pygame.transform.flip(
                self.proj[self.frame // 5], True, False)
        else:
            self.rect.x += self.vitesse
            self.image = self.proj[self.frame // 5]

        # tester les collisions avec les autres joueurs
        for player in self.game.check_collision(self, self.ennemy_gr):
            # supprimer le projectile
            self.remove()
            # Effet
            self.get_hit.play()
            # faire subir les degats au joueur
            self.player.get_damage()
            screen_shake = 30

        # verifier si notre projectile n'est plus present sur l'ecran
        if self.rect.x > self.w or self.rect.x + self.rect.width < 0:
            # supprimer le projectile
            self.remove()

        return screen_shake

    def get_hits(self, tiles):
        """Colision des joueurs avec le terrain"""
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisions(self, tiles):
        """Vérifie si le projectile touche le terrain"""
        collisions = self.get_hits(tiles)
        for tile in collisions:
            self.remove()
