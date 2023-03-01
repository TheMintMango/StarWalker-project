import os
import sys
from math import sin
import random
import csv, operator

import pygame

# Окно и экран
SIZE = WIDTH, HEIGHT = 800, 800 # Размеры окна

screen = pygame.display.set_mode(SIZE)  # Создание окна
pygame.display.set_caption('StarWalker')

# Задаем fps
pygame.init()
clock = pygame.time.Clock()
FPS = 60

# Проверяем существует ли файл настроек, если нет, то создаем
if not os.path.isfile('settings.csv'):
    with open("settings.csv", "w", encoding="utf8", newline='') as settings:
        writer = csv.writer(settings)
        writer.writerow(('1', '1'))

with open("settings.csv", encoding="utf8") as settings:
    reader = csv.reader(settings, delimiter=",", quotechar='"')
    music_volume, sfx_volume = map(lambda x: float(x), (list(reader))[0])

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

        self.kill_counter = 0
        self.next_drop = 0
        self.start = 0
        self.spawn_delay = 0
        self.difficulty = 0

        self.show_htp = True
        self.first_loop = True

        self.player_name = ""

        self.UI = UI(screen)
        pygame.mouse.set_visible(False)

        if not os.path.isfile('leaderboard.csv'):
            with open("leaderboard.csv", "w", encoding="utf8", newline='') as leaderboard:
                writer = csv.writer(leaderboard)

    # Главное меню
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

        self.UI.update()

        pygame.display.flip()

    # Меню настроек
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'main_menu'

        with open("settings.csv", "w", encoding="utf8", newline='') as settings:
            writer = csv.writer(settings)
            writer.writerow((str(music_volume), str(sfx_volume)))

        self.UI.update()

        pygame.display.flip()

    # Экран с обучением
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if previous_screen == 'main_menu':
                        self.show_htp = True
                        self.state = previous_screen
                    else:
                        self.state = previous_screen

        self.UI.update()

        pygame.display.flip()

    # Метод, отвечающий за основную игры
    def main_game(self):
        if self.first_loop:
            pygame.mixer.music.load("assets/sound/spaceship shooter .wav")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(music_volume)
            ship.rect.y = 350
            ship.rect.x = 350
            ship.score = 0
            self.kill_counter = 0
            self.next_drop = random.randint(20, 30)
            self.start = 0
            self.difficulty = 0
            self.spawn_delay = 5000
            self.player_name = ""
            self.first_loop = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_ESCAPE]:
            self.state = 'game_over'

        ship.update(self.keys)

        # Двигаем задний фон
        screen.fill('black')
        for i in range(0, self.tiles):
            screen.blit(bg, (0, bg_h * i - 2000 + self.scroll))

        self.scroll += 4

        if abs(self.scroll) > bg_h:
            self.scroll = 0

        now = pygame.time.get_ticks()

        if len(enemy_group) <= 9 and now - self.start > self.spawn_delay:
            self.start = now
            type = random.randint(0,1)
            if type == 0:
                enemy_group.add(DoubleLaser())
            elif type == 1:
                enemy_group.add(Jet())

        if self.start >= 5000 and self.start < 20000:
            self.spawn_delay = 4000
        elif self.start >= 20000 + 15000 * self.difficulty and self.difficulty < 6:
            self.spawn_delay -= 500
            self.difficulty += 1

        if not ship.is_dead:
            player_group.draw(screen)
        bullet_group.draw(screen)
        particle_group.draw(screen)
        pick_ups_group.draw(screen)
        enemy_group.draw(screen)
        enemy_group.update()
        bullet_group.update()
        particle_group.update()
        pick_ups_group.update()
        self.UI.update()
        pygame.display.flip()

    # Совершаем приготовления для перехода на экран проигрыша
    def game_over(self):
        pygame.mixer.music.fadeout(100)
        enemy_group.empty()
        bullet_group.empty()
        particle_group.empty()
        pick_ups_group.empty()

        ship.max_hp = 3
        ship.current_hp = 3
        ship.is_dead = False
        ship.invincible = False

        self.first_loop = True
        self.state = 'game_over_screen'

    # Экран конца игры
    def game_over_screen(self):
        screen.fill('black')

        mouse_pos = pygame.mouse.get_pos()

        game_over_title = get_font(60).render("GAME OVER", True, "White")
        game_over_rect = game_over_title.get_rect(center=(400, 60))

        your_score_title = get_font(40).render("YOUR SCORE:", True, "White")
        your_score_rect = your_score_title.get_rect(center=(400, 200))

        score_amount_title = get_font(60).render(str(int(ship.score)), True, "White")
        score_amount_rect = score_amount_title.get_rect(center=(400, 260))

        enter_name_title = get_font(40).render("ENTER YOUR NAME:", True, "White")
        enter_name_rect = enter_name_title.get_rect(center=(400, 380))

        player_name = get_font(60).render(self.player_name, True, "White")
        player_name_rect = player_name.get_rect(center=(400, 440))

        screen.blit(player_name, player_name_rect)
        screen.blit(your_score_title, your_score_rect)
        screen.blit(score_amount_title, score_amount_rect)
        screen.blit(enter_name_title, enter_name_rect)
        screen.blit(game_over_title, game_over_rect)

        continue_btn = Button(image=pygame.image.load("assets/buttons/Options Rect.png"), pos=(400, 700),
                          text_input="CONTINUE", font=get_font(60), base_color="White", hovering_color="#b68f40")

        continue_btn.changeColor(mouse_pos)
        continue_btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_btn.checkForInput(mouse_pos):
                    self.state = 'leaderboard_update'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'main_menu'
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.unicode.isalpha() and len(self.player_name) <= 2:
                    self.player_name += event.unicode.upper()

        self.UI.update()

        pygame.display.flip()

    # Обновляем данные таблицы лидеров в csv файле
    def leaderboard_update(self):
        if self.player_name == "":
            self.player_name = "NUL"

        with open("leaderboard.csv", encoding="utf8") as leaderboard:
            reader = csv.reader(leaderboard, delimiter=",", quotechar='"')

            data = [row for row in reader]
            data.append([self.player_name, str(int(ship.score))])
            sortedlist = sorted(data, key=lambda row: int(row[1]), reverse=True)

        with open("leaderboard.csv", "w", encoding="utf8", newline='') as leaderboard:
            writer = csv.writer(leaderboard)

            if len(sortedlist) > 10:
                sortedlist = sortedlist[0:9]

            for row in sortedlist:
                writer.writerow(row)

        self.state = 'leaderboard'

    # Экран с таблицей лидеров
    def leaderboard(self):
        with open("leaderboard.csv", encoding="utf8") as leaderboard:
            reader = csv.reader(leaderboard, delimiter=",", quotechar='"')
            data = [row for row in reader]

        mouse_pos = pygame.mouse.get_pos()

        screen.fill('black')

        leaderboard_title = get_font(60).render("LEADERBOARD", True, "White")
        leaderboard_rect = leaderboard_title.get_rect(center=(400, 60))

        for i in range(len(data)):
            player_name =  get_font(35).render(data[i][0], True, "White")
            player_name_rect = player_name.get_rect(center=(200, 140 + 45 * i))
            player_score = get_font(35).render(data[i][1], True, "White")
            player_score_rect = player_score.get_rect(center=(600, 140 + 45 * i))

            screen.blit(player_name, player_name_rect)
            screen.blit(player_score, player_score_rect)

        screen.blit(leaderboard_title, leaderboard_rect)

        continue_btn = Button(image=pygame.image.load("assets/buttons/Options Rect.png"), pos=(400, 700),
                              text_input="CONTINUE", font=get_font(60), base_color="White", hovering_color="#b68f40")

        continue_btn.changeColor(mouse_pos)
        continue_btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_btn.checkForInput(mouse_pos):
                    self.state = 'main_menu'

        self.UI.update()

        pygame.display.flip()

    # Определяем на каком экране сейчас находится пользователь и открываем его
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
        elif self.state == 'game_over':
            self.game_over()
        elif self.state == 'game_over_screen':
            self.game_over_screen()
        elif self.state == 'leaderboard_update':
            self.leaderboard_update()
        elif self.state == 'leaderboard':
            self.leaderboard()


