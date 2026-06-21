import random
import pygame

GAME_TITLE = "Carrera de Obstáculos"
SCREEN_W = 1280
SCREEN_H = 720
GRAVITY = 1.2
JUMP_FORCE = -15.6

GAME_METADATA = {
    "id": "carrera_de_obstaculos",
    "title": GAME_TITLE,
    "description": "Juego de carrera de obstáculos",
    "authors": ["Gabriel Mejias", "Sofia Marquez"],
    "group_number": 7,
    "cover_path": "assets/covers/carrera_de_obstaculos.jpg"
}


class Player:
    def __init__(self, x, y, w, h, ground_y):
        self.rect = pygame.Rect(x, y, w, h)
        self.vy = 0
        self.ground_y = ground_y
        self.holding_jump = False

    def jump(self):
        if self.rect.bottom >= self.ground_y:
            self.vy = JUMP_FORCE
            self.holding_jump = True

    def release_jump(self):
        self.holding_jump = False

    def update(self):
        if self.vy < 0 and self.holding_jump:
            self.vy += GRAVITY * 0.5
        else:
            self.vy += GRAVITY

        self.rect.y += self.vy

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vy = 0
            self.holding_jump = False

    def draw(self, screen):
        pygame.draw.rect(screen, (40, 40, 40), self.rect)


class Obstacle:
    def __init__(self, x, w, h, ground_y):
        self.rect = pygame.Rect(x, ground_y - h, w, h)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 180, 0), self.rect)


class DiagonalObstacle(Obstacle):
    def __init__(self, x, w, h, ground_y, speed_x=10, speed_y=4):
        self.rect = pygame.Rect(x, 0, w, h)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.ground_y = ground_y

    def update(self, speed=None):
        self.rect.x -= self.speed_x
        if self.rect.bottom < self.ground_y:
            self.rect.y += self.speed_y
            if self.rect.bottom > self.ground_y:
                self.rect.bottom = self.ground_y
        else:
            self.rect.bottom = self.ground_y

    def draw(self, screen):
        pygame.draw.rect(screen, (180, 0, 0), self.rect)


def spawn_obstacle_pair(start_x, sizes, ground_y, gap_variants):
    distance_between = random.choice(gap_variants)
    obstacles = []
    current_x = start_x
    for w, h in sizes:
        obstacles.append(Obstacle(current_x, w, h, ground_y))
        current_x += w + distance_between
    return obstacles


class CarreraDeObstaculos:
    def __init__(self):
        self.screen = None
        self.running = True
        self.ground_y = SCREEN_H - 120
        self.player = Player(70, self.ground_y - 72, 53, 72, self.ground_y)
        self.gap_variants = [int(self.player.rect.width * 1.2) + 220,
                             int(self.player.rect.width * 1.2) + 140,
                             int(self.player.rect.width * 1.2) + 20]
        self.obstacles = spawn_obstacle_pair(
            SCREEN_W + random.randint(120, 260),
            [(34, 48), (38, 66)],
            self.ground_y,
            self.gap_variants,
        )
        self.diagonal_obstacle = None
        self.next_diagonal_trigger = 100
        self.speed = 6.6
        self.score = 0
        self.font = pygame.font.SysFont("consolas", 24)

    def _inject_context(self, screen):
        self.screen = screen

    def _stop_context(self):
        self.running = False

    def stop(self):
        self.running = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.player.jump()
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                self.player.release_jump()

    def update(self, dt):
        if not self.running:
            return

        self.player.update()

        for obs in self.obstacles:
            obs.update(self.speed)
            if self.player.rect.colliderect(obs.rect):
                self.running = False
                return

        displayed_score = self.score // 10
        if displayed_score >= self.next_diagonal_trigger and self.diagonal_obstacle is None:
            self.diagonal_obstacle = DiagonalObstacle(
                SCREEN_W - 40,
                32,
                32,
                self.ground_y,
                speed_x=10,
                speed_y=4,
            )
            self.next_diagonal_trigger += 67

        if self.diagonal_obstacle:
            self.diagonal_obstacle.update()
            if self.player.rect.colliderect(self.diagonal_obstacle.rect):
                self.running = False
                return
            if self.diagonal_obstacle.rect.right < 0 or self.diagonal_obstacle.rect.top > SCREEN_H:
                self.diagonal_obstacle = None

        if max(o.rect.right for o in self.obstacles) < 0:
            self.obstacles = spawn_obstacle_pair(
                SCREEN_W + random.randint(120, 260),
                [(34, 48), (38, 66)],
                self.ground_y,
                self.gap_variants,
            )

        self.score += 1
        if self.score % 10 == 0:
            self.speed += 0.02

    def draw(self):
        if self.screen is None:
            return

        self.screen.fill((255, 255, 255))
        self.player.draw(self.screen)

        for obs in self.obstacles:
            obs.draw(self.screen)

        if self.diagonal_obstacle:
            self.diagonal_obstacle.draw(self.screen)

        pygame.draw.line(self.screen, (120, 120, 120), (0, self.ground_y), (SCREEN_W, self.ground_y), 2)
        score_text = self.font.render(f"Score: {self.score // 10}", True, (0, 0, 0))
        self.screen.blit(score_text, (20, 20))


