import pygame
import random

data_score = open(r'D:\pythonProjectx\data\results.txt', 'r')
a = data_score.readlines().copy()
data = a if a != [] else [0]
data_score.close()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 0, 255),
    (255, 165, 0)
]

BLOCK_SIZE = 25
BOARD_WIDTH = 250 // BLOCK_SIZE
BOARD_HEIGHT = 500 // BLOCK_SIZE

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

TETROMINOS = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
]
KOUNT = 0

class Tetris:
    def __init__(self):

        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_tetromino = self.new_tetromino()

        self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_tetromino[0]) // 2]

        self.available_colors = COLORS[:]
        self.last_color = None
        self.current_color = self.get_new_color()
        self.level = 1
        self.next_tetromino = self.new_tetromino()
        self.next_color = self.get_new_color()
        self.score = 0

    def new_tetromino(self):

        return random.choice(TETROMINOS)

    def get_new_color(self):

        if len(self.available_colors) == 0:
            self.available_colors = COLORS[:]

        new_color = random.choice(self.available_colors)
        self.available_colors.remove(new_color)
        self.last_color = new_color
        return new_color

    def rotate_tetromino(self):

        self.current_tetromino = [list(row) for row in zip(*self.current_tetromino[::-1])]

    def move_tetromino(self, dx, dy):

        self.current_position[0] += dx
        self.current_position[1] += dy

        if self.collision():
            self.current_position[0] -= dx
            self.current_position[1] -= dy
            return False
        return True

    def collision(self):

        shape = self.current_tetromino
        x, y = self.current_position
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:

                    if (i + x >= BOARD_HEIGHT or
                        j + y < 0 or
                        j + y >= BOARD_WIDTH or
                            isinstance(self.board[i + x][j + y], tuple)):
                        return True
        return False

    def merge_tetromino(self):

        shape = self.current_tetromino
        x, y = self.current_position
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:

                    self.board[i + x][j + y] = self.current_color

    def clear_lines(self):
        global KOUNT

        lines_to_clear = [i for i, row in enumerate(self.board) if all(isinstance(cell, tuple) for cell in row)]
        cleared_lines = len(lines_to_clear)

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
            del self.board[i]
            self.board.insert(0, [0] * BOARD_WIDTH)
            KOUNT += 1

    def drop_tetromino(self):

        if not self.move_tetromino(1, 0):
            self.merge_tetromino()
            self.clear_lines()
            self.current_tetromino = self.next_tetromino
            self.current_color = self.next_color
            self.next_tetromino = self.new_tetromino()
            self.next_color = self.get_new_color()

            self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_tetromino[0]) // 2]
            if self.collision():
                return False
        return True

class StartScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Выберите режим")
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.mode = None
        self.buttons = [
            {"text": "1", "rect": pygame.Rect(100, 150, 150, 150), "mode": "level_1"},
            {"text": "2", "rect": pygame.Rect(300, 150, 150, 150), "mode": "level_2"},
            {"text": "3", "rect": pygame.Rect(500, 150, 150, 150), "mode": "level_3"},
            {"text": "Бесконечный режим", "rect": pygame.Rect(200, 350, 350, 150), "mode": "infinite"},
        ]

    def run(self):
        while self.running:
            self.screen.fill(WHITE)

            for button in self.buttons:
                pygame.draw.rect(self.screen, BLACK, button["rect"], 2)
                text = self.font.render(button["text"], True, BLACK)
                text_rect = text.get_rect(center=button["rect"].center)
                self.screen.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            self.start_game(button["mode"])

            pygame.display.flip()

        pygame.quit()

    def start_game(self, mode):
        self.running = False
        game = Game(mode)
        game.run()