# Класс, отвечающий за действия и отображение игрока
class Player(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("player_ship/player_ship_1.png"), (50, 50))
    image2 = pygame.transform.scale(load_image("player_ship/player_ship_2.png"), (50, 50))
    laser_sfx = pygame.mixer.Sound("assets/sound/laser.wav")

    def __init__(self, *group):
        super().__init__(*group)
        self.sprites = []
        self.sprites.append(Player.image)
        self.sprites.append(Player.image2)
        self.current_sprite = 0
        self.animation_speed = 0.3
        self.image = self.sprites[self.current_sprite]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.shooting_speed = 0.1
        self.reload = 0
        self.speedx = 5
        self.speedy = 5

        self.max_hp = 3
        self.current_hp = 3
        self.is_dead = False
        self.invincible = False
        self.invincibility_duration = 700
        self.death_duration = 1500
        self.hurt_time = 0

        self.score = 0
        self.score_gain = 0.01

    # Проверяем столкновения с противниками и, если они есть, получаем урон
    def check_enemy_collisions(self):
        if not self.invincible:
            for enemy in enemy_group:
                enemy_collisions = pygame.sprite.collide_mask(self, enemy)
                if enemy_collisions:
                    enemy.health -= 1
                    self.change_health(-1)

    def shoot(self):
        return Bullet(*self.rect.midtop, 'player')

    # Метод, меняющий текущее здоровье. При получении урона дает игроку неуязвимость
    def change_health(self, health_change):
        if health_change > 0 and self.current_hp < self.max_hp:
            self.current_hp += health_change
        elif health_change < 0:
            if not self.invincible:
                self.current_hp += health_change
                self.invincible = True
                self.hurt_time = pygame.time.get_ticks()
        else:
            self.change_score(15)

    # Метод, меняющий текущее значение очков, вплоть до максимального
    def change_score(self, score):
        if self.score >= 99999:
            self.score = 99999
        else:
            self.score += score

    # Проверяем жив ли игрок
    def check_death(self):
        if self.current_hp <= 0:
            particle_group.add(Particle(*self.rect.topleft, 'explosion'))
            self.is_dead = True

    # Если игрок неуязвим запускает таймер неуязвимости
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    # Запускает посмертный таймер, чтобы проигралась анимация взрыва и игрок понял что он умер
    def death_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.hurt_time >= self.death_duration:
            game_state.state = 'game_over'

    # Все анимации игрока
    def animation(self):
        self.current_sprite += self.animation_speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    # Управление кораблем
    def get_input(self):
        if game_state.keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speedy
        elif game_state.keys[pygame.K_s] and self.rect.bottom < HEIGHT - 100:
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

    # Для мигания спрайта игрока при неуязвимости
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self, *args):
        if self.is_dead:
            self.death_timer()
        else:
            self.change_score(self.score_gain)
            self.check_death()
            self.animation()
            self.check_enemy_collisions()
            self.get_input()
            self.invincibility_timer()


