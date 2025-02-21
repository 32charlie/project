import pygame
from config import *
from tetris import Tetris


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
            {"text": "1", "rect": pygame.Rect(100, 250, 150, 150), "rect_color": pygame.Rect(102, 252, 146, 146),
             'color': (194, 252, 196), "mode": [1, "level_1"]},
            {"text": "2", "rect": pygame.Rect(300, 250, 150, 150), "rect_color": pygame.Rect(302, 252, 146, 146),
             'color': (251, 252, 194), "mode": [2, "level_2"]},
            {"text": "3", "rect": pygame.Rect(500, 250, 150, 150), "rect_color": pygame.Rect(502, 252, 146, 146),
             'color': (252, 194, 194), "mode": [3, "level_3"]},
            {"text": "Бесконечный режим", "rect": pygame.Rect(200, 450, 350, 150),
             "rect_color": pygame.Rect(202, 452, 346, 146), 'color': (255, 255, 255), "mode": [1, "infinite"]},
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
            self.running = False  # Закрыть начальное окно
            game = Game(mode)
            game.run()  # Запуск основной игры с выбранным режимом

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


class Game:
    def __init__(self, mode):
        pygame.init()
        # Инициализация окна
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()  # Для контроля FPS
        self.tetris = Tetris()  # Первая инициализация тетромино
        self.running = True  # Запуск игры
        self.fall_time = 0  # Время падения текущей фигуры
        self.fall_speed = 500  # Падение каждую 500 мс (0.5 секун
        self.side_move_time = 0  # Время бокового перемещенияды)
        self.side_move_speed = 1000000  # Ограничение скорости бокового движения
        self.game_over = False  # Флаг окончания игры
        self.win = False
        self.paused = False  # Флаг паузы
        self.pause_button_rect = pygame.Rect(10, 10, 50, 50)  # Прямоугольник для кнопки паузы
        self.mode = mode  # Переменная для хранения выбранного режима
        self.speed_coeff = 0.95
        self.infinite = False
        pygame.mixer.music.load('data/game_music.mp3')
        pygame.mixer.music.set_volume(0.3)

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

    def draw_pause_button(self):  # Отрисовка кнопки паузы
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
        if KOUNT >= 3:  # Увеличиваем скорость падения после каждых 5 линий
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
        pygame.mixer.music.play(-1)
        self.mode = self.set_mode()  # Получаем режим из начального окна
        while self.running:
            self.draw_background()
            self.draw_pause_button()  # Отрисовка кнопки паузы
            self.draw_pause_message()  # Отрисовка сообщения о паузе
            button_rect_return = self.draw_return_button()
            current_time = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах
            # Проверка времени на падение
            if (not self.paused and not self.game_over and not self.win and
                    current_time - self.fall_time > self.fall_speed):
                if not self.tetris.drop_tetromino():
                    self.game_over = True  # Игра окончена
                self.fall_time = current_time  # Обновляем время падения
                self.increase_speed()  # Проверяем, нужно ли увеличить скорость
            if self.tetris.score >= 1000 and not self.infinite:
                self.win = True
            self.draw_board()  # Рисуем игровое поле
            self.draw_current_tetromino()  # Отрисовка текущей фигуры
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
                        pygame.mixer.music.stop()  # Возвращаемся в начальное меню
                        start_back = StartScreen()
                        start_back.run()
                        self.running = False
                        return False
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