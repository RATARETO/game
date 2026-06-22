# Размеры окна
WINDOW_HEIGHT = 900
WINDOW_WIDTH = 1200
FPS = 60

# Размер клетки и отступы карты
TILE_SIZE = 50
MAP_START_X, MAP_START_Y = 3, 2
MAP_WEIGHT, MAP_HEIGHT = 20, 15

# Параметры ИИ (минимакс)
AI_DEPTH = 3                     # глубина поиска
EVAL_ENEMY_HEALTH_WEIGHT = 2.0   # коэффициент здоровья врагов
EVAL_PLAYER_HEALTH_WEIGHT = 3.0  # коэффициент здоровья игрока
EVAL_DISTANCE_WEIGHT = 0.5       # штраф за расстояние

# Максимальное количество ходов за один шаг
MAX_MOVES_PER_TURN = 1
