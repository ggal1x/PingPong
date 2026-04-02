import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
BALL_SIZE = 15
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг для двух игроков")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.Font(None, 36)

# Класс для платформы
class Paddle:
    def __init__(self, x, y, color, up_key, down_key):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.up_key = up_key
        self.down_key = down_key
        self.speed = PADDLE_SPEED
    
    def move(self, keys):
        if keys[self.up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[self.down_key] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Класс для мяча
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    
    def check_collision_with_walls(self):
        # Отскок от верхней и нижней стены
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y
    
    def check_collision_with_paddles(self, paddle1, paddle2):
        # Отскок от левой платформы
        if self.rect.colliderect(paddle1.rect) and self.speed_x < 0:
            self.speed_x = -self.speed_x
            # Немного меняем угол в зависимости от места удара
            offset = (self.rect.centery - paddle1.rect.centery) / (PADDLE_HEIGHT // 2)
            self.speed_y += offset * 3
            # Ограничиваем скорость по Y
            self.speed_y = max(-8, min(8, self.speed_y))
        
        # Отскок от правой платформы
        if self.rect.colliderect(paddle2.rect) and self.speed_x > 0:
            self.speed_x = -self.speed_x
            # Немного меняем угол в зависимости от места удара
            offset = (self.rect.centery - paddle2.rect.centery) / (PADDLE_HEIGHT // 2)
            self.speed_y += offset * 3
            # Ограничиваем скорость по Y
            self.speed_y = max(-8, min(8, self.speed_y))
    
    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = BALL_SPEED_X if self.speed_x > 0 else -BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

# Создание объектов
paddle1 = Paddle(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE, pygame.K_w, pygame.K_s)
paddle2 = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, RED, pygame.K_UP, pygame.K_DOWN)
ball = Ball()

# Счет
score1 = 0
score2 = 0

# Главный игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Получение нажатых клавиш
    keys = pygame.key.get_pressed()
    
    # Движение платформ
    paddle1.move(keys)
    paddle2.move(keys)
    
    # Движение мяча
    ball.move()
    
    # Проверка коллизий со стенами
    ball.check_collision_with_walls()
    
    # Проверка коллизий с платформами
    ball.check_collision_with_paddles(paddle1, paddle2)
    
    # Проверка голов
    if ball.rect.left <= 0:
        score2 += 1
        ball.reset()
        # Меняем направление мяча к проигравшему игроку
        ball.speed_x = -abs(ball.speed_x)
    elif ball.rect.right >= WIDTH:
        score1 += 1
        ball.reset()
        # Меняем направление мяча к проигравшему игроку
        ball.speed_x = abs(ball.speed_x)
    
    # Отрисовка
    screen.fill(BLACK)
    
    # Рисуем центральную линию
    for y in range(0, HEIGHT, 30):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, y, 10, 15))
    
    # Рисуем платформы
    paddle1.draw(screen)
    paddle2.draw(screen)
    
    # Рисуем мяч
    ball.draw(screen)
    
    # Отображение счета
    score_text1 = font.render(str(score1), True, WHITE)
    score_text2 = font.render(str(score2), True, WHITE)
    screen.blit(score_text1, (WIDTH // 4, 20))
    screen.blit(score_text2, (WIDTH * 3 // 4, 20))
    
    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

# Выход из игры
pygame.quit()
sys.exit()