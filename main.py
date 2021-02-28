import sys
import pygame
import random
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from tab_liderov import MyWidgett
from rules import MyWidgettt
from game import Game, Snake, Food, Border


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Начало игры.ui', self) # Начальное окно
        self.pushButton.clicked.connect(self.push) # Кнопка для старта игры
        self.pushButton_2.clicked.connect(self.push_2) # Кнопка для просмотра таблицы лидеров
        self.pushButton_3.clicked.connect(self.push_3) # Кнопка для просмотра правил

    def push(self): # Начало игры
        if self.lineEdit.text() != '' and len(self.lineEdit.text()) <= 10: # Проверка ввел ли пользователь ник
            self.label_3.setText('')
            self.nik = self.lineEdit.text()
            self.lvl = self.comboBox.currentText()
            game = Game(self.lvl, self.nik)
            snake = Snake(game.green, game.x0, game.y0)
            food = Food(game.x0, game.y0, game.screen_width, game.screen_height, game.a, snake.snake_body)
            all_sprites = pygame.sprite.Group()
            Border(game.x0, game.y0, game.screen_width, game.y0, all_sprites)
            Border(game.x0, game.screen_height, game.screen_width, game.screen_height, all_sprites)
            Border(game.x0, game.y0, game.x0, game.screen_height, all_sprites)
            Border(game.screen_width, game.y0, game.screen_width, game.screen_height, all_sprites)
            while game.run:
                snake.change = game.events(snake.change) # Задаем направление
                snake.change_direction() # Проверка на изменение направления движения
                snake.move() # Меняем направление движения
                game.score, food.food_pos, game.speed, food.type = snake.check_food(
                    game.score, food.food_pos, game.x0, game.y0, game.screen_width, game.screen_height,
                    game.lvl, game.speed, food.type, game.a) # Получаем количество очков, новую позицию еды, скорость и тип еды
                if snake.check_on_crash(
                        game.game_over, game.x0, game.y0, game.screen_width, game.screen_height, game.a): # Проверка на столкновение
                    snake.draw_snake(game.screen, game.white) # Прорисовываем заново змейку
                    food.draw_food(game.screen, self.lvl) # Прорсовываем еду
                    all_sprites.draw(game.screen) # Прорисовка стен игрого поля
                    all_sprites.update()
                    game.boxes() # Прорисовка препятствий
                    game.show_score() # Показываем количество очков
                    game.snake_speed() # Обновляем показатели скорости
        else:
            if self.lineEdit.text() == '': # Если не ввели ник
                self.label_3.setText("Введите ваш игровой ник!")
            else: # Если ник слишком длинный
                self.label_3.setText("Ваш игровой ник слишком длинный! Макс.длина 10 символов")


    def push_2(self): # Просмотр таблицы лидеров
        self.second_form = MyWidgett()
        self.second_form.show()

    def push_3(self): # Просмотр правил
        self.rules = MyWidgettt()
        self.rules.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())