class Game():
    def __init__(self, mode):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.tetris = Tetris()
        self.running = True
        self.fall_time = 0
        self.fall_speed = 500
        self.side_move_time = 0
        self.side_move_speed = 5000
        self.game_over = False
        self.paused = False
        self.pause_button_rect = pygame.Rect(10, 10, 50, 50)
        self.mode = mode
        self.speed_coeff = 0.95

    def draw_background(self):

        self.screen.fill(WHITE)

        game_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 - 1, (SCREEN_HEIGHT - 500) // 2 - 1, 252, 502)
        pygame.draw.rect(self.screen, BLACK, game_rect, 2)

    def draw_board(self):

        for i, row in enumerate(self.tetris.board):
            for j, cell in enumerate(row):
                if isinstance(cell, tuple):

                    outer_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 + j * BLOCK_SIZE, (SCREEN_HEIGHT - 500) // 2 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, BLACK, outer_rect)

                    inner_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 + j * BLOCK_SIZE + 1, (SCREEN_HEIGHT - 500) // 2 + i * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                    pygame.draw.rect(self.screen, cell, inner_rect)

    def draw_current_tetromino(self):

        shape = self.tetris.current_tetromino
        x, y = self.tetris.current_position
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:

                    outer_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 + (y + j) * BLOCK_SIZE, (SCREEN_HEIGHT - 500) // 2 + (x + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, BLACK, outer_rect)

                    inner_rect = pygame.Rect((SCREEN_WIDTH - 250) // 2 + (y + j) * BLOCK_SIZE + 1, (SCREEN_HEIGHT - 500) // 2 + (x + i) * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
                    pygame.draw.rect(self.screen, self.tetris.current_color, inner_rect)

    def draw_next_tetromino(self):

        font = pygame.font.Font(None, 30)
        text = font.render("Следующая фигура:", True, BLACK)
        self.screen.blit(text, (SCREEN_WIDTH - 230, (SCREEN_HEIGHT - 300) // 2))

        next_shape = self.tetris.next_tetromino
        for i, row in enumerate(next_shape):
            for j, cell in enumerate(row):
                if cell:

                    outer_rect = pygame.Rect(SCREEN_WIDTH - 160 + j * BLOCK_SIZE,
                                             (SCREEN_HEIGHT - 300) // 2 + 30 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, BLACK, outer_rect)

                    inner_rect = pygame.Rect(SCREEN_WIDTH - 160 + j * BLOCK_SIZE + 1,
                                             (SCREEN_HEIGHT - 300) // 2 + 30 + i * BLOCK_SIZE + 1, BLOCK_SIZE - 2,
                                             BLOCK_SIZE - 2)
                    pygame.draw.rect(self.screen, self.tetris.next_color, inner_rect)

    def set_mode(self):
        if self.mode[-1] == 1:
            0
        elif self.mode[-1] == 2:
            self.speed_coeff = 0.92
        elif self.mode[-1] == 3:
            self.speed_coeff = 0.85

        return self.mode

    def draw_score(self):

        font = pygame.font.Font(None, 36)
        score_text = f"Счет: {self.tetris.score}"
        text = font.render(score_text, True, BLACK)
        self.screen.blit(text, (60, (SCREEN_HEIGHT - 300) // 2))

    def draw_best_res(self):

        font = pygame.font.Font(None, 26)
        score_text = f"Лучший результат: {str(int(max(data)))}"
        text = font.render(score_text, True, BLACK)
        self.screen.blit(text, (40, (SCREEN_HEIGHT - 400) // 2))

    def draw_restart_button(self):
        button_size = 50
        button_rect = pygame.Rect(SCREEN_WIDTH - button_size - 10, 10, button_size, button_size)
        restart_button = pygame.transform.scale(pygame.image.load(r"assets\sprites\restart.png").convert_alpha(), (50, 50))

        self.screen.blit(restart_button, button_rect)
        return button_rect

    def draw_pause_button(self):

        start_rect = pygame.Rect(10, 10, 50, 50)
        start_button = pygame.transform.scale(pygame.image.load(r"assets\sprites\start.png").convert_alpha(),
                                                (50, 50))
        stop_button = pygame.transform.scale(pygame.image.load(r"assets\sprites\stop.png").convert_alpha(),
                                                (50, 50))
        self.screen.blit(stop_button, start_rect) if not self.paused else self.screen.blit(start_button, start_rect)

    def draw_pause_message(self):
        if self.paused:
            font = pygame.font.Font(None, 50)
            text = font.render("Игра приостановлена", True, BLACK)
            text_rect = pygame.Rect(200, 10, 50, 50)
            self.screen.blit(text, text_rect)

    def draw_game_over(self):

        font_size = 80
        font = pygame.font.Font(None, font_size)
        text = font.render("Game Over", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        outline_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(self.screen, DARK_YELLOW, outline_rect.inflate(10, 10))
        self.screen.blit(text, text_rect)

    def increase_speed(self):
        global KOUNT

        if KOUNT >= 3:
            self.tetris.level += 1
            self.fall_speed = self.fall_speed * self.speed_coeff
            self.fall_speed = 200 if self.fall_speed < 200 else self.fall_speed
            self.side_move_speed = 5000
            KOUNT = 0

    def save_score(self):
        data_score = open(r'D:\pythonProjectx\data\results.txt', 'a')
        data_score.write(f'{self.tetris.score}\n')
        data_score.close()
        data.append(str(self.tetris.score))

    def run(self):

        self.mode = self.set_mode()
        while self.running:
            self.draw_background()
            self.draw_pause_button()
            self.draw_pause_message()
            current_time = pygame.time.get_ticks()

            if not self.paused and not self.game_over and current_time - self.fall_time > self.fall_speed:
                if not self.tetris.drop_tetromino():
                    self.game_over = True
                self.fall_time = current_time
                self.increase_speed()

            self.draw_board()
            self.draw_current_tetromino()
            self.draw_next_tetromino()
            self.draw_score()
            self.draw_best_res()
            button_rect = self.draw_restart_button()

            if self.game_over:
                self.draw_game_over()
                if data[-1] != str(self.tetris.score):
                    self.save_score()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.tetris = Tetris()
                        self.game_over = False
                    if event.key ==  pygame.K_SPACE:
                        self.paused = not self.paused

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.pause_button_rect.collidepoint(mouse_pos):
                        self.paused = not self.paused

                    if button_rect.collidepoint(mouse_pos):
                        self.tetris = Tetris()
                        self.game_over = False

                if not self.paused:
                    if event.type == pygame.KEYDOWN:
                        if not self.game_over:
                            if event.key == pygame.K_LEFT:
                                self.tetris.move_tetromino(0, -1)
                            if event.key == pygame.K_RIGHT:
                                self.tetris.move_tetromino(0, 1)
                            if event.key == pygame.K_DOWN:
                                self.tetris.move_tetromino(1, 0)
                            if event.key == pygame.K_UP:
                                self.tetris.rotate_tetromino()
                                if self.tetris.collision():
                                    self.tetris.rotate_tetromino()
                                    self.tetris.rotate_tetromino()
                                    self.tetris.rotate_tetromino()

            if not self.paused:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and current_time - self.side_move_time > self.side_move_speed:
                    self.tetris.move_tetromino(0, -1)
                    self.side_move_time = current_time
                if keys[pygame.K_RIGHT] and current_time - self.side_move_time > self.side_move_speed:
                    self.tetris.move_tetromino(0, 1)
                    self.side_move_time = current_time
                if keys[pygame.K_DOWN]:
                    self.tetris.move_tetromino(1, 0)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    start_screen = StartScreen()
    start_screen.run()  