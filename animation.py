import pygame
import os
from spritesheet import Spritesheet


# definir une class qui va s'occuper des animations


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_name, proj_name, facing, heart_x):
        super().__init__()
        # definir l'image de base du sprite/joueur --> le rectangle se basera sur cette image
        # self.image = animations['persos']['perso'].get(sprite_name)[0]
        self.image = animations['persos'][sprite_name].get('static')[0]
        # stocker le nom du joueur
        self.sprite_name = sprite_name
        # chercher toutes les images correspondants au joueur choisis
        self.images_run = animations['persos'][sprite_name].get('run')
        self.images_static = animations['persos'][sprite_name].get('static')
        self.images_jump = animations['persos'][sprite_name].get('jump')
        self.images_dead = animations['persos'][sprite_name].get('dead')
        self.images_hit = animations['persos'][sprite_name].get('hit')
        self.images_attack = animations['persos'][sprite_name].get('attack')
        # self.images_shield = animations['persos'][sprite_name].get('shield')
        self.images_proj = animations['projectiles']['projectile'].get(proj_name)
        self.images_heart = animations['huds']['hud'].get('heart')
        # dictionnaire qui s'occupe des images/frames courant pour l'animation du joueur
        self.current_images = {
            'run': 0,
            'static': 0,
            'jump': 0,
            'double_jump': 0,
            'attack': 0,
            'shield': 0,
            'dead': 0,
            'hit': 0
        }
        # dictionnaire qui s'occupe des images/frames courant pour les coeurs du joueur
        self.current_hud = {
            'heart': 0
        }
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.3
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        # faving --> pour savoir si le joueur regarde à gauche ou à droite
        self.facing = facing
        # faire l'animation qu'une seule fois pour le loser
        self.loser_animation = 0
        self.winner_animation = 0

        # position des coeurs du joueur (coeur de vie en haut de l'écran)
        self.heart_x = heart_x
        self.health = 3
        self.max_health = 3
        # coeur 1, 2, 3
        self.hearts = [True, True, True]

    def empty_hearts(self, screen):
        """Animaion des coeurs"""
        for heart in range(self.max_health):
            if heart < self.health:
                screen.blit(self.images_heart[0], (heart * 50 + self.heart_x, 15))
            elif self.hearts[heart]:
                self.current_hud['heart'] += 1
                if self.current_hud['heart'] >= len(self.images_heart) * 7:
                    self.hearts[heart] = False
                    self.current_hud['heart'] = 0
                # if self.hearts[heart]:
                #     screen.blit(self.images_heart[self.current_hud['heart'] // 7], (heart * 50 + self.heart_x, 15))
                # screen.blit(self.images_heart[self.current_hud['heart'] // 7], (heart * 50 + self.heart_x, 15))

                if self.hearts[heart]:
                    screen.blit(self.images_heart[self.current_hud['heart'] // 7], (heart * 50 + self.heart_x, 15))
                else:
                    screen.blit(self.images_heart[5], (heart * 50 + self.heart_x, 15))

    def move_on_floor(self, left_key):
        """Méthode ANIMATION

        Méthode pour l'animation du joueur sur le sol
        """
        # passer à l'image suivante
        self.current_images['run'] += 1

        # verifier si on a atteint la fin de l'animation
        # le '* 3' sert à ralentir l'animation
        if self.current_images['run'] >= len(self.images_run) * 3:
            # remettre l'animation au départ
            self.current_images['run'] = 0

        # modifier l'image précedente par la suivante
        # le '// 3' sert à ralentir l'animation
        # verifier si on se déplace à gauche ou à droite
        if left_key:
            self.facing = 'L'
            self.image = pygame.transform.flip(self.images_run[self.current_images['run'] // 3], True, False)
        else:
            self.facing = 'R'
            self.image = self.images_run[self.current_images['run'] // 3]

    def not_move(self):
        """Méthode ANIMATION

        Méthode pour animer le sprite quand il ne bouge pas
        Le faire respirer pour rendre le jeu plus réaliste, plus complet
        """
        # passer à l'image suivante
        self.current_images['static'] += 1

        # verifier si on a atteint la fin de l'animation
        # le '* 3' sert à ralentir l'animation
        if self.current_images['static'] >= len(self.images_static) * 7:
            # remettre l'animation au départ
            self.current_images['static'] = 0

        # modifier l'image précedente par la suivante
        # le '// 3' sert à ralentir l'animation
        # verifier si on se déplace à gauche ou à droite
        if self.facing == 'L':
            self.image = pygame.transform.flip(self.images_static[self.current_images['static'] // 7], True,
                                               False)
        else:
            self.image = self.images_static[self.current_images['static'] // 7]

    def jump(self):
        """Méthode ANIMATION

        Méthode pour l'animation du joueur quand il saute
        """
        # Le joueur ne peut sauter que si il est sur le sol
        if self.on_ground:
            # si le joueur touche le sol, remettre l'image de base
            self.current_images['jump'] = 0
            self.is_jumping = True
            self.velocity.y -= 11
            self.on_ground = False

        self.current_images['jump'] += 1

        if self.current_images['jump'] >= len(self.images_jump) * 20:
            self.current_images['jump'] = 0

        if self.facing == 'L':
            self.image = pygame.transform.flip(self.images_jump[self.current_images['jump'] // 20], True, False)
        else:
            self.image = self.images_jump[self.current_images['jump'] // 20]

    def animate(self, left_key=False, right_key=False):
        """Méthode ANIMATION

        Méthode Principale pour animer le sprite
        """
        # si le joueur saute et bouge vers la gauche ou la droite
        if self.is_jumping and (left_key or right_key):
            # tourner la tete du joueur si il change de direction quand il est en train de sauter
            if left_key:
                self.facing = 'L'
            else:
                self.facing = 'R'

        # si le joueur change de sens dans les aires en lachant la touche jump 
        elif not self.is_jumping and (left_key or right_key):
            # tourner la tete du joueur si il change de direction quand il est en train de sauter
            if left_key:
                self.facing = 'L'
            else:
                self.facing = 'R'

        # si le joueur se déplace sur le sol
        if self.on_ground and (left_key or right_key):

            # bouger sur le sol
            self.move_on_floor(left_key)

        # si le joueur est sur le sol mais qu'il ne se déplace pas
        elif self.on_ground:
            # faire respirer le joueur
            self.not_move()

        else:
            # faire respirer le joueur
            self.not_move()

    def winner(self):
        """Méthode ANIMATION

        Animer le joueur qui a gagner
        """
        # si c'est un chevalier on fait l'animation qu'une seule fois
        if 'knight' in self.sprite_name and self.winner_animation <= 1:
            # passer à l'image suivante
            self.current_images['attack'] += 1

            # verifier si on a atteint la fin de l'animation
            # le '* 3' sert à ralentir l'animation
            if self.current_images['attack'] >= len(self.images_attack) * 5:
                self.winner_animation += 1
                # remettre l'animation au départ
                self.current_images['attack'] = 0

            if self.winner_animation <= 1:
                # modifier l'image précedente par la suivante
                # le '// 3' sert à ralentir l'animation
                # verifier si on se déplace à gauche ou à droite
                if self.facing == 'L':
                    self.image = pygame.transform.flip(self.images_attack[self.current_images['attack'] // 5], True, False)
                else:
                    self.image = self.images_attack[self.current_images['attack'] // 5]
        else:
            # faire respirer le joueur
            self.not_move()

    def loser(self):
        """Méthode ANIMATION

        Animer le joueur qui a perdu
        """
        # si c'est un chevalier on fait l'animation qu'une seule fois
        if 'knight' in self.sprite_name:
            # on teste si la première animation n'est pas fini
            if self.loser_animation == 0:
                # passer à l'image suivante
                self.current_images['dead'] += 1

                # verifier si on a atteint la fin de l'animation
                # le '* 3' sert à ralentir l'animation
                if self.current_images['dead'] >= len(self.images_dead) * 10:
                    self.loser_animation += 1
                    # # remettre l'animation au départ
                    # self.current_images['dead'] = 0

                if self.loser_animation == 0:
                    # modifier l'image précedente par la suivante
                    # le '// 3' sert à ralentir l'animation
                    # verifier si on se déplace à gauche ou à droite
                    if self.facing == 'L':
                        self.image = pygame.transform.flip(self.images_dead[self.current_images['dead'] // 10], True, False)
                    else:
                        self.image = self.images_dead[self.current_images['dead'] // 10]
        # les autres persos on fait l'animation en continue
        elif 'dino' in self.sprite_name:
            # passer à l'image suivante
            self.current_images['dead'] += 1

            # verifier si on a atteint la fin de l'animation
            # le '* 3' sert à ralentir l'animation
            if self.current_images['dead'] >= len(self.images_dead) * 20:
                # remettre l'animation au départ
                self.current_images['dead'] = 0

            # modifier l'image précedente par la suivante
            # le '// 3' sert à ralentir l'animation
            # verifier si on se déplace à gauche ou à droite
            if self.facing == 'L':
                self.image = pygame.transform.flip(self.images_dead[self.current_images['dead'] // 20], True, False)
            else:
                self.image = self.images_dead[self.current_images['dead'] // 20]
        # les autres perso n'ont pas d'animation de mort
        else:
            # passer à l'image suivante
            self.current_images['hit'] += 1

            # verifier si on a atteint la fin de l'animation
            # le '* 3' sert à ralentir l'animation
            if self.current_images['hit'] >= len(self.images_hit) * 20:
                # remettre l'animation au départ
                self.current_images['hit'] = 0

            # modifier l'image précedente par la suivante
            # le '// 3' sert à ralentir l'animation
            # verifier si on se déplace à gauche ou à droite
            if self.facing == 'L':
                self.image = pygame.transform.flip(self.images_hit[self.current_images['hit'] // 20], True, False)
            else:
                self.image = self.images_hit[self.current_images['hit'] // 20]


class AnimatePortail(pygame.sprite.Sprite):

    def __init__(self, game, name, map):
        super().__init__()
        self.game = game
        self.name = name
        # récupérer l'image de base
        self.image = portail[0]
        self.rect = self.image.get_rect()
        # postionner le portail suivant la map chosis
        if map == 'assets/Background/sunset_mountain/mountain.png':
            if self.name == 'portail 1':
                self.rect.x = self.game.w // 1.17
                self.rect.y = self.game.h // 1.66
            elif self.name == 'portail 2':
                self.rect.x = self.game.w // 20 - self.rect.width // 1.3
                self.rect.y = self.game.h // 20
        elif map == 'assets/Background/icy_arena/arena.png':
            if self.name == 'portail 1':
                self.rect.x = self.game.w // 1.1
                self.rect.y = self.game.h // 2.5
            elif self.name == 'portail 2':
                self.rect.x = self.game.w // 3
                self.rect.y = self.game.h // 20 - 70
        elif map == 'assets/Background/neo_lagos/neo.png':
            if self.name == 'portail 1':
                self.rect.x = self.game.w // 1.1
                self.rect.y = self.game.h // 20 - 40
            elif self.name == 'portail 2':
                self.rect.x = self.game.w // 15
                self.rect.y = self.game.h // 3.5
            
        self.frame = 0
        # récupérer les images du portail
        self.images = portail

    def animate(self):
        """Animer le portail de téléportation"""
        # passer à l'image suivante
        self.frame += 1

        if self.frame >= len(self.images) * 5:
            self.frame = 0
        self.image = self.images[self.frame // 5]

def load_images(path_to_directory):
    """Load images and return them as a dict."""
    images = []
    for filename in os.listdir(path_to_directory):
        if filename.endswith('.png'):
            path = os.path.join(path_to_directory, filename)
            images.append(pygame.image.load(path))
            # enlever l'arriere plan qui peut être en noir
            images[-1].set_colorkey((0, 0, 0))
    return images

def load_images_sheet(sprite_sheet, frame_name):
    # recuperer les donnees du fichier '.json' où se trouvent les images
    data = sprite_sheet.get_data()
    # l'index sert pour le nom des frames (à la fin de chaque fichier)
    # exemple --> "dark_knight_static1", "dark_knight_static2", ...
    index = 1
    # ranger les images dans une liste
    images = []
    for key in data['frames'].keys():
        if frame_name == 'jump':
            # ne pas calculer 'double_jump'
            if 'double_jump' in key:
                pass
            elif frame_name in key:
                images.append(sprite_sheet.parse_sprite(frame_name + str(index)))
                index += 1
        else:
            if frame_name in key:
                images.append(sprite_sheet.parse_sprite(frame_name + str(index)))
                index += 1

    # renvoyer la liste d'image
    return images


# def load_perso(path_to_directory):
#     """Load image of the perso
#     Return a Dictionary with all characters of the game
#     """
#     images = {}
#     for filename in os.listdir(path_to_directory):
#         path = os.path.join(path_to_directory, filename)
#         # on enleve l'extension '.png' pour avoir le nom du perso
#         perso_name = filename.replace('.png', '')
#         # la valeur sera une liste
#         # --> (nécessaire pour le bon fonctionnement de la fonction 'redim_sprite')
#         images[perso_name] = [pygame.image.load(path)]
#         # print(images)
#         # images[perso_name] = redim_sprite(images[perso_name], origin_height_perso)
#     return images


def redim_sprite(sprite, height_sprite):
    """Redimensionner les images du sprite

    sprite: type(list)
    height_sprite: en pixel

    Pas besoin de retourner qqch car quand on fait une action en appelant le module 'pygame',
    il gère automatiquement son environnement/jeu
    --> les images sont donc bien redimensionnées après l'appel de la fonction
    """
    for i in range(len(sprite)):
        width = sprite[i].get_width()
        height = sprite[i].get_height()
        # arrondir le rapport à 1 chiffre apres la virgule
        rapport = round(height_sprite/height, 1)
        # le rapport sert à garder les proportion de l'image (avec tjs 50 pixels de hauteur)
        width *= rapport
        height *= rapport
        sprite[i] = pygame.transform.scale(sprite[i], (int(width), int(height)))
        # enlever l'arrière plan en noir
        sprite[i].set_colorkey((0, 0, 0))


def get_perso(anim_perso):
    """Retourne les persos

    seulement une image du perso
    --> [[0, image, name], [1, image, name], [2, image, name], ...]
    """
    # le dictionnaire va servir à savoir quel joueur a été choisi
    # dict_perso = {}
    persos = []
    n = 0
    for perso in anim_perso.keys():
        new_perso = []
        new_perso.append(n)
        # ajouter la première image static
        image = anim_perso[perso]['static'][0]
        width = image.get_width()
        height = image.get_height()
        # arrondir le rapport à 1 chiffre apres la virgule
        rapport = round(100 / height, 1)
        # le rapport sert à garder les proportion de l'image (avec tjs 50 pixels de hauteur)
        width *= rapport
        height *= rapport
        image = pygame.transform.scale(image, (int(width), int(height)))
        new_perso.append(image)
        # ajouter le nom du perso
        new_perso.append(perso)
        persos.append(new_perso)

    return persos

def get_projectile(anim_proj):
    """Retourne les projectiles

    seulement une image du projectile
    --> [[0, image, name], [1, image, name], [2, image, name], ...]
    """
    # le dictionnaire va servir à savoir quel joueur a été choisi
    # dict_perso = {}
    projectiles = []
    n = 0
    # récupérer le nom du projectile et son image
    for name, proj in anim_proj.items():
        new_proj = []
        new_proj.append(n)
        # ajouter la première image du projectile
        image = proj[0]
        width = image.get_width()
        height = image.get_height()
        # arrondir le rapport à 1 chiffre apres la virgule
        rapport = round(50 / height, 1)
        # le rapport sert à garder les proportion de l'image (avec tjs 50 pixels de hauteur)
        width *= rapport
        height *= rapport
        image = pygame.transform.scale(image, (int(width), int(height)))
        new_proj.append(image)
        # ajouter le nom du proj
        new_proj.append(name)
        projectiles.append(new_proj)

    return projectiles



dark_knight_sheet = Spritesheet("assets/knights/dark_knight/dark_knight_sheet.png")
blue_knight_sheet = Spritesheet("assets/knights/blue_knight/blue_knight_sheet.png")
gold_knight_sheet = Spritesheet("assets/knights/gold_knight/gold_knight_sheet.png")
red_knight_sheet = Spritesheet("assets/knights/red_knight/red_knight_sheet.png")

blue_dino_sheet = Spritesheet("assets/dino/blue_dino_sheet.png")
green_dino_sheet = Spritesheet("assets/dino/green_dino_sheet.png")
red_dino_sheet = Spritesheet("assets/dino/red_dino_sheet.png")
yellow_dino_sheet = Spritesheet("assets/dino/yellow_dino_sheet.png")

blue_guy_sheet = Spritesheet("assets/little_guys/blue_guy/blue_guy_sheet.png")
mask_guy_sheet = Spritesheet("assets/little_guys/mask_guy/mask_guy_sheet.png")
ninja_frog_sheet = Spritesheet("assets/little_guys/ninja_frog/ninja_frog_sheet.png")
pink_guy_sheet = Spritesheet("assets/little_guys/pink_guy/pink_guy_sheet.png")

"""
Definir un dictionnaire qui va contenir les images chargées de chaque joueur/sprite,
Ainsi que les images des projectiles.
Exemple --> 'blue_dino':
                'run': ['dino1.png', 'dino2.png', 'dino3.png', ...]
                'static': ['dino1.png', 'dino2.png', 'dino3.png', ...]
Chaque valeur est une liste (nécessaire pour le bon fonctionnement de la fonction 'redim_sprite')
"""
animations = {
    'persos': {
        'blue_dino': {
            'run': load_images_sheet(blue_dino_sheet, 'run'),
            'static': load_images_sheet(blue_dino_sheet, 'static'),
            'jump': load_images_sheet(blue_dino_sheet, 'jump'),
            'dead': load_images_sheet(blue_dino_sheet, 'dead')
        },
        'green_dino': {
            'run': load_images_sheet(green_dino_sheet, 'run'),
            'static': load_images_sheet(green_dino_sheet, 'static'),
            'jump': load_images_sheet(green_dino_sheet, 'jump'),
            'dead': load_images_sheet(green_dino_sheet, 'dead')
        },
        'red_dino': {
            'run': load_images_sheet(red_dino_sheet, 'run'),
            'static': load_images_sheet(red_dino_sheet, 'static'),
            'jump': load_images_sheet(red_dino_sheet, 'jump'),
            'dead': load_images_sheet(red_dino_sheet, 'dead')
        },
        'yellow_dino': {
            'run': load_images_sheet(yellow_dino_sheet, 'run'),
            'static': load_images_sheet(yellow_dino_sheet, 'static'),
            'jump': load_images_sheet(yellow_dino_sheet, 'jump'),
            'dead': load_images_sheet(yellow_dino_sheet, 'dead')
        },
        'blue_knight': {
            'run': load_images_sheet(blue_knight_sheet, 'blue_knight_run'),
            'static': load_images_sheet(blue_knight_sheet, 'blue_knight_static'),
            'jump': load_images_sheet(blue_knight_sheet, 'blue_knight_jump'),
            'attack': load_images_sheet(blue_knight_sheet, 'blue_knight_attack'),
            'shield': load_images_sheet(blue_knight_sheet, 'blue_knight_shield'),
            'dead': load_images_sheet(blue_knight_sheet, 'blue_knight_dead')
        },
        'dark_knight': {
            'run': load_images_sheet(dark_knight_sheet, 'dark_knight_run'),
            'static': load_images_sheet(dark_knight_sheet, 'dark_knight_static'),
            'jump': load_images_sheet(dark_knight_sheet, 'dark_knight_jump'),
            'attack': load_images_sheet(dark_knight_sheet, 'dark_knight_attack'),
            'shield': load_images_sheet(dark_knight_sheet, 'dark_knight_shield'),
            'dead': load_images_sheet(dark_knight_sheet, 'dark_knight_dead')
        },
        'red_knight': {
            'run': load_images_sheet(red_knight_sheet, 'red_knight_run'),
            'static': load_images_sheet(red_knight_sheet, 'red_knight_static'),
            'jump': load_images_sheet(red_knight_sheet, 'red_knight_jump'),
            'attack': load_images_sheet(red_knight_sheet, 'red_knight_attack'),
            'shield': load_images_sheet(red_knight_sheet, 'red_knight_shield'),
            'dead': load_images_sheet(red_knight_sheet, 'red_knight_dead')
        },
        'gold_knight': {
            'run': load_images_sheet(gold_knight_sheet, 'gold_knight_run'),
            'static': load_images_sheet(gold_knight_sheet, 'gold_knight_static'),
            'jump': load_images_sheet(gold_knight_sheet, 'gold_knight_jump'),
            'attack': load_images_sheet(gold_knight_sheet, 'gold_knight_attack'),
            'shield': load_images_sheet(gold_knight_sheet, 'gold_knight_shield'),
            'dead': load_images_sheet(gold_knight_sheet, 'gold_knight_dead')
        },
        'blue_guy': {
            'run': load_images_sheet(blue_guy_sheet, 'run'),
            'static': load_images_sheet(blue_guy_sheet, 'static'),
            'double_jump': load_images_sheet(blue_guy_sheet, 'double_jump'),
            'jump': load_images_sheet(blue_guy_sheet, 'jump'),
            'hit': load_images_sheet(blue_guy_sheet, 'hit')
        },
        'mask_guy': {
            'run': load_images_sheet(mask_guy_sheet, 'run'),
            'static': load_images_sheet(mask_guy_sheet, 'static'),
            'double_jump': load_images_sheet(mask_guy_sheet, 'double_jump'),
            'jump': load_images_sheet(mask_guy_sheet, 'jump'),
            'hit': load_images_sheet(mask_guy_sheet, 'hit')
        },
        'ninja_frog': {
            'run': load_images_sheet(ninja_frog_sheet, 'run'),
            'static': load_images_sheet(ninja_frog_sheet, 'static'),
            'double_jump': load_images_sheet(ninja_frog_sheet, 'double_jump'),
            'jump': load_images_sheet(ninja_frog_sheet, 'jump'),
            'hit': load_images_sheet(ninja_frog_sheet, 'hit')
        },
        'pink_guy': {
            'run': load_images_sheet(pink_guy_sheet, 'run'),
            'static': load_images_sheet(pink_guy_sheet, 'static'),
            'double_jump': load_images_sheet(pink_guy_sheet, 'double_jump'),
            'jump': load_images_sheet(pink_guy_sheet, 'jump'),
            'hit': load_images_sheet(pink_guy_sheet, 'hit')
        }
    },
    'projectiles': {
        'projectile': {
            'Bolt': load_images('assets/Shoot/Bolt/frames'),
            'Charged': load_images('assets/Shoot/Charged/frames'),
            'Crossed': load_images('assets/Shoot/Crossed/frames'),
            'Pulse': load_images('assets/Shoot/Pulse/frames'),
            'Spark': load_images('assets/Shoot/Spark/frames'),
            'Wave': load_images('assets/Shoot/Wave/frames')
        }
    },
    'huds': {
        'hud': {
            'heart': load_images('assets/hud/heart')
        }
    }
}

# definier la heuteur du personnage
origin_height_perso = 60

# charger le portail ainsi que ses images
portail = load_images('assets/portail')
redim_sprite(portail, origin_height_perso * 3)

# ####------------ Redimension de toutes les images des JOUEURS ------------####
# recuperer les donnes/images de n'importe quel JOUEUR
for key in animations['persos'].keys():
    height_perso = origin_height_perso
    # si c'est un chevalier on l'agrandit un peu plus par rapport au dino
    if 'knight' in key:
        height_perso *= 1

    # rentrer dans son dictionnaire pour avoir toutes ses images ('run', 'static', 'jump', ...)
    for img in animations['persos'][key].keys():
        if 'dino' in key and 'run' in img:
            height_perso = origin_height_perso
            # éviter que le dino ait une grosse tete quand il court
            height_perso //= 1.1
            redim_sprite(animations['persos'][key][img], height_perso)
        else:
            redim_sprite(animations['persos'][key][img], height_perso)

height_perso = origin_height_perso

# ####------------ Redimension de toutes les images des PROJECTILES ------------####
# recuperer les donnes/images de n'importe quel PROJECTILE
for key in animations['projectiles'].keys():
    # rentrer dans son dictionnaire pour avoir toutes ses images ('run', 'static', 'jump', ...)
    for img in animations['projectiles'][key].keys():
        redim_sprite(animations['projectiles'][key][img], height_perso // 1.5)
