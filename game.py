import pygame
import sys
import random
import time
import sqlite3


class Border(pygame.sprite.Sprite): # Прорисовка игрового поля
    def __init__(self, x1, y1, x2, y2, all_sprites):
        super().__init__(all_sprites)
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Game():
    def __init__(self, lvl, nik):
        self.lvl = lvl
        self.nik = nik
        self.run = True
        self.a = []
        if lvl == 'Легкий': # В зависимости от уровня определяется размер поля
            self.x0 = 40
            self.y0 = 40
            self.screen_width = 240
            self.screen_height = 240
        elif lvl == 'Средний':
            self.x0 = 40
            self.y0 = 40
            self.screen_width = 340
            self.screen_height = 340
        elif lvl == 'Сложный':
            self.x0 = 40
            self.y0 = 40
            self.screen_width = 440
            self.screen_height = 440
        elif lvl == 'Эксперт':
            self.x0 = 40
            self.y0 = 40
            self.screen_width = 540
            self.screen_height = 540
            for i in range(15): # На экспертном уровне сложности появляются препятствия
                self.a.append([random.randrange(self.x0 / 10 + 1, self.screen_width / 10 - 1) * 10,
                               random.randrange(self.y0 / 10 + 1, self.screen_height / 10 - 1) * 10])
                # Задаются координаты препятствий (не могут появится на пути игрока при старте)

        pygame.init()
        pygame.display.set_caption('Игра "Змейка"')
        self.screen = pygame.display.set_mode((self.screen_width + self.x0, self.screen_height + self.y0))
        # Задаем размер окна

        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(93, 161, 48)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 0, 255)

        self.fps = pygame.time.Clock() # Скорость змейки

        self.score = 0 # Результат
        self.speed = 0 # Скорость

    def boxes(self): # Появление препятствий (если они есть)
        for i in self.a:
            pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), pygame.Rect(int(i[0]), int(i[1]), 10, 10))

    def events(self, direction): # Обработка нажатий клавиш
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    direction = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    direction = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    direction = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    direction = "DOWN"
        return direction

    def snake_speed(self): # В зависимости от сложности задается скорость
        pygame.display.flip()
        if self.lvl == 'Легкий':
            self.fps.tick(5)
            print(self.speed)
        elif self.lvl == 'Средний':
            self.fps.tick(15 + self.speed) # При съедании яблок увеличивается скорость (кроме лекого уровня сложности)
            print(self.speed)
        elif self.lvl == 'Сложный':
            self.fps.tick(20 + self.speed)
            print(self.speed)
        elif self.lvl == 'Эксперт':
            self.fps.tick(30 + self.speed)
            print(self.speed)

    def show_score(self, n=1): # Показывает результат и ник игрока
        font = pygame.font.SysFont('monaco', 24)
        surf = font.render(
            'Счёт: {0}'.format(self.score), True, self.black)
        surf1 = font.render(
            'Имя: {}'.format(self.nik), True, self.black)
        rect = surf.get_rect()
        rect1 = surf1.get_rect()
        if n == 1: # Если игра не закончена результат выводится в левом верхнем углы
            rect.midtop = (65, self.y0 / 2)
            rect1.midtop = (self.screen_width - 45, self.y0 / 2)
            self.screen.blit(surf, rect)
            self.screen.blit(surf1, rect1)
        elif n == 0: # Если игра закончена результат выводится под надписью Game over
            rect.midtop = ((self.screen_width + self.x0) / 2,
                             (self.screen_height + self.y0) / 2)
            self.screen.blit(surf, rect)

    def game_over(self): # Завершение игры
        self.screen.fill(pygame.Color("white")) # Экран становится белым
        font = pygame.font.SysFont('monaco', 36)
        surf = font.render('Game over', True, self.red) # Вывод надписи об окончании игры
        rect = surf.get_rect()
        rect.midtop = ((self.screen_width + self.x0) / 2, (self.screen_height) / 2)
        self.screen.blit(surf, rect)
        self.show_score(0)

        self.connection = sqlite3.connect("tab_liderov.sqlite") # Заносим результат в таблицу
        self.cur = self.connection.cursor()
        self.cur.execute(
            f'insert into liders(nik, lvl, res) values ("{str(self.nik)}", "{self.lvl}", {str(self.score)})').fetchall()
        self.connection.commit()

        pygame.display.flip()
        time.sleep(3) # Через 3 секунды после завершения игры окно закрывается
        pygame.quit()
        self.run = False


