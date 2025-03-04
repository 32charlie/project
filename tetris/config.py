import os

data_score = open(fr'{os.path.abspath(os.getcwd())}\data\results.txt', 'r')  # База данных результатов
a = data_score.readlines().copy()
data = a if a != [] else [0]
data_score.close()
# Определение цвета
BLACK = (0, 0, 0)  # Определяем черный цвет в RGB
WHITE = (255, 255, 255)  # Определяем белый цвет в RGB
YELLOW = (255, 255, 0)  # Определяем желтый цвет в RGB
GREEN = (0, 255, 0)  # Определяем зелёный цвет в RGB
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
RETURN = True
LST_COEFF = {1: 0.95, 2: 0.92, 3: 0.85}
