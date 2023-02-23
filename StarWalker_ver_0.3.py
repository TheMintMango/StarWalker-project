import os
import sys
import math

import pygame

# Окно и экран
SIZE = WIDTH, HEIGHT = 800, 800 # Размеры окна

screen = pygame.display.set_mode(SIZE)  # Создание окна
pygame.display.set_caption('StarWalker')

# Задаем fps
pygame.init()
clock = pygame.time.Clock()
FPS = 60
sfx_volume = 1
music_volume = 0.5

# Функция, загружающая изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('assets', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

# Возвращает шрифт заданного размера
def get_font(size):
    return pygame.font.Font("assets/buttons/font.ttf", size)

# Создает кнопки, обрабатывает нажатия и наведение на кнопки
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


# Переключает и отрисовывает игровые экраны
class GameState():
    def __init__(self):
        self.state = 'main_menu'

        self.scroll = 0
        self.tiles = 2

        self.show_htp = True
        self.start_music = True

    def main_menu(self):
        screen.fill('black')

        mouse_pos = pygame.mouse.get_pos()

        title = get_font(75).render("STARWALKER", True, "#b68f40")
        title_rect = title.get_rect(center=(400, 150))

        play_btn = Button(image=pygame.image.load("assets/buttons/Play Rect.png"), pos=(400, 350),
                             text_input="PLAY", font=get_font(60), base_color="White", hovering_color="#b68f40")
        options_btn = Button(image=pygame.image.load("assets/buttons/Options Rect.png"), pos=(400, 500),
                                text_input="OPTIONS", font=get_font(60), base_color="White", hovering_color="#b68f40")
        quit_btn = Button(image=pygame.image.load("assets/buttons/Quit Rect.png"), pos=(400, 650),
                             text_input="QUIT", font=get_font(60), base_color="White", hovering_color="#b68f40")

        screen.blit(title, title_rect)

        for button in [play_btn, options_btn, quit_btn]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.checkForInput(mouse_pos):
                    if self.show_htp:
                        self.state = 'how_to_play_mm'
                        self.show_htp = False
                    else:
                        self.state = 'main_game'
                if options_btn.checkForInput(mouse_pos):
                    self.state = 'options'
                if quit_btn.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

    def options(self):
        global music_volume, sfx_volume
        screen.fill('black')

        mouse_pos = pygame.mouse.get_pos()

        option_title = get_font(50).render("OPTIONS", True, "White")
        options_rect = option_title.get_rect(center=(400, 50))

        music_text = get_font(40).render("MUSIC", True, "White")
        music_rect = music_text.get_rect(center=(225, 175))
        sfx_text = get_font(40).render("SFX", True, "White")
        sfx_rect = sfx_text.get_rect(center=(225, 275))

        music_volume_text = get_font(40).render(str(int(music_volume * 10) * 10) + "%", True, "White")
        music_volume_rect = music_volume_text.get_rect(center=(525, 175))
        sfx_volume_text = get_font(40).render(str(int(sfx_volume * 10) * 10) + "%", True, "White")
        sfx_volume_rect = sfx_volume_text.get_rect(center=(525, 275))

        screen.blit(option_title, options_rect)
        screen.blit(music_text, music_rect)
        screen.blit(sfx_text, sfx_rect)
        screen.blit(music_volume_text, music_volume_rect)
        screen.blit(sfx_volume_text, sfx_volume_rect)


        back_btn = Button(image=None, pos=(200, 725),
                          text_input="BACK", font=get_font(60), base_color="White", hovering_color="#b68f40")
        htp_btn = Button(image=None, pos=(320, 625),
                         text_input="HOW TO PLAY?", font=get_font(40), base_color="White", hovering_color="#b68f40")

        music_volume_up = Button(image=None, pos=(625, 175),
                          text_input=">", font=get_font(40), base_color="White", hovering_color="#b68f40")
        music_volume_down = Button(image=None, pos=(425, 175),
                         text_input="<", font=get_font(40), base_color="White", hovering_color="#b68f40")
        sfx_volume_up = Button(image=None, pos=(625, 275),
                          text_input=">", font=get_font(40), base_color="White", hovering_color="#b68f40")
        sfx_volume_down = Button(image=None, pos=(425, 275),
                         text_input="<", font=get_font(40), base_color="White", hovering_color="#b68f40")

        for button in [back_btn, htp_btn, music_volume_up, music_volume_down, sfx_volume_up, sfx_volume_down]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.checkForInput(mouse_pos):
                    self.state = 'main_menu'
                if htp_btn.checkForInput(mouse_pos):
                    self.state = 'how_to_play_opt'
                if music_volume_up.checkForInput(mouse_pos) and music_volume < 1:
                    music_volume = round(music_volume + 0.1, 1)
                if music_volume_down.checkForInput(mouse_pos) and music_volume >= 0.1:
                    music_volume = round(music_volume - 0.1, 1)
                if sfx_volume_up.checkForInput(mouse_pos) and sfx_volume < 1:
                    sfx_volume = round(sfx_volume + 0.1, 1)
                if sfx_volume_down.checkForInput(mouse_pos) and sfx_volume >= 0.1:
                    sfx_volume = round(sfx_volume - 0.1, 1)

        pygame.display.flip()

    def how_to_play(self, previous_screen):

        mouse_pos = pygame.mouse.get_pos()

        screen.fill('black')

        htp_title = get_font(50).render("HOW TO PLAY", True, "White")
        htp_rect = htp_title.get_rect(center=(400, 75))

        movement_text = get_font(25).render("Press WASD to move", True, "White")
        movement_rect = movement_text.get_rect(center=(400, 225))

        shoot_text = get_font(25).render("Press SPACE to shoot", True, "White")
        shoot_rect = shoot_text.get_rect(center=(400, 300))

        exit_text = get_font(25).render("Press ESC to end current", True, "White")
        exit_rect = exit_text.get_rect(center=(400, 375))
        exit_text_2 = get_font(25).render("run and return to main menu", True, "White")
        exit_rect_2 = exit_text.get_rect(center=(365, 410))

        if previous_screen == 'main_menu':
            play_btn = Button(image=pygame.image.load("assets/buttons/Play Rect.png"), pos=(600, 700),
                              text_input="PLAY", font=get_font(60), base_color="White", hovering_color="#b68f40")
            back_btn = Button(image=pygame.image.load("assets/buttons/Play Rect.png"), pos=(200, 700),
                              text_input="BACK", font=get_font(60), base_color="White", hovering_color="#b68f40")
        elif previous_screen == 'options':
            back_btn = Button(image=pygame.image.load("assets/buttons/Play Rect.png"), pos=(400, 700),
                              text_input="BACK", font=get_font(60), base_color="White", hovering_color="#b68f40")


        if previous_screen == 'main_menu':
            for button in [play_btn, back_btn]:
                button.changeColor(mouse_pos)
                button.update(screen)
        elif previous_screen == 'options':
            back_btn.changeColor(mouse_pos)
            back_btn.update(screen)

        screen.blit(htp_title, htp_rect)
        screen.blit(movement_text, movement_rect)
        screen.blit(shoot_text, shoot_rect)
        screen.blit(exit_text, exit_rect)
        screen.blit(exit_text_2, exit_rect_2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if previous_screen == 'main_menu':
                    if play_btn.checkForInput(mouse_pos):
                        self.state = 'main_game'
                    if back_btn.checkForInput(mouse_pos):
                        self.state = previous_screen
                        self.show_htp = True
                elif previous_screen == 'options':
                    if back_btn.checkForInput(mouse_pos):
                        self.state = previous_screen


        pygame.display.flip()


    # Метод, отвечающий за экран игры
    def main_game(self):
        if self.start_music:
            pygame.mixer.music.load("assets/sound/spaceship shooter .wav")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(music_volume)
            self.start_music = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_ESCAPE]:
            pygame.mixer.music.unload()
            self.start_music = True
            self.state = 'main_menu'

        ship.update(self.keys)

        # Двигаем задний фон
        screen.fill('black')
        for i in range(0, self.tiles):
            screen.blit(bg, (0, bg_h * i - 2000 + self.scroll))

        self.scroll += 4

        if abs(self.scroll) > bg_h:
            self.scroll = 0

        player_group.draw(screen)
        bullet_group.draw(screen)
        bullet_group.update()
        pygame.display.flip()

    def state_manager(self):
        if self.state == 'main_menu':
            self.main_menu()
        elif self.state == 'main_game':
            self.main_game()
        elif self.state == 'options':
            self.options()
        elif self.state == 'how_to_play_mm':
            self.how_to_play('main_menu')
        elif self.state == 'how_to_play_opt':
            self.how_to_play('options')


