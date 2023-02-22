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

# Функция, загружающая изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('sprites', name)
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
    return pygame.font.Font("sprites/buttons/font.ttf", size)

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
        self.tiles = 3

    def main_menu(self):
        screen.fill('black')

        mouse_pos = pygame.mouse.get_pos()

        title = get_font(75).render("STARWALKER", True, "#b68f40")
        title_rect = title.get_rect(center=(400, 150))

        play_btn = Button(image=pygame.image.load("sprites/buttons/Play Rect.png"), pos=(400, 350),
                             text_input="PLAY", font=get_font(60), base_color="White", hovering_color="#b68f40")
        options_btn = Button(image=pygame.image.load("sprites/buttons/Options Rect.png"), pos=(400, 500),
                                text_input="OPTIONS", font=get_font(60), base_color="White", hovering_color="#b68f40")
        quit_btn = Button(image=pygame.image.load("sprites/buttons/Quit Rect.png"), pos=(400, 650),
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
                    self.state = 'main_game'
                if options_btn.checkForInput(mouse_pos):
                    self.state = 'options'
                if quit_btn.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

    def options(self):
        screen.fill('black')

        mouse_pos = pygame.mouse.get_pos()

        option_title = get_font(50).render("OPTIONS", True, "White")
        options_rect = option_title.get_rect(center=(400, 75))
        screen.blit(option_title, options_rect)

        back_btn = Button(image=None, pos=(400, 725),
                          text_input="BACK", font=get_font(75), base_color="White", hovering_color="#b68f40")

        back_btn.changeColor(mouse_pos)
        back_btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.checkForInput(mouse_pos):
                    self.state = 'main_menu'

        pygame.display.flip()

    # Функция, отвечающая за экран игры
    def main_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_ESCAPE]:
            self.state = 'main_menu'

        ship.update(self.keys)

        # Двигаем задний фон
        screen.fill('black')
        for i in range(0, self.tiles):
            screen.blit(bg, (0, bg_h * i - 2000 + self.scroll))

        self.scroll += 5

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


# Класс, отвечающий за действия и отображение игрока
class Player(pygame.sprite.Sprite):
    image = load_image("player_ship/player_ship_1.png")
    image2 = load_image("player_ship/player_ship_2.png")
    image = pygame.transform.scale(image, (50, 50))
    image2 = pygame.transform.scale(image2, (50, 50))
    laser_sfx = pygame.mixer.Sound("sprites/spaceship shooter music/laser.wav")

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

        if game_state.keys[pygame.K_w]:
            self.rect.y -= self.speedy
        elif game_state.keys[pygame.K_s]:
            self.rect.y += self.speedy

        if game_state.keys[pygame.K_a]:
            self.rect.x -= self.speedx
        elif game_state.keys[pygame.K_d]:
            self.rect.x += self.speedx

        if game_state.keys[pygame.K_SPACE]:
            self.reload += self.shooting_speed

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
