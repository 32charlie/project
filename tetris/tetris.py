import os
import pygame  # Импортируем библиотеку Pygame, которая используется для создания игр
import random  # Импортируем модуль random для генерации случайных чисел

data_score = open(fr'{os.path.abspath(os.getcwd())}\data\results.txt', 'r')  # База данных результатов
a = data_score.readlines().copy()
data = a if a != [] else [0]
data_score.close()
# Определение цвета
BLACK = (0, 0, 0)  # Определяем черный цвет в RGB
WHITE = (255, 255, 255)  # Определяем белый цвет в RGB
YELLOW = (255, 255, 0)  # Определяем желтый цвет в RGB
GREEN = (0, 255, 0)
DARK_YELLOW = (200, 200, 0)  # Определяем темный желтый цвет в RGB
# Определение доступных цветов для фигур
COLORS = [
    (255, 0, 0),  # Красный
    (0, 255, 0),  # Зеленый
    (0, 0, 255),  # Синий
    (0, 255, 255),  # Циан
    (255, 0, 255),  # Магента
    (255, 165, 0)  # Оранжевый
]

# Размеры клетки и игрового поля
BLOCK_SIZE = 25  # Размер одного блока (клеточки) в пикселях
BOARD_WIDTH = 250 // BLOCK_SIZE  # Количество клеток по ширине (10 блоков)
BOARD_HEIGHT = 500 // BLOCK_SIZE  # Количество клеток по высоте (20 блоков)

# Размеры окна
SCREEN_WIDTH = 750  # Ширина окна в пикселях
SCREEN_HEIGHT = 700  # Высота окна в пикселях

# Формы Тетромино (фигур) как двумерные списки
TETROMINOS = [
    [[1, 1, 1, 1]],  # I-образная фигура
    [[1, 1], [1, 1]],  # O-образная фигура
    [[0, 1, 0], [1, 1, 1]],  # T-образная фигура
    [[1, 1, 0], [0, 1, 1]],  # S-образная фигура
    [[0, 1, 1], [1, 1, 0]],  # Z-образная фигура
    [[1, 0, 0], [1, 1, 1]],  # L-образная фигура
    [[0, 0, 1], [1, 1, 1]],  # J-образная фигура
]
KOUNT = 0

LST_COEFF = {1: 0.95, 2: 0.92, 3: 0.85}

pygame.mixer.init()
game_music = pygame.mixer.Sound('data/game_music.mp3')
pygame.mixer.music.load('data/game_music.mp3')
pygame.mixer.music.set_volume(0.3)


# Определение главного класса Тетриса
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
        return False  # Если коллизий нет, возвращаем False

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


