import random
import pygame

HEIGHT = 1280
WIDTH = 720

pygame.init()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
clock = pygame.time.Clock()
running = True
dt = 0


pipe_speed = 200
pipe_width = 50
pipe_gap = 200
pipe_gap_between = 300
pipe_color = "#E9C46A"

player_size = 25
player_speed = 600
player_color = "#E76F51"


class Pipe:
    def __init__(self, screen, speed, width, gap, color) -> None:
        self.screen = screen
        self.default_color = color
        self.color = color
        self.speed = speed
        self.width = width
        self.gap = gap

        self.pos_x = screen.get_width()
        self.height = random.randint(0, screen.get_height() - gap)

        self.top_rect = pygame.Rect(0, 0, 0, 0)
        self.bottom_rect = pygame.Rect(0, 0, 0, 0)

    def update(self, dt, bird):
        self.pos_x -= self.speed * dt

        self.top_rect = pygame.Rect(self.pos_x, 0, self.width, self.height)
        self.bottom_rect = pygame.Rect(self.pos_x, self.height + self.gap, self.width, screen.get_height())

        if (self.top_rect.colliderect(bird.body) or self.bottom_rect.colliderect(bird.body)):
            bird.body.centerx = self.pos_x - bird.body.width/2
            bird.hit = True

    def draw(self):
        pygame.draw.rect(screen, self.color, self.top_rect)
        pygame.draw.rect(screen, self.color, self.bottom_rect)


class Player:
    def __init__(self, screen, size, color, speed) -> None:
        self.screen = screen
        self.size = size
        self.color = color
        self.speed = speed
        self.dead = False
        self.hit = False
        self.fitness = 0.0

        self.body = pygame.Rect(screen.get_width() * .3 - size / 2, screen.get_height() / 2 - size / 2, size, size)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.body)

    def update(self, pipes: list[Pipe]):
        if self.hit:
            self.dead = True

        if self.dead:
            return

    def move(self, state, dt):
        if self.dead:
            return

        if state == "up":
            self.body.centery -= self.speed * dt
        if state == "down":
            self.body.centery += self.speed * dt
        if state == "stay":
            pass

agent = Player(screen, player_size, player_color, player_speed)

pipe = Pipe(screen, pipe_speed, pipe_width, pipe_gap, pipe_color)
last_pipe = pipe
pipes = [pipe]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("#264653")

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        agent.move("up", dt)
    if keys[pygame.K_s]:
        agent.move("down", dt)

    if (last_pipe.pos_x < screen.get_width() - pipe_gap_between - pipe_width):
        pipe = Pipe(screen, pipe_speed, pipe_width, pipe_gap, pipe_color)
        pipes.append(pipe)
        last_pipe = pipe

    for pipe in pipes:
        pipe.update(dt, agent)
        pipe.draw()

    agent.update(pipes)
    agent.draw()

    if (pipes[:1][0].pos_x <= -pipe_width):
        pipes.pop(0)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

    clock.tick(60)

pygame.quit()
