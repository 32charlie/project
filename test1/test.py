import pygame
import os

# Инициализация Pygame
pygame.init()

# Определение размеров окна и тайлов
tile_size = 64
window_size = (1500, 720)
window = pygame.display.set_mode(window_size)

# Установка цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Функция для загрузки спрайтов
def load_sprite(file_path):
    try:
        sprite = pygame.image.load(file_path)
        sprite = pygame.transform.scale(sprite, (tile_size, tile_size))  # Изменение размера спрайта до размера тайла
        return sprite
    except pygame.error as e:
        print(f"Не удалось загрузить спрайт: {file_path}. Ошибка: {e}")
        return pygame.Surface((tile_size, tile_size))  # В случае ошибки возвращаем пустой спрайт


# Загрузка спрайтов из файлов
player_texture = pygame.transform.scale(pygame.image.load(r"assets\sprites\sp5.png").convert_alpha(), (64, 64))


# Данные карты (40x40)
map_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]

# Начальная позиция персонажа
player_x = 1
player_y = 1

move_speed = 70
last_move_time = 0


floor_texture = load_sprite(os.path.join(r"assets\sprites", "sp11.png"))
wall_texture = load_sprite(os.path.join(r"assets\sprites", "sp2.png"))
sea_texture = load_sprite(os.path.join(r"assets\sprites", "sp13.png"))


# Функция для отрисовки карты
def draw_map(map_data):
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == 0:  # Проходимая область
                window.blit(floor_texture, (x * tile_size, y * tile_size))
            elif tile == 1:  # Непроходимая область
                window.blit(wall_texture, (x * tile_size, y * tile_size))
            elif tile == 2:  # Непроходимая область
                window.blit(sea_texture, (x * tile_size, y * tile_size))


clock = pygame.time.Clock()
# Главный игровой цикл
running = True

while running:
    current_time = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Обработка движения персонажа
    if current_time - last_move_time > move_speed:  # Проверяем, достаточно ли времени прошло
        if keys[pygame.K_LEFT]:
            if map_data[player_y][player_x - 1] == 0:  # Проверка на проходимость
                player_x -= 1
                last_move_time = current_time  # Обновляем время последнего перемещения
        if keys[pygame.K_RIGHT]:
            if map_data[player_y][player_x + 1] == 0:  # Проверка на проходимость
                player_x += 1
                last_move_time = current_time  # Обновляем время последнего перемещения
        if keys[pygame.K_UP]:
            if map_data[player_y - 1][player_x] == 0:  # Проверка на проходимость
                player_y -= 1
                last_move_time = current_time  # Обновляем время последнего перемещения
        if keys[pygame.K_DOWN]:
            if map_data[player_y + 1][player_x] == 0:  # Проверка на проходимость
                player_y += 1
                last_move_time = current_time  # Обновляем время последнего перемещения

    # Оставшаяся часть цикла
    window.fill(BLACK)  # Очистка экрана
    draw_map(map_data)  # Отрисовка карты
    window.blit(player_texture, (player_x * (tile_size - 24), player_y * (tile_size - 24)))  # Отрисовка персонажа
    pygame.display.flip()  # Обновление экрана

    clock.tick(60)

pygame.quit()