# Основной класс игры
class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Выберите режим")
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.flag = 0
        button_size = 24
        self.choice_one = 2
        self.choice_two = 2
        self.choice_three = 2
        self.flag_menu = False
        self.button_one = pygame.Rect(100, 620, button_size, button_size)  # Положение кнопки
        self.button_two = pygame.Rect(295, 620, button_size, button_size)  # Положение кнопки
        self.button_three = pygame.Rect(495, 620, button_size, button_size)  # Положение кнопки
        self.buttons = [
            {"text": "1", "rect": pygame.Rect(100, 250, 150, 150), "rect_color": pygame.Rect(102, 252, 146, 146), 'color': (194, 252, 196), "mode": [1, "level_1"]},
            {"text": "2", "rect": pygame.Rect(300, 250, 150, 150), "rect_color": pygame.Rect(302, 252, 146, 146), 'color': (251, 252, 194), "mode": [2, "level_2"]},
            {"text": "3", "rect": pygame.Rect(500, 250, 150, 150), "rect_color": pygame.Rect(502, 252, 146, 146), 'color': (252, 194, 194), "mode": [3, "level_3"]},
            {"text": "Бесконечный режим", "rect": pygame.Rect(200, 450, 350, 150), "rect_color": pygame.Rect(202, 452, 346, 146), 'color': (255, 255, 255), "mode": [1, "infinite"]},
        ]

    def run(self):
        while self.running:
            self.screen.fill((232, 241, 255))

            restart_button = pygame.image.load(r"assets\sprites\logo.png").convert_alpha()
            self.screen.blit(restart_button, (50, 30))
            for button in self.buttons:
                pygame.draw.rect(self.screen, BLACK, button["rect"], 2)
                pygame.draw.rect(self.screen, button['color'], button["rect_color"])
                text = self.font.render(button["text"], True, BLACK)
                text_rect = text.get_rect(center=button["rect"].center)
                self.screen.blit(text, text_rect)
                if self.flag_menu:
                    self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_one.collidepoint(mouse_pos):
                        self.buttons[-1]["mode"] = [1, "infinite"]
                        self.choice_one = 20
                        self.choice_two = 2
                        self.choice_three = 2
                    if self.button_two.collidepoint(mouse_pos):
                        self.buttons[-1]["mode"] = [2, "infinite"]
                        self.choice_one = 2
                        self.choice_two = 20
                        self.choice_three = 2
                    if self.button_three.collidepoint(mouse_pos):
                        self.buttons[-1]["mode"] = [3, "infinite"]
                        self.choice_one = 2
                        self.choice_two = 2
                        self.choice_three = 20
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            self.start_game(button["mode"])  # Запускаем игру с выбранным режимом

            pygame.display.flip()

        pygame.quit()

    def start_game(self, mode):
        if mode[-1] == "infinite" and self.flag == 0:
            self.draw_board()
            self.flag = 1
            self.flag_menu = True
        else:
            pygame.mixer.music.play(-1)
            self.running = False  # Закрыть начальное окно
            game = Game(mode)
            game.run() # Запуск основной игры с выбранным режимом

    def draw_board(self):

        text_one = self.font.render('Легкий', True, BLACK)
        pygame.draw.rect(self.screen, BLACK, self.button_one, self.choice_one)
        self.screen.blit(text_one, (130, 620))

        text_two = self.font.render('Средний', True, BLACK)
        pygame.draw.rect(self.screen, BLACK, self.button_two, self.choice_two)
        self.screen.blit(text_two, (325, 620))

        text_three = self.font.render('Сложный', True, BLACK)
        pygame.draw.rect(self.screen, BLACK, self.button_three, self.choice_three)
        self.screen.blit(text_three, (525, 620))


