import pygame
import random

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

class Tetris:
    def __init__(self):

        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_tetromino = self.new_tetromino()

        self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_tetromino[0]) // 2]

        self.available_colors = COLORS[:]
        self.last_color = None
        self.current_color = self.get_new_color()
        self.level = 1

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

        lines_to_clear = [i for i, row in enumerate(self.board) if all(isinstance(cell, tuple) for cell in row)]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * BOARD_WIDTH)

    def drop_tetromino(self):

        if not self.move_tetromino(1, 0):
            self.merge_tetromino()
            self.clear_lines()
            self.current_tetromino = self.new_tetromino()
            self.current_color = self.get_new_color()

            self.current_position = [0, BOARD_WIDTH // 2 - len(self.current_tetromino[0]) // 2]
            if self.collision():
                return False
        return True

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.tetris = Tetris()
        self.running = True
        self.fall_time = 0
        self.fall_speed = 500
        self.side_move_time = 0
        self.side_move_speed = self.fall_speed * 1.5
        self.game_over = False

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

    def draw_game_over(self):

        font_size = 80
        font = pygame.font.Font(None, font_size)
        text = font.render("Game Over", True, YELLOW)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        outline_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(self.screen, DARK_YELLOW, outline_rect.inflate(10, 10))
        self.screen.blit(text, text_rect)

    def increase_speed(self):

        if sum(all(isinstance(cell, tuple) for cell in row) for row in self.tetris.board) >= self.tetris.level * 5:
            self.tetris.level += 1
            self.fall_speed = max(100, self.fall_speed - 50)
            self.side_move_speed = self.fall_speed * 1.5

    def run(self):

        while self.running:
            self.draw_background()
            current_time = pygame.time.get_ticks()

            if not self.game_over and current_time - self.fall_time > self.fall_speed:
                if not self.tetris.drop_tetromino():
                    self.game_over = True
                self.fall_time = current_time
                self.increase_speed()

            self.draw_board()
            self.draw_current_tetromino()

            if self.game_over:
                self.draw_game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_r:
                        self.tetris = Tetris()
                        self.game_over = False
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
    Game().run()