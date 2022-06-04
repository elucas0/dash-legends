import pygame
import sys
from game import Game, EndGame
import random

# On initialise le jeu
pygame.init()
pygame.mixer.init()

# Génération de la fenêtre du jeu
pygame.display.set_caption("DashLegends")

# On met le jeu en plein écran et on détermine le nombre d'image par seconde maximum
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock() # 
FPS_MAX = 60 #On limite les images par seconde

# Ecran du menu
menu_bg = pygame.image.load(
    'assets/Background/menu/DashLegends.png').convert_alpha() # Permet de gagner des FPS
menu_bg = pygame.transform.scale(menu_bg, (1920, 1080)) # Mise à l'échelle

# Ecran de l'option (sans le logo)
option_bg = pygame.image.load(
    'assets/Background/menu/option_screen.png').convert_alpha()
option_bg = pygame.transform.scale(option_bg, (1920, 1080))

# Juste le logo (pour le jeu en pause)
logo = pygame.image.load('assets/Background/menu/logo.png').convert_alpha()
logo = pygame.transform.scale(logo, (1920//5, 1080//7))

# Mini-maps dans le menu de sélection
sunset_mountain = pygame.image.load(
    'assets/Background/sunset_mountain/mountain_preview.png').convert_alpha()
icy_arena = pygame.image.load(
    'assets/Background/icy_arena/arena_preview.png').convert_alpha()
neo_lagos = pygame.image.load(
    'assets/Background/neo_lagos/neo_preview.png').convert_alpha()

# Police d'écriture
font = pygame.font.SysFont("Montserrat", 50)
small_font = pygame.font.SysFont("Montserrat", 35)
pixel = pygame.font.Font("assets/Miscellaneous/Font/8-BIT WONDER.TTF", 20)
small_pixel = pygame.font.Font("assets/Miscellaneous/Font/8-BIT WONDER.TTF", 13)
symbol = pygame.font.SysFont("segoeuisymbol", 35)
bigsymbol = pygame.font.SysFont("segoeuisymbol", 55)

# Afin de pouvoir jouer plusieurs sons en même temps
pygame.mixer.set_num_channels(64)

# Musiques
pygame.mixer.music.load('assets/Music/menu_theme.mp3')
main_theme = pygame.mixer.Sound('assets/Music/main_theme.mp3')
over = pygame.mixer.Sound('assets/Music/game_over.mp3')

#Volume par défaut
volume = 0.2

pygame.mixer.music.set_volume(volume)
main_theme.set_volume(volume)
over.set_volume(volume)

#Jouer la musique à l'infini
pygame.mixer.music.play(-1)

# Effets
on_click = pygame.mixer.Sound('assets/Music/Sounds/click.wav')
on_back = pygame.mixer.Sound('assets/Music/Sounds/back.wav')
launch = pygame.mixer.Sound('assets/Music/Sounds/launch.wav')

# Volume
on_click.set_volume(0.1)
on_back.set_volume(0.2)
launch.set_volume(0.2)

# Image des touches
controle = pygame.image.load('assets/Miscellaneous/Option/controls.png')

# Initialisation d'une variable qui détermine si l'on clique
click = False
particles = []


def update_fps():
    """Affiche les images par seconde"""
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("white"))
    return fps_text


def draw_text(text, font, color, surface, button):
    """Permet d'afficher du texte facilement"""
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = button.center
    surface.blit(textobj, textrect)


def present_game_surface_on_screen(game_surface):
    """Redimensionne la surface prise en paramètre et la renvoie
    avec un ratio 16/9"""
    # Si l'écran a un ratio < 16/9
    if screen.get_width()/screen.get_height() < 16/9:
        # La largeur reste la même
        new_surface_width = screen.get_width()
        # Modification de la hauteur
        new_surface_height = int(screen.get_width() * 9/16)
    # Si l'écran a un ratio > 16/9
    else:
        # Modification de la Largeur
        new_surface_width = int(screen.get_height() * 16/9)
        # La hauteur reste la même
        new_surface_height = screen.get_height()
    # Surface finale redimensionnée au ratio 16/9
    new_surface = pygame.transform.scale(
        game_surface, (new_surface_width, new_surface_height))

    # Actualisation de l'écran
    screen.fill((0, 0, 0))
    # Centrage de la nouvelle surface
    screen.blit(new_surface, (screen.get_width()/2 - new_surface_width /
                2, screen.get_height()/2 - new_surface_height/2))

    # Mise à jour de l'écran
    pygame.display.flip()


def convert_screen_to_game_coordinates(coord):
    """Transforme des coordonees de la surface screen pour la surface du jeu"""
    # Reprise de la surface redimensionnée
    if screen.get_width()/screen.get_height() < 16/9:
        new_surface_width = screen.get_width()
        new_surface_height = int(screen.get_width() * 9/16)
    else:
        new_surface_width = int(screen.get_height() * 16/9)
        new_surface_height = screen.get_height()

    x, y = coord
    x -= screen.get_width()/2 - new_surface_width/2
    y -= screen.get_height()/2 - new_surface_height/2
    x = x / new_surface_width * 1920
    y = y / new_surface_height * 1080
    return x, y


def main_menu(click):
    """Menu principal"""
    menu_surface = pygame.Surface((1920, 1080))
    while True:
        present_game_surface_on_screen(menu_surface)
        # On fait apparaître l'image du menu
        menu_surface.blit(menu_bg, (0, 0))
        mx, my = convert_screen_to_game_coordinates(
            pygame.mouse.get_pos())  # Position de la souris


        color_play = (220, 139, 220)  # Couleur du bouton pour jouer
        color_options = (244, 187, 164)  # Couleur du bouton options
        color_quit = (255, 105, 97)  # Couleur du bouton pour quitter

        # On dessine les boutons
        play = pygame.Rect(1920/2-100, 1080/2, 200, 50)
        options = pygame.Rect(1920/2-100, 1080/2+100, 200, 50)
        quit = pygame.Rect(1920/2-100, 1080/2+200, 200, 50)

        # Détermine si la souris passe sur le bouton, si oui, les bords deviennent blanc
        if play.collidepoint((mx, my)):
            color_play = (255, 255, 255) # Changer les couleurs des boutons
            if click:  # Si le bouton est cliquer, démarrer le jeu
                on_click.play()
                choose(Game())
        elif options.collidepoint((mx, my)):
            color_options = (255, 255, 255)
            if click:
                # Si le bouton est cliquer aller à la page option
                on_click.play()
                option(volume)
        elif quit.collidepoint((mx, my)):
            color_quit = (255, 255, 255)
            if click:
                pygame.quit()       # Si le bouton est cliquer, quitter le menu
                sys.exit()

        # On affiche les boutons arrondies et le texte
        pygame.draw.rect(menu_surface, color_play, play, 3, border_radius=15)
        draw_text('Jouer', pixel, color_play, menu_surface, play)

        pygame.draw.rect(menu_surface, color_options,
                         options, 3, border_radius=15)
        draw_text('Options', pixel, color_options, menu_surface, options)

        pygame.draw.rect(menu_surface, color_quit, quit, 3, border_radius=15)
        draw_text('Quitter', pixel, color_quit, menu_surface, quit)


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN: #Si on appuie sur entrée
                    on_click.play()
                    choose(Game())
            if event.type == pygame.MOUSEBUTTONDOWN:  # Si on fais clic gauche
                if event.button == 1:
                    click = True

        pygame.display.update()


def option(volume):
    """Page option"""
    option_surface = pygame.Surface((1920, 1080))
    RUNNING = True
    while RUNNING:
        # On fait apparaître l'image du menu
        present_game_surface_on_screen(option_surface)
        mx, my = convert_screen_to_game_coordinates(
            pygame.mouse.get_pos())  # Position de la souris

        option_surface.blit(option_bg, (0, 0))

        control = pygame.Rect(1920/2, 1080/11, 0, 0)
        sound = pygame.Rect(1920/2, 1080/1.3, 0, 0)
        decrease = pygame.Rect(1920/2.2, 1080/1.2, 50, 50)
        increase = pygame.Rect(1920/1.9, 1080/1.2, 50, 50)
        show_volume = pygame.Rect(1920/2.05, 1080/1.2, 50, 50)
        back = pygame.Rect(1920/2-100, 1080/1.1, 200, 50)

        color_decrease = (255, 179, 71)
        color_increase = (176, 242, 182)
        color_back = (255, 105, 97)

        if back.collidepoint((mx, my)):
            color_back = (255, 255, 255)
            if click:
                on_back.play()
                RUNNING = False  # Retour à la page précédente

        elif decrease.collidepoint((mx, my)):
            # Diminuer le volume
            color_decrease = (255, 255, 255)
            if click and volume > 0:
                on_back.play()
                volume -= 0.1
                volume = round(volume, 1)
                pygame.mixer.music.set_volume(volume)
                main_theme.set_volume(volume)
                over.set_volume(volume)

        elif increase.collidepoint((mx, my)):
            #Augmenter le volume
            color_increase = (255, 255, 255)
            if click and volume < 1:
                on_back.play()
                volume += 0.1
                volume = round(volume, 1)
                pygame.mixer.music.set_volume(volume)
                main_theme.set_volume(volume)
                over.set_volume(volume)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    on_back.play()
                    RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        draw_text('Controles', pixel, (244, 187, 164),
                  option_surface, control)
        option_surface.blit(controle, (1920/50, 1080/4))

        draw_text('Sons', pixel, (244, 187, 164), option_surface, sound)
        pygame.draw.rect(option_surface, color_decrease,
                         decrease, 1, border_radius=15)
        draw_text('-', font, color_decrease, option_surface, decrease)

        pygame.draw.rect(option_surface, color_increase,
                         increase, 1, border_radius=15)
        draw_text('+', font, color_increase, option_surface, increase)

        pygame.draw.rect(option_surface, color_back, back, 3, border_radius=15)
        draw_text('Retour', pixel, color_back, option_surface, back)

        draw_text(f'{volume*100}%', small_font,
                  (255, 255, 255), option_surface, show_volume)
        pygame.display.update()


def pause(game, click):
    """Page de pause"""
    RUNNING = True
    while RUNNING:
        present_game_surface_on_screen(game.surface)
        # On affiche le logo sans changer le fond d'écran pour donner une impression d'arrête dans le temps
        game.surface.blit(
            logo, (1920/2-logo.get_rect().center[0], logo.get_rect().center[1]))

        mx, my = convert_screen_to_game_coordinates(
            pygame.mouse.get_pos())  # Position de la souris

        color_menu = (220, 139, 220)
        color_options = (244, 187, 164)  # Couleur du bouton option
        color_unpause = (238, 175, 178)

        menu = pygame.Rect(1920/2-100, 1080/2, 200, 50)
        options = pygame.Rect(1920/2-100, 1080/2+100, 200, 50)
        unpause = pygame.Rect(1920/2-100, 1080/2+200, 200, 50)
        

        if menu.collidepoint((mx, my)):
            color_menu = (255, 255, 255)
            if click:
                pygame.mixer.stop()
                on_back.play()
                pygame.mixer.music.play(-1)
                main_menu(click=False)  # Retour au menu principal
        elif options.collidepoint((mx, my)):
            color_options = (255, 255, 255)
            if click:
                # Si le bouton est cliquer aller à la page option
                on_click.play()
                option(volume)
        if unpause.collidepoint((mx, my)):
            color_unpause = (255, 255, 255)
            if click:
                on_click.play()
                pygame.mixer.unpause()
                RUNNING = False         # Retour au jeu

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Si on appuie sur Echap, on retourne au jeu
                    on_click.play()
                    pygame.mixer.unpause()
                    RUNNING = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.draw.rect(game.surface, color_unpause,
                         unpause, 3, border_radius=15)
        draw_text('Retour', pixel, color_unpause, game.surface, unpause)
        pygame.draw.rect(game.surface, color_menu, menu, 3, border_radius=15)
        draw_text('Options', pixel, color_options, game.surface, options)
        pygame.draw.rect(game.surface, color_options,
                         options, 3, border_radius=15)
        draw_text('Menu principal', small_pixel,
                  color_menu, game.surface, menu)

        pygame.display.update()


def choose(game):
    """Choisir les personnages ainsi que les projectiles"""
    select = 'arena'
    choose_surface = pygame.Surface((1920, 1080))
    RUNNING = True
    while RUNNING:
        present_game_surface_on_screen(choose_surface)

        choose_surface.blit(option_bg, (0, 0))
        
        # choisir les joueurs et les projectiles
        game.choose_players(choose_surface, 1920, 1080)
        game.choose_proj(choose_surface, 1920, 1080)

        mx, my = convert_screen_to_game_coordinates(
            pygame.mouse.get_pos())  # Position de la souris

        # Texte et les 2 boutons
        choose_player = pygame.Rect(1920/2-100, 1080/10, 200, 50)
        menu = pygame.Rect(1920/15-100, 1080/40, 100, 45)
        lessgo = pygame.Rect(1920/2 - 100, 1080 - 1080/5, 200, 50)

        # Rectangles de selection autour des maps
        map1_rect = pygame.Rect(1920-10-sunset_mountain.get_width(), 1080-10-sunset_mountain.get_height(),
                           sunset_mountain.get_width(), sunset_mountain.get_height())
        map2_rect = pygame.Rect(1920-10-icy_arena.get_width(), 1080/1.2-10-icy_arena.get_height(),
                           icy_arena.get_width(), icy_arena.get_height())
        map3_rect = pygame.Rect(1920-10-neo_lagos.get_width(), 1080/1.5-10-neo_lagos.get_height(),
                           neo_lagos.get_width(), neo_lagos.get_height())

        # Grand rectangle des joueurs et des projectiles
        player1 = pygame.Rect(1920/2-450, 1080/3.5, 250, 400)
        player2 = pygame.Rect(1920/2 + 200, 1080/3.5, 250, 400)
        choose_proj1 = pygame.Rect(1920/2 - 425, 1080/1.5, 200, 50)
        choose_proj2 = pygame.Rect(1920/2 + 225, 1080/1.5, 200, 50)

        # Flèches pour sélectionner
        player1_l = pygame.Rect(1920/2-500, 1080/2.25, 30, 30)
        player1_r = pygame.Rect(1920/2-185, 1080/2.25, 30, 30)

        player2_l = pygame.Rect(1920/2+150, 1080/2.25, 30, 30)
        player2_r = pygame.Rect(1920/2+470, 1080/2.25, 30, 30)
        
        proj1_l = pygame.Rect(1920/2 - 460, 1080/1.48, 30, 30)
        proj1_r = pygame.Rect(1920/2 - 220, 1080/1.48, 30, 30)
        
        proj2_l = pygame.Rect(1920/2+190, 1080/1.48, 30, 30)
        proj2_r = pygame.Rect(1920/2 + 430, 1080/1.48, 30, 30)

        # Couleur des boutons
        color_menu = (255, 209, 220)  # Retour en arrière
        color_lessgo = (220, 139, 220)  # Bouton pour jouer
        color_rect_map_1 = (255, 255, 255)
        color_rect_map_2 = (255, 255, 255)
        color_rect_map_3 = (255, 255, 255)
        player1_l_color = (255, 255, 255)  # Flèches
        player1_r_color = (255, 255, 255)
        player2_l_color = (255, 255, 255)
        player2_r_color = (255, 255, 255)
        proj1_l_color = (255, 255, 255)
        proj1_r_color = (255, 255, 255)
        proj2_l_color = (255, 255, 255)
        proj2_r_color = (255, 255, 255)

        # Collisions avec les boutons
        if menu.collidepoint((mx, my)):
            color_menu = (255, 255, 255)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                on_back.play()
                main_menu(click=False)

        if lessgo.collidepoint((mx, my)):
            color_lessgo = (255, 255, 255)
            if click:  # Si le bouton est cliquer, démarrer le jeu avec les persos et les projectiles chosisi
                pygame.mixer.music.fadeout(1000)
                launch.play()
                main_theme.play(loops=-1)
                name_player_1, name_player_2 = game.get_name_players()
                name_proj_1, name_proj_2 = game.get_name_proj()
                ingame(Game(name_player_1, name_player_2, name_proj_1, name_proj_2, map_background), name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)

        if map1_rect.collidepoint((mx, my)):
            color_rect_map_1 = (255, 105, 97)
            if click:
                select = 'mountain'

        if map2_rect.collidepoint((mx, my)):
            color_rect_map_2 = (255, 105, 97)
            if click:
                select = 'arena'

        if map3_rect.collidepoint((mx, my)):
            color_rect_map_3 = (255, 105, 97)
            if click:
                select = 'neo'

        if player1_l.collidepoint((mx, my)):
            player1_l_color = (220, 139, 220)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                game.perso_at_left(True, False)
                on_click.play()

        elif player1_r.collidepoint((mx, my)):
            player1_r_color = (220, 139, 220)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                game.perso_at_right(True, False)
                on_click.play()

        elif player2_l.collidepoint((mx, my)):
            player2_l_color = (220, 139, 220)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                game.perso_at_left(False, True)
                on_click.play()

        elif player2_r.collidepoint((mx, my)):
            player2_r_color = (220, 139, 220)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                game.perso_at_right(False, True)
                on_click.play()
                
        elif proj1_l.collidepoint((mx, my)):
            proj1_l_color = (220, 139, 220)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                game.proj_at_left(True, False)
                on_click.play()
                
        elif proj1_r.collidepoint((mx, my)):
            proj1_r_color = (220, 139, 220)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                game.proj_at_right(True, False)
                on_click.play()
                
        elif proj2_l.collidepoint((mx, my)):
            proj2_l_color = (220, 139, 220)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                game.proj_at_left(False, True)
                on_click.play()
                
        elif proj2_r.collidepoint((mx, my)):
            proj2_r_color = (220, 139, 220)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                game.proj_at_right(False, True)
                on_click.play()
        
        # Texte
        draw_text("Choisissez votre personnage",
                  pixel, (255, 209, 220), choose_surface, choose_player)

        # Boutons
        pygame.draw.rect(choose_surface, color_menu, menu, 1, border_radius=15)
        draw_text('←', bigsymbol, color_menu, choose_surface, menu)

        pygame.draw.rect(choose_surface, color_lessgo,
                         lessgo, 1, border_radius=15)
        draw_text("C'est parti !", small_font,
                  color_lessgo, choose_surface, lessgo)


        draw_text("◀", symbol, player1_l_color, choose_surface, player1_l)
        pygame.draw.rect(choose_surface, (255, 255, 255),
                         player1, 2, border_radius=15)
        draw_text("▶",
                  symbol, player1_r_color, choose_surface, player1_r)
        
        
        draw_text("◀", symbol, proj1_l_color, choose_surface, proj1_l)
        pygame.draw.rect(choose_surface, (255, 255, 255),
                         choose_proj1, 2, border_radius=15)
        draw_text("▶", symbol, proj1_r_color, choose_surface, proj1_r)


        draw_text("◀",
                  symbol, player2_l_color, choose_surface, player2_l)
        pygame.draw.rect(choose_surface, (255, 255, 255),
                         player2, 2, border_radius=15)
        draw_text("▶",
                  symbol, player2_r_color, choose_surface, player2_r)
        
        draw_text("◀", symbol, proj2_l_color, choose_surface, proj2_l)
        pygame.draw.rect(choose_surface, (255, 255, 255),
                         choose_proj2, 2, border_radius=15)
        draw_text("▶", symbol, proj2_r_color, choose_surface, proj2_r)

        # Maps
        if select == 'mountain':
            color_rect_map_1 = (255, 105, 97)
            map_background = 'assets/Background/sunset_mountain/mountain.png'
        elif select == 'arena':
            color_rect_map_2 = (255, 105, 97)
            map_background = 'assets/Background/icy_arena/arena.png'
        else :
            color_rect_map_3 = (255, 105, 97)
            map_background = 'assets/Background/neo_lagos/neo.png'

        #Boutons de sélection des maps :

        #Map sunset mountain
        choose_surface.blit(
            sunset_mountain, (1920-10-sunset_mountain.get_width(), 1080-10-sunset_mountain.get_height()))
        pygame.draw.rect(choose_surface, color_rect_map_1, map1_rect, 1)

        #Map icy arena
        choose_surface.blit(
            icy_arena, (1920-10-icy_arena.get_width(), 1080/1.2-10-icy_arena.get_height()))
        pygame.draw.rect(choose_surface, color_rect_map_2, map2_rect, 1)

        #Map neo lagos
        choose_surface.blit(
            neo_lagos, (1920-10-neo_lagos.get_width(), 1080/1.5-10-neo_lagos.get_height()))
        pygame.draw.rect(choose_surface, color_rect_map_3, map3_rect, 1)


        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # ajouter la touche pressee dans le dictionnaire de la classe Game
                # détecter les touches appuyées
                game.pressed[event.key] = True
                game.change_perso_keyboard()

                if event.key == pygame.K_ESCAPE:
                    on_back.play()
                    RUNNING = False
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.fadeout(1000)
                    launch.play()
                    main_theme.play(loops=-1)
                    name_player_1, name_player_2 = game.get_name_players()
                    name_proj_1, name_proj_2 = game.get_name_proj()
                    ingame(Game(name_player_1, name_player_2, name_proj_1, name_proj_2, map_background), name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)

            if event.type == pygame.MOUSEBUTTONDOWN:  # Si on fais clic gauche
                if event.button == 1:
                    click = True

            # detecter si un joueur lache une touche du clavier
            if event.type == pygame.KEYUP:
                game.pressed[event.key] = False

        pygame.display.update()


def ingame(game, name_player_1, name_player_2, name_proj_1, name_proj_2, map_background):
    """Fonction du jeu qui capte les touches enfoncées"""
    RUNNING = True
    while RUNNING:

        # dt = 1 pour 60 fps (fps max)
        dt = clock.tick(60) * .001 * FPS_MAX
        # dt ne peut pas aller au delà de 3
        dt = min(dt, 3)
        # Rafraichir
        check_1, check_2 = game.update(dt)

        present_game_surface_on_screen(game.surface)
        # Affiche les ips
        screen.blit(update_fps(), (10, 0))

        # Mise à jour de l'écran
        pygame.display.flip()

        # 'pygame.event.get()' --> retourne une liste d'evenement
        for event in pygame.event.get():
            # Si on ferme la fenêtre du jeu
            if event.type == pygame.QUIT:
                RUNNING = False

            # detecter si un joueur appuye une touche du clavier
            if event.type == pygame.KEYDOWN:
                # ajouter la touche pressee dans le dictionnaire de la classe Game
                # avec comme cle 'True', pour savoir si le joueur veut se deplacer à gauche ou à droite (entre autre)
                game.pressed[event.key] = True

                # Si le joueur appuie sur Echap pour fermer le jeu
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.pause()
                    on_click.play()
                    pause(game, click=False)

            # detecter si un joueur lache une touche du clavier
            if event.type == pygame.KEYUP:
                game.pressed[event.key] = False

        if check_1:
            # Si le joueur 2 a perdu
            pygame.mixer.stop()
            over.play(loops=-1, fade_ms=5000)
            RUNNING = False
            end_game = EndGame("Joueur 1", "Joueur 2",
                               name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)
            game_over("Joueur 1", end_game, name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)
        elif check_2:
            # Si le joueur 1 à perdu
            pygame.mixer.stop()
            over.play(loops=-1, fade_ms=5000)
            RUNNING = False
            end_game = EndGame("Joueur 2", "Joueur 1",
                               name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)
            game_over("Joueur 2", end_game, name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)


def game_over(player, end_game, name_player_1, name_player_2, name_proj_1, name_proj_2, map_background):
    """Fonction de fin lorsque un joueur est vaincu"""
    gameover_surface = pygame.Surface((1920, 1080))
    RUNNING = True
    click = False
    while RUNNING:
        present_game_surface_on_screen(gameover_surface)
        # On fait apparaître l'image du menu
        gameover_surface.blit(option_bg, (0, 0))

        # Animer les personnages
        end_game.animate()
        end_game.moving_sprites.draw(gameover_surface)

        mx, my = convert_screen_to_game_coordinates(
          pygame.mouse.get_pos())  # Position de la souris

        # Particules qui se déplacent différement et de taille différente
        particles.append(
        [[1920/3, 1080/2.5], [random.randint(0, 30) / 10 - 5, -2], random.randint(6, 11)])

        particles.append(
        [[1920/1.5, 1080/2.5], [random.randint(0, 30) / 10-5, -2], random.randint(6, 11)])

        winner = pygame.Rect(1920/2-100, 1080/2.5, 200, 50)
        menu = pygame.Rect(1920/2-300, 1080 - 1080/5, 200, 50)
        replay = pygame.Rect(1920/2+100, 1080 - 1080/5, 200, 50)

        color_menu = (244, 187, 164)  # Couleur du bouton menu
        color_replay = (220, 139, 220)  # Couleur du bouton pour rejouer
        color_gold = (239, 199, 121)

        if menu.collidepoint((mx, my)):
            color_menu = (255, 255, 255)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                on_back.play()
                pygame.mixer.stop()
                pygame.mixer.music.play(-1)
                main_menu(click=False)

        if replay.collidepoint((mx, my)):
            color_replay = (255, 255, 255)
            if click:  # Si le bouton est cliquer, démarrer le jeu
                launch.play()
                pygame.mixer.stop()
                main_theme.play(loops=-1)
                ingame(Game(name_player_1, name_player_2, name_proj_1, name_proj_2, map_background), name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)

        draw_text(f"Le {player} remporte la DashVictoire",
                  pixel, (239, 199, 121), gameover_surface, winner)

        pygame.draw.rect(gameover_surface, color_menu, menu, 3, border_radius=15)
        draw_text('Menu principal', small_pixel,
                  color_menu, gameover_surface, menu)

        pygame.draw.rect(gameover_surface, color_replay,
                         replay, 3, border_radius=15)
        draw_text('Rejouer', pixel, color_replay, gameover_surface, replay)

        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.05
            #particle[1][1] -= 0.1
            pygame.draw.circle(gameover_surface, color_gold, [int(
                particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                particles.remove(particle)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    launch.play()
                    pygame.mixer.stop()
                    main_theme.play(loops=-1)
                    ingame(Game(name_player_1, name_player_2, name_proj_1, name_proj_2, map_background), name_player_1, name_player_2, name_proj_1, name_proj_2, map_background)
            if event.type == pygame.MOUSEBUTTONDOWN:  # Si on fais clic gauche
                if event.button == 1:
                    click = True

        pygame.display.update()


# Appel du menu principal
main_menu(click)