class Snake(): # Змейка
    def __init__(self, snake_color, x0, y0):
        self.snake_head = [x0 + 20, y0] # Голова змеи
        self.snake_body = [[x0 + 20, y0], [x0 + 10, y0], [x0, y0]] # Туловище змеи (изначально три клетки)
        self.snake_color = snake_color
        self.direction = "RIGHT" # Направление змейки (изначально направо)
        self.change = self.direction

    def change_direction(self): # Проверка если змейка не разворачивается на 180 градусов, она меняет направление
        if (self.change == "RIGHT" and not self.direction == "LEFT") \
                or (self.change == "LEFT" and not self.direction == "RIGHT") \
                or (self.change == "UP" and not self.direction == "DOWN") \
                or (self.change == "DOWN" and not self.direction == "UP"):
            self.direction = self.change

    def move(self): # движение змейки
        if self.direction == "RIGHT":
            self.snake_head[0] += 10
        elif self.direction == "LEFT":
            self.snake_head[0] -= 10
        elif self.direction == "UP":
            self.snake_head[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head[1] += 10

    def check_food(self, score, food_pos, x0, y0, screen_width, screen_height, lvl, speed, type, a):
        # Проверка на съедание змейкой еды
        self.snake_body.insert(0, list(self.snake_head)) # Прибавляем изначально змейки одну клетку
        if (self.snake_head[0] == food_pos[0] and
                self.snake_head[1] == food_pos[1]): # Если координаты головы змейки и еды совпадают
            food_pos = [random.randrange(x0 / 10, screen_width / 10) * 10,
                        random.randrange(y0 / 10, screen_height / 10) * 10]
            # Задаем координаты новой еды
            while food_pos in a or food_pos in self.snake_body: # Если координаты новой еды совпадают с препятствием, перезадаем координаты
                food_pos = [random.randrange(x0 / 10, screen_width / 10) * 10,
                            random.randrange(y0 / 10, screen_height / 10) * 10]
            if type == 5: # В зависимости от типа еды даем бонусы
                score += 10
            elif (type == 4 or type == 3) and lvl != 'Легкий':
                if lvl == 'Легкий': # В зависимости от уровня сложности уменьшаем скорость змейки
                    if speed > 4:
                        speed -= 0.2
                elif lvl == 'Средний':
                    if speed > 10:
                        speed -= 0.5
                elif lvl == 'Сложный':
                    if speed > 20:
                        speed -= 1
                elif lvl == 'Эксперт':
                    if speed > 30:
                        speed -= 3
            else:
                score += 1

            if lvl == 'Легкий': # В зависимости от уровня сложности увеличиваем скорость змейки от еды
                pass
            elif lvl == 'Средний':
                if speed < 20:
                    speed += 0.05
            elif lvl == 'Сложный':
                if speed < 35:
                    speed += 0.2
            elif lvl == 'Эксперт':
                if speed < 40:
                    speed += 0.5
            type = random.randrange(0, 10) # Задаем тип новой еды
        else: # Если координаты головы змейки и еды не совпадают то убираем клетку, которую мы добавили
            self.snake_body.pop()
        return score, food_pos, speed, type

    def draw_snake(self, play_surface, surface_color): # прорисовываем змейку
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(play_surface, self.snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_on_crash(self, game_over, x0, y0, screen_width, screen_height, a): # Проверка на столкновение с препятствиями
        if self.snake_head[0] > screen_width - 10 or self.snake_head[0] < x0 \
                or self.snake_head[1] > screen_height - 10 or self.snake_head[1] < y0: # столкновение с стеной
            game_over()
            return 0
        for i in self.snake_body[1:]: # Столкновение с туловищем
            if i[0] == self.snake_head[0] and i[1] == self.snake_head[1]:
                game_over()
                return 0
        for box in range(len(a)): # Столкновение с доп. препятствиями
            if (a[box][0] == self.snake_head[0] and
                    a[box][1] == self.snake_head[1]):
                game_over()
                return 0
        return 1


class Food(): # Еда
    def __init__(self, x0, y0, screen_width, screen_height, a, snake_body):
        self.food_pos = [random.randrange(x0 / 10, screen_width / 10) * 10,
                         random.randrange(y0 / 10, screen_height / 10) * 10] # Появление первой еды на поле
        while self.food_pos in a or self.food_pos in snake_body: # ...
            self.food_pos = [random.randrange(x0 / 10, screen_width / 10) * 10,
                             random.randrange(y0 / 10, screen_height / 10) * 10]
        self.type = random.randrange(0, 10) # ...

    def draw_food(self, screen, lvl):
        # Получаем рандомное число от 0 до 10, числа 0, 1, 2, 6, 7, 8, 9 это обычное яблоко
        # Число 5 это золотое яблоко
        # Числа 3, 4 - серая сфера
        # Обычное яблоко: увеличивает скорость, прибавляет 1 балл
        # Золотое яблоко: увеличивает скорость, прибавляет 10 баллов
        # Серая сфера: уменьшает скорость
        if 5 < self.type <= 10: # Определяем тип еды
            pygame.draw.rect(
                screen, pygame.Color(255, 0, 0), pygame.Rect(
                    self.food_pos[0], self.food_pos[1],
                    10, 10))
        elif self.type == 5:
            pygame.draw.rect(
                screen, pygame.Color(255, 215, 0), pygame.Rect(
                    self.food_pos[0], self.food_pos[1],
                    10, 10))
        elif (self.type == 4 or self.type == 3) and lvl != 'Легкий':
            pygame.draw.circle(
                screen, pygame.Color(169, 169, 169),
                (self.food_pos[0] + 5, self.food_pos[1] + 5), 5, 2)
        else:
            pygame.draw.rect(
                screen, pygame.Color(255, 0, 0), pygame.Rect(
                    self.food_pos[0], self.food_pos[1],
                    10, 10))