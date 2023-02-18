import os
import sys
import math

import pygame

# Размеры окна
SIZE = WIDTH, HEIGHT = 500, 500

# Создание окна
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('StarWalker')

# Задаем fps
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

# Класс, отвечающий за действия и отображение игрока
class Player(pygame.sprite.Sprite):
    image = load_image("player_ship/player_ship_1.png")
    image2 = load_image("player_ship/player_ship_2.png")
    image = pygame.transform.scale(image, (50, 50))
    image2 = pygame.transform.scale(image2, (50, 50))

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
        self.speedx = 4
        self.speedy = 4

    def shoot(self):
        return Bullet(*self.rect.midtop)

    def update(self, *args):
        self.current_sprite += self.animation_speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        if keys[pygame.K_w]:
            self.rect.y -= self.speedy
        elif keys[pygame.K_s]:
            self.rect.y += self.speedy

        if keys[pygame.K_a]:
            self.rect.x -= self.speedx
        elif keys[pygame.K_d]:
            self.rect.x += self.speedx

        if keys[pygame.K_SPACE]:
            self.reload += self.shooting_speed

            if int(self.reload):
                bullet_group.add(self.shoot())
                self.reload = 0

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


# Загружаем задний фон
bg = load_image("backgrounds/shooting_stars.png")
bg_h = bg.get_height()
scroll = 0
tiles = 3

# Создаем группы спрайтов
player_group = pygame.sprite.Group()
ship = Player(player_group)

bullet_group = pygame.sprite.Group()


running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    ship.update(keys)

    # Двигаем задний фон
    screen.fill('black')
    for i in range(0, tiles):
        screen.blit(bg, (0, bg_h * i - 2000 + scroll))

    scroll += 5

    if abs(scroll) > bg_h:
        scroll = 0

    # Отрисовываем группы спрайтов и обновляем экран
    player_group.draw(screen)
    bullet_group.draw(screen)
    bullet_group.update()
    pygame.display.flip()
pygame.quit()