# Основной класс игры
class Game():
    def __init__(self, mode):
        pygame.init()
        # Инициализация окна
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()  # Для контроля FPS
        self.tetris = Tetris()  # Первая инициализация тетромино
        self.running = True  # Запуск игры
        self.fall_time = 0  # Время падения текущей фигуры
        self.fall_speed = 500  # Падение каждую 500 мс (0.5 секунды)
        self.side_move_time = 0  # Время бокового перемещения
        self.side_move_speed = 1000000  # Ограничение скорости бокового движения
        self.game_over = False  # Флаг окончания игры
        self.win = False
        self.paused = False  # Флаг паузы
        self.pause_button_rect = pygame.Rect(10, 10, 50, 50)  # Прямоугольник для кнопки паузы
        self.mode = mode  # Переменная для хранения выбранного режима
        self.speed_coeff = 0.95
        self.infinite = False

    def draw_background(self):
        # Отрисовка фона
        self.screen.fill(WHITE)  # Задаем фон белым цветом

        # Рисуем рамку для игрового поля
        game_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 - 1, (SCREEN_HEIGHT - 500) // 2 - 1, 252,
                                502)  # Центрируем поле
        pygame.draw.rect(self.screen, BLACK, game_rect, 2)  # Черная окантовка вокруг поля для игры

    def draw_board(self):
        # Рисуем игровое поле
        for i, row in enumerate(self.tetris.board):
            for j, cell in enumerate(row):
                if isinstance(cell, tuple):  # Проверяем, является ли ячейка цветом
                    # Окантовка фигуры
                    outer_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 + j * BLOCK_SIZE,
                                             (SCREEN_HEIGHT - 500) // 2 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, BLACK, outer_rect)  # Рисуем окантовку

                    # Рисуем фигуру
                    inner_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 + j * BLOCK_SIZE + 1,
                                             (SCREEN_HEIGHT - 500) // 2 + i * BLOCK_SIZE + 1, BLOCK_SIZE - 2,
                                             BLOCK_SIZE - 2)
                    pygame.draw.rect(self.screen, cell, inner_rect)  # Форма

    def draw_current_speed(self):
        font = pygame.font.Font(None, 30)  # Размер шрифта
        text = font.render(f"{self.mode}, {self.fall_speed}, {self.speed_coeff}", True, BLACK)  # Создание текста
        self.screen.blit(text, (25, 400))  # Положение текста

    def draw_current_tetromino(self):
        # Рисуем текущую фигуру
        shape = self.tetris.current_tetromino
        x, y = self.tetris.current_position  # Текущая позиция фигуры
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    # Окантовка текущей фигуры
                    outer_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 + (y + j) * BLOCK_SIZE,
                                             (SCREEN_HEIGHT - 500) // 2 + (x + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, BLACK, outer_rect)  # Окантовка

                    # Рисуем фигуру
                    inner_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 + (y + j) * BLOCK_SIZE + 1,
                                             (SCREEN_HEIGHT - 500) // 2 + (x + i) * BLOCK_SIZE + 1, BLOCK_SIZE - 2,
                                             BLOCK_SIZE - 2)
                    pygame.draw.rect(self.screen, self.tetris.current_color, inner_rect)  # Рисуем текущую фигуру

    def draw_next_tetromino(self):
        # Отображение текста "Следующая фигура:"
        font = pygame.font.Font(None, 30)  # Размер шрифта
        text = font.render("Следующая фигура:", True, BLACK)  # Создание текста
        self.screen.blit(text, (SCREEN_WIDTH - 230, (SCREEN_HEIGHT - 300) // 2))  # Положение текста

        # Рисуем следующую фигуру
        next_shape = self.tetris.next_tetromino  # Получаем следующую фигуру
        for i, row in enumerate(next_shape):
            for j, cell in enumerate(row):
                if cell:
                    # Окантовка следующей фигуры
                    outer_rect = pygame.Rect(SCREEN_WIDTH - 160 + j * BLOCK_SIZE,
                                             (SCREEN_HEIGHT - 300) // 2 + 30 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, BLACK, outer_rect)  # Окантовка

                    # Рисуем фигуру
                    inner_rect = pygame.Rect(SCREEN_WIDTH - 160 + j * BLOCK_SIZE + 1,
                                             (SCREEN_HEIGHT - 300) // 2 + 30 + i * BLOCK_SIZE + 1, BLOCK_SIZE - 2,
                                             BLOCK_SIZE - 2)
                    pygame.draw.rect(self.screen, self.tetris.next_color, inner_rect)  # Рисуем следующую фигуру

    def set_mode(self):
        if '1' in self.mode[-1]:
            pass
        elif '2' in self.mode[-1]:
            self.speed_coeff = 0.92
        elif '3' in self.mode[-1]:
            self.speed_coeff = 0.85
        else:
            self.infinite = True
            self.speed_coeff = LST_COEFF[self.mode[0]]
        # Этот метод будет содержать логику выбора режима в зависимости от кнопки
        return self.mode  # Возвращаем выбранный режим

    def draw_score(self):
        # Отображение текста счёта
        font = pygame.font.Font(None, 36)  # Размер шрифта
        score_text = f"Счет: {self.tetris.score}"  # Подготовка текста счёта
        text = font.render(score_text, True, BLACK)  # Создание текста
        self.screen.blit(text, (60, (SCREEN_HEIGHT - 300) // 2))  # Положение текста

    def draw_best_res(self):
        # Отображение рекорда
        font = pygame.font.Font(None, 36)  # Размер шрифта
        score_text = f"Рекорд: {str(max(list(map(int, data))))}"  # Отображение лучшего результата
        text = font.render(score_text, True, BLACK)  # Создание текста
        self.screen.blit(text, (60, (SCREEN_HEIGHT - 400) // 2))  # Положение текста

    def draw_restart_button(self):
        button_size = 50  # Размер кнопки
        button_rect = pygame.Rect(SCREEN_WIDTH - button_size - 10, 10, button_size, button_size)  # Положение кнопки
        restart_button = pygame.transform.scale(pygame.image.load(r"assets\sprites\restart.png").convert_alpha(),
                                                (50, 50))
        # Отображение кнопки
        self.screen.blit(restart_button, button_rect)  # Отображение текста на кнопке
        return button_rect  # Возвращаем прямоугольник кнопки для дальнейшей проверки нажатий

    def draw_return_button(self):
        button_rect = pygame.Rect(10, SCREEN_HEIGHT - 60, 50, 50)  # Положение и размер кнопки
        return_button = pygame.transform.scale(pygame.image.load(r"assets\sprites\home.png").convert_alpha(),
                                                (50, 50))
        self.screen.blit(return_button, button_rect)
        return button_rect  # Возвращаем прямоугольник кнопки для дальнейшей проверки нажатий

    def draw_pause_button(self):
        # Отрисовка кнопки паузы
        start_rect = pygame.Rect(10, 10, 50, 50)  # Положение кнопки
        start_button = pygame.transform.scale(pygame.image.load(r"assets\sprites\start.png").convert_alpha(),
                                              (50, 50))
        stop_button = pygame.transform.scale(pygame.image.load(r"assets\sprites\stop.png").convert_alpha(),
                                             (50, 50))
        self.screen.blit(stop_button, start_rect) if not self.paused else self.screen.blit(start_button, start_rect)

    def draw_pause_message(self):
        if self.paused:
            font = pygame.font.Font(None, 50)  # Размер шрифта
            text = font.render("Игра приостановлена", True, BLACK)  # Создаем текст
            text_rect = pygame.Rect(200, 10, 50, 50)  # Положение текста
            self.screen.blit(text, text_rect)  # Отображение текста на экране

    def draw_game_over(self):
        # Отображение текста "Game Over"
        font_size = 80  # Размер шрифта для Game Over
        font = pygame.font.Font(None, font_size)  # Объект шрифта
        text = font.render("Game Over", True, YELLOW)  # Создание текста "Game Over"
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Положение текста в центре экрана
        # Окантовка текста
        outline_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Создание области для текста
        pygame.draw.rect(self.screen, DARK_YELLOW, outline_rect.inflate(10, 10))  # Окантовка текста
        self.screen.blit(text, text_rect)  # Отображение текста на экране

    def draw_win(self):
        # Отображение текста "Win"
        font_size = 80  # Размер шрифта для Game Over
        font = pygame.font.Font(None, font_size)  # Объект шрифта
        text = font.render("Победа!", True, GREEN)  # Создание текста "Win"
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Положение текста в центре экрана
        # Окантовка текста
        outline_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Создание области для текста
        pygame.draw.rect(self.screen, (0, 200, 0), outline_rect.inflate(10, 10))  # Окантовка текста
        self.screen.blit(text, text_rect)  # Отображение текста на экране

    def increase_speed(self):
        global KOUNT
        # Увеличиваем скорость падения после каждых 5 линий
        if KOUNT >= 3:
            self.tetris.level += 1  # Увеличиваем уровень в классе Tetris
            self.fall_speed = self.fall_speed * self.speed_coeff  # Уменьшаем скорость падения до минимума 100ms
            self.fall_speed = 200 if self.fall_speed < 200 else self.fall_speed
            self.side_move_speed = 5000  # Обновляем скорость бокового движения
            KOUNT = 0

    def save_score(self):
        data_score = open(fr'{os.path.abspath(os.getcwd())}\data\results.txt', 'a')
        data_score.write(f'{self.tetris.score}\n')
        data_score.close()
        data.append(str(self.tetris.score))

    def run(self):

        # Основной игровой цикл
        self.mode = self.set_mode()  # Получаем режим из начального окна
        while self.running:
            self.draw_background()
            self.draw_pause_button()  # Отрисовка кнопки паузы
            self.draw_pause_message()  # Отрисовка сообщения о паузе
            button_rect_return = self.draw_return_button()
            current_time = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах

            # Проверка времени на падение
            if not self.paused and not self.game_over and not self.win and current_time - self.fall_time > self.fall_speed:
                if not self.tetris.drop_tetromino():
                    self.game_over = True  # Игра окончена
                self.fall_time = current_time  # Обновляем время падения
                self.increase_speed()  # Проверяем, нужно ли увеличить скорость
            if self.tetris.score >= 1000 and not self.infinite:
                self.win = True

            self.draw_board()  # Рисуем игровое поле
            self.draw_current_tetromino()  # Отрисовка текущей фигуры
            self.draw_current_speed()
            self.draw_next_tetromino()
            self.draw_score()
            self.draw_best_res()
            button_rect = self.draw_restart_button()

            if self.game_over:
                self.draw_game_over()  # Отображение текста Game Over
                if data[-1] != str(self.tetris.score):
                    self.save_score()  # Сохранение результата
            if self.win:
                self.draw_win()
                if data[-1] != str(self.tetris.score):
                    self.save_score()  # Сохранение результата

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                    self.running = False
                if event.type == pygame.KEYDOWN:  # Если нажата клавиша
                    if event.key == pygame.K_r:  # Перезапуск игры
                        self.tetris = Tetris()  # Создание нового объекта Tetris
                        pygame.mixer.music.play()
                        self.game_over = False  # Сброс флага окончания игры
                        self.speed_coeff = 0.95
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ
                    mouse_pos = pygame.mouse.get_pos()  # Получаем позицию мыши
                    if self.pause_button_rect.collidepoint(mouse_pos):  # Проверяем, нажата ли кнопка паузы
                        self.paused = not self.paused  # Переключение флага паузы
                        pygame.mixer.music.pause() if self.paused else pygame.mixer.music.unpause()

                    if button_rect.collidepoint(mouse_pos):  # Проверяем, нажата ли кнопка перезапуска
                        pygame.mixer.music.play()
                        self.tetris = Tetris()  # Создание нового объекта Tetris
                        self.game_over = False
                        self.win = False  # Сброс флага окончания игры
                        self.fall_speed = 500

                    if button_rect_return.collidepoint(mouse_pos):  # Проверяем, нажата ли кнопка возврата
                        pygame.mixer.music.stop()
                        start_back = StartScreen()
                        start_back.run()  # Возвращаемся в начальное меню
                        self.running = False

                if not self.paused and not self.win:  # Если игра не на паузе
                    if event.type == pygame.KEYDOWN:  # Если нажата клавиша
                        if not self.game_over:  # Если игра не окончена
                            if event.key == pygame.K_LEFT:
                                self.tetris.move_tetromino(0, -1)  # Движение влево
                            if event.key == pygame.K_RIGHT:
                                self.tetris.move_tetromino(0, 1)  # Движение вправо
                            if event.key == pygame.K_DOWN:
                                self.tetris.move_tetromino(1, 0)  # Движение вниз
                            if event.key == pygame.K_UP:
                                self.tetris.rotate_tetromino()  # Поворот фигуры
                                if self.tetris.collision():  # Проверка на коллизии
                                    self.tetris.rotate_tetromino()  # Поворот обратно, если есть коллизия
                                    self.tetris.rotate_tetromino()
                                    self.tetris.rotate_tetromino()

            if not self.paused and not self.win:  # Обработка движения только если игра не на паузе
                keys = pygame.key.get_pressed()  # Получаем текущее состояние клавиш
                if keys[pygame.K_LEFT] and current_time - self.side_move_time > self.side_move_speed:
                    self.tetris.move_tetromino(0, -1)  # Движение влево
                    self.side_move_time = current_time  # Обновляем время бокового движения
                if keys[pygame.K_RIGHT] and current_time - self.side_move_time > self.side_move_speed:
                    self.tetris.move_tetromino(0, 1)  # Движение вправо
                    self.side_move_time = current_time  # Обновляем время бокового движения
                if keys[pygame.K_DOWN]:
                    self.tetris.move_tetromino(1, 0)  # Движение вниз

            pygame.display.flip()  # Обновляем экран
            self.clock.tick(60)  # Устанавливаем частоту обновления экрана (60 FPS)

        pygame.quit()  # Выход из Pygame


if __name__ == '__main__':
    start_screen = StartScreen()
    start_screen.run()  # Запуск начального окна
