import random
from config import *

KOUNT = 0
LST_COEFF = {1: 0.95, 2: 0.92, 3: 0.85}


class Tetris:
    def __init__(self):
        # Инициализация игрового поля и необходимых переменных
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]  # Создаем 2D-массив для доски
        self.current_tetromino = self.new_tetromino()  # Получаем новую фигуру
        # Устанавливаем позицию фигуры на поле
        self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_tetromino[0]) // 2]
        # Создаем список доступных цветов отбора
        self.available_colors = COLORS[:]  # Копируем список цветов
        self.last_color = None  # Хранит предыдущий цвет
        self.current_color = self.get_new_color()  # Определение начального цвета
        self.level = 1  # Инициализация уровня игры
        self.next_tetromino = self.new_tetromino()  # Генерация следующей фигуры
        self.next_color = self.get_new_color()  # Получение цвета следующей фигуры
        self.score = 0

    def new_tetromino(self):
        # Генерация новой фигуры случайным образом из списка TETROMINOS
        return random.choice(TETROMINOS)

    def get_new_color(self):
        # Получие нового цвета для текущей фигуры
        if len(self.available_colors) == 0:  # Проверка, если список цветов пуст
            self.available_colors = COLORS[:]  # Если да, восстанавливаем полный список цветов
        # Случайный выбор цвета
        new_color = random.choice(self.available_colors)
        self.available_colors.remove(new_color)  # Удаляем использованный цвет из списка
        self.last_color = new_color  # Сохраняем последний использованный цвет
        return new_color  # Возвращаем новый цвет

    def rotate_tetromino(self):
        # Поворот фигуры по часовой стрелке
        self.current_tetromino = [list(row) for row in zip(*self.current_tetromino[::-1])]

    def move_tetromino(self, dx, dy):
        # Изменение положения фигуры
        self.current_position[0] += dx  # Изменение по вертикали
        self.current_position[1] += dy  # Изменение по горизонтали
        if self.collision():  # Проверка на коллизию
            self.current_position[0] -= dx  # Возврат назад по вертикали
            self.current_position[1] -= dy  # Возврат назад по горизонтали
            return False  # Возвращаем False при коллизии
        return True  # Возвращаем True если движение без коллизии

    def collision(self):
        # Проверка на коллизию с другими фигурами и границами
        shape = self.current_tetromino  # Получаем текущую форму фигуры
        x, y = self.current_position  # Получаем текущие координаты фигуры
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:  # Если текущая ячейка не пустая
                    # Проверка условий коллизии
                    if (i + x >= BOARD_HEIGHT or  # Если выходит за низ поля
                            j + y < 0 or  # Если выходит за левую границу
                            j + y >= BOARD_WIDTH or  # Если выходит за правую границу
                            isinstance(self.board[i + x][j + y], tuple)):  # Если ячейка занята другой фигурой
                        return True  # Если есть коллизия, возвращаем True
        return False  # Если коллизии нет, возвращаем False

    def merge_tetromino(self):
        # Смена текущей фигуры с игровым полем
        shape = self.current_tetromino
        x, y = self.current_position
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    # Запоминаем цвет вместе с фигурой
                    self.board[i + x][j + y] = self.current_color

    def clear_lines(self):
        global KOUNT
        # Очистка заполненных линий
        lines_to_clear = [i for i, row in enumerate(self.board) if all(isinstance(cell, tuple) for cell in row)]
        cleared_lines = len(lines_to_clear)  # Количество очищенных линий
        # Обновление счёта в зависимости от количества очищенных линий
        if cleared_lines > 0:
            if cleared_lines == 1:
                self.score += 100
            elif cleared_lines == 2:
                self.score += 300
            elif cleared_lines == 3:
                self.score += 700
            elif cleared_lines == 4:
                self.score += 1500
        for i in lines_to_clear:
            del self.board[i]  # Удаляем полностью заполненные линии
            self.board.insert(0, [0] * BOARD_WIDTH)  # Вставляем новые пустые линии сверху
            KOUNT += 1

    def drop_tetromino(self):
        # Движение фигуры вниз
        if not self.move_tetromino(1, 0):  # Попытка переместить Тетромино вниз
            self.merge_tetromino()  # Слить фигуру с доской
            self.clear_lines()  # Очистить линии
            self.current_tetromino = self.next_tetromino  # Перемещение следующей фигуры
            self.current_color = self.next_color  # Установка цвета текущей фигуры
            self.next_tetromino = self.new_tetromino()  # Генерация новой следующей фигуры
            self.next_color = self.get_new_color()  # Получение цвета следующей фигуры
            # Сбросить позицию для следующей фигуры
            self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_tetromino[0]) // 2]
            if self.collision():  # Проверка на коллизии
                return False  # Игра окончена
        return True  # Игра продолжается