# Класс, отвечающий за стреляющего противника (не такой красивый как у игрока)
class DoubleLaser(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("double-laser-enemy/double_laser_1.png"), (50, 50))
    image2 = pygame.transform.scale(load_image("double-laser-enemy/double_laser_2.png"), (50, 50))
    image3 = pygame.transform.scale(load_image("double-laser-enemy/double_laser_3.png"), (50, 50))

    def __init__(self, *group):
        super().__init__(*group)
        self.laser_sfx = pygame.mixer.Sound("assets/sound/laser.wav")
        self.sprites = []
        for sprite in [DoubleLaser.image, DoubleLaser.image2, DoubleLaser.image3]:
            self.sprites.append(sprite)
        self.current_sprite = 0
        self.animation_speed = 0.3
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.direction = random.randint(0, 1)
        self.speedx = 0
        self.speedy = 0
        self.rect.y = -50
        self.health = 4

        if self.direction == 0:
            self.rect.x = random.randint(0, 200)
            self.speedy = 1
            self.speedx = 1
        elif self.direction == 1:
            self.rect.x = random.randint(600, 800)
            self.speedy = 1
            self.speedx = -1

        self.shooting_speed = 0.01
        self.second_shot = 1
        self.reload = 0

    def shoot(self):
        return Bullet(*self.rect.midtop, 'doublelaser')

    def update(self):
        self.current_sprite += self.animation_speed

        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.top > HEIGHT - 100) or (self.rect.right < 0) or (self.rect.left > WIDTH):
            self.kill()
        elif self.health <= 0:
            particle_group.add(Particle(*self.rect.topleft, 'explosion'))

            ship.change_score(10)
            game_state.kill_counter += 1
            if game_state.kill_counter == game_state.next_drop:
                pick_ups_group.add(PickUps(*self.rect.topleft, 'med_kit'))
                game_state.kill_counter = 0
                game_state.next_drop = random.randint(20, 30)

            self.kill()

        self.reload += self.shooting_speed

        if int(self.reload):
            self.laser_sfx.set_volume(sfx_volume / 2)
            bullet_group.add(self.shoot())
            self.laser_sfx.play()
            if self.second_shot:
                self.reload = 0.9
                self.second_shot = 0
            else:
                self.reload = 0
                self.second_shot = 1


# Класс, отвечающий за таранящего противника (не такой красивый как у игрока)
class Jet(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.frames = []
        self.cur_frame = 0
        self.animation_speed = 0.3

        self.columns = 3
        self.rows = 1
        self.cut_sheet(load_image("jet-enemy/jet_enemy.png"))
        self.image = self.frames[self.cur_frame]

        self.speedy = 3
        self.rect.y = -50
        self.rect.x = random.randint(100, 700)
        self.health = 3

    def cut_sheet(self, sheet):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // self.columns,
                                sheet.get_height() // self.rows)
        for j in range(self.rows):
            for i in range(self.columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (50, 50)))

    def update(self):
        self.cur_frame = self.cur_frame + self.animation_speed
        self.next_frame = int(self.cur_frame) % len(self.frames)
        self.image = self.frames[self.next_frame]

        self.rect.y += self.speedy

        if (self.rect.top > HEIGHT - 100):
            self.kill()
        elif self.health <= 0:
            particle_group.add(Particle(*self.rect.topleft, 'explosion'))

            ship.change_score(15)
            game_state.kill_counter += 1
            if game_state.kill_counter == game_state.next_drop:
                pick_ups_group.add(PickUps(*self.rect.topleft, 'med_kit'))
                game_state.kill_counter = 0
                game_state.next_drop = random.randint(20, 30)

            self.kill()


# Класс, отвечающий за снаряды
class Bullet(pygame.sprite.Sprite):
    laser_img_1 = pygame.transform.scale(load_image("double-laser-enemy/enemy_laser_projectile_1.png"), (16, 26))
    laser_img_2 = pygame.transform.scale(load_image("double-laser-enemy/enemy_laser_projectile_2.png"), (16, 26))

    def __init__(self, pos_x, pos_y, shooter):
        super().__init__()
        self.shooter = shooter
        if self.shooter == 'player':
            self.image = bullet_img = pygame.transform.scale(load_image("projectiles/small_projectile_1.png"), (10, 16))
            self.rect = self.image.get_rect(center = (pos_x, pos_y))
            self.mask = pygame.mask.from_surface(self.image)
        elif self.shooter == 'doublelaser':
            self.sprites = []
            for sprite in [Bullet.laser_img_1, Bullet.laser_img_2]:
                self.sprites.append(sprite)
            self.current_sprite = 0
            self.animation_speed = 0.3
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect(midtop = (pos_x, pos_y))
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.check_collisions()
        if self.shooter == 'player':
            self.rect.y -= 10
            if self.rect.y < 0:
                self.kill()
        elif self.shooter == 'doublelaser':
            self.current_sprite += self.animation_speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]

            self.rect.y += 5
            if self.rect.y > HEIGHT - 100:
                self.kill()

    def check_collisions(self):
        if self.shooter == 'player':
            for enemy in enemy_group:
                enemy_collisions = pygame.sprite.collide_mask(self, enemy)
                if enemy_collisions:
                    enemy.health -= 1
                    self.kill()
        elif self.shooter == 'doublelaser':
            if pygame.sprite.collide_mask(self, ship):
                ship.change_health(-1)
                self.kill()


# Класс, отвечающий за подбираемые предметы (аптечки)
class PickUps(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, type):
        super().__init__()
        self.type = type
        if self.type == 'med_kit':
            self.image = pygame.transform.scale(load_image("player_Ui/full_container.png"), (50, 50))
            self.rect = self.image.get_rect(topleft = (pos_x, pos_y))
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.fall()
        self.check_collisions()

    def fall(self):
        self.rect.y += 2

    def check_collisions(self):
        if pygame.sprite.collide_mask(self, ship):
            ship.change_health(1)
            ship.change_score(20)
            self.kill()


# Класс, отвечающий за анимации эффектов (взрывов)
class Particle(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, type):
        if type == 'explosion':
            super().__init__()
            self.type = type
            self.frames = []
            self.cur_frame = 0
            self.animation_speed = 0.2
            self.columns = 8
            self.rows = 1
            self.cut_sheet(load_image("explosions/explosion-6.png"))
            self.rect = self.rect.move(pos_x, pos_y)
            self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // self.columns,
                                    sheet.get_height() // self.rows)
        for j in range(self.rows):
            for i in range(self.columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (60, 60)))

    def update(self):
        self.cur_frame = self.cur_frame + self.animation_speed
        self.next_frame = int(self.cur_frame) % len(self.frames)
        self.image = self.frames[self.next_frame]
        if self.type == 'explosion':
            if self.next_frame == 0 and self.cur_frame >= len(self.frames):
                self.kill()


# Класс, отвечающий за отображения интерфейса
class UI(pygame.sprite.Sprite):

    def __init__(self, surface):
        super().__init__()
        self.display_surface = surface

        #фон интерфейса
        self.UI_base = load_image("player_Ui/Ui_base.png")

        #пустые и полные контейнеры здоровья
        self.full_container = load_image("player_Ui/full_container.png")
        self.full_container = pygame.transform.scale(self.full_container, (50, 50))
        self.empty_container = load_image("player_Ui/empty_container.png")
        self.empty_container = pygame.transform.scale(self.empty_container, (50, 50))

        #курсор мыши
        self.mouse_cursor = load_image("player_Ui/Blue_Arrow_Diamond.png")
        self.mouse_cursor = pygame.transform.scale(self.mouse_cursor, (32, 32))

    def show_health(self, current, full):
        self.display_surface.blit(self.UI_base, (0, 700))

        for i in range(0, current):
            self.display_surface.blit(self.full_container, (25 + 55 * i, 725))
        if full > current:
            for i in range(0, full - current):
                self.display_surface.blit(self.empty_container, (25 + 55 * current + 55 * i, 725))

    def show_score(self, score):
        self.score = int(score)

        score_num = get_font(25).render("SCORE:" + str(self.score), True, "White")
        score_rect = score_num.get_rect(center=(625, 750))

        self.display_surface.blit(score_num, score_rect)

    def update(self):

        if game_state.state == 'main_game':
            self.show_health(ship.current_hp, ship.max_hp)
            self.show_score(ship.score)
        else:
            if pygame.mouse.get_focused():
                self.display_surface.blit(self.mouse_cursor, pygame.mouse.get_pos())


# Игровой сетап
game_state = GameState()

bg = load_image("backgrounds/bg_stars.png")
bg.set_alpha(150)
bg_h = bg.get_height()

player_group = pygame.sprite.Group()
ship = Player(player_group)

enemy_group = pygame.sprite.Group()

bullet_group = pygame.sprite.Group()

particle_group = pygame.sprite.Group()

pick_ups_group = pygame.sprite.Group()

running = True
while running:

    clock.tick(FPS)

    game_state.state_manager()