# Класс, отвечающий за действия и отображение игрока
class Player(pygame.sprite.Sprite):
    image = load_image("player_ship/player_ship_1.png")
    image2 = load_image("player_ship/player_ship_2.png")
    image = pygame.transform.scale(image, (50, 50))
    image2 = pygame.transform.scale(image2, (50, 50))
    laser_sfx = pygame.mixer.Sound("assets/sound/laser.wav")

    def __init__(self, *group):
        super().__init__(*group)
        self.sprites = []
        self.sprites.append(Player.image)
        self.sprites.append(Player.image2)
        self.current_sprite = 0
        self.animation_speed = 0.3
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.x = 225
        self.rect.y = 225

        self.shooting_speed = 0.1
        self.reload = 0
        self.speedx = 5
        self.speedy = 5

    def shoot(self):
        return Bullet(*self.rect.midtop)

    def update(self, *args):
        self.current_sprite += self.animation_speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        if game_state.keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speedy
        elif game_state.keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speedy

        if game_state.keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speedx
        elif game_state.keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speedx

        if game_state.keys[pygame.K_SPACE]:
            self.reload += self.shooting_speed
            self.laser_sfx.set_volume(sfx_volume)

            if int(self.reload):
                bullet_group.add(self.shoot())
                self.reload = 0
                self.laser_sfx.play()

# Снаряды, которыми стреляет игрок
class Bullet(pygame.sprite.Sprite):
    image = load_image("projectiles/small_projectile_1.png")
    image = pygame.transform.scale(image, (10, 16))

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = Bullet.image
        self.rect = self.image.get_rect(center = (pos_x,pos_y))

    def update(self):
        self.rect.y -= 10

# Игровой сетап
game_state = GameState()

bg = load_image("backgrounds/bg_stars.png") # Загружаем задний фон
bg_h = bg.get_height()

# Создаем группы спрайтов
player_group = pygame.sprite.Group()
ship = Player(player_group)

bullet_group = pygame.sprite.Group()

running = True
while running:
    clock.tick(FPS)

    game_state.state_manager()
