import pygame
import random

# Constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self, x, y, color):
        self.body = [(x, y)]
        self.direction = RIGHT
        self.grow = False
        self.color = color

    def head(self):
        return self.body[0]

    def move(self):
        x, y = self.head()
        dx, dy = self.direction
        new_head = (x + dx, y + dy)
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def collide(self, positions):
        return self.head() in positions

    def out_of_bounds(self):
        x, y = self.head()
        return not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT)

    def draw(self, surface):
        for x, y in self.body:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.color, rect)


def random_position(exclude):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in exclude:
            return pos


def ai_choose_direction(ai_snake, target, forbidden):
    # Choose direction that reduces Manhattan distance to target and is safe
    possible = [UP, DOWN, LEFT, RIGHT]
    best = None
    best_dist = float('inf')
    for d in possible:
        head_x, head_y = ai_snake.head()
        nx, ny = head_x + d[0], head_y + d[1]
        if (nx, ny) in forbidden or not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
            continue
        dist = abs(target[0] - nx) + abs(target[1] - ny)
        if dist < best_dist:
            best_dist = dist
            best = d
    return best


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    player = Snake(5, GRID_HEIGHT // 2, (0, 255, 0))
    ai = Snake(GRID_WIDTH - 6, GRID_HEIGHT // 2, (255, 0, 0))
    apple = random_position(player.body + ai.body)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.direction != DOWN:
                    player.direction = UP
                elif event.key == pygame.K_DOWN and player.direction != UP:
                    player.direction = DOWN
                elif event.key == pygame.K_LEFT and player.direction != RIGHT:
                    player.direction = LEFT
                elif event.key == pygame.K_RIGHT and player.direction != LEFT:
                    player.direction = RIGHT

        # AI move
        ai_dir = ai_choose_direction(ai, apple, set(player.body + ai.body[1:]))
        if ai_dir:
            ai.direction = ai_dir

        player.move()
        ai.move()

        # Check collisions
        occupied = set(player.body[1:] + ai.body[1:])
        if player.out_of_bounds() or player.collide(occupied):
            msg = font.render('AI Wins!', True, (255, 255, 255))
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            continue
        if ai.out_of_bounds() or ai.collide(set(player.body + ai.body[1:])):
            msg = font.render('Player Wins!', True, (255, 255, 255))
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            continue
        if player.head() == ai.head():
            msg = font.render('Draw!', True, (255, 255, 255))
            screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            continue

        # Apple eaten
        if player.head() == apple:
            player.grow = True
            apple = random_position(player.body + ai.body)
        if ai.head() == apple:
            ai.grow = True
            apple = random_position(player.body + ai.body)

        screen.fill((0, 0, 0))
        player.draw(screen)
        ai.draw(screen)
        apple_rect = pygame.Rect(apple[0]*CELL_SIZE, apple[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (255, 255, 0), apple_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
