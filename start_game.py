from snake import *
from os import environ
from game_settings import SURFACE_COLOR, ROWS, SQUARE_SIZE, GRID_COLOR, HEIGHT, WIDTH, SNAKE_COLOR, APPLE_COLOR

def draw_screen(surface):
    surface.fill(SURFACE_COLOR)

# draw the grid lines on the screen
def draw_grid(surface):
    for x in range(0, WIDTH, SQUARE_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, SQUARE_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))

def play_game():
    pygame.init()
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Snake Game")
    game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake_game = SnakeGame(game_surface)  # initialize SnakeGame instance

    mainloop = True
    while mainloop:
        draw_screen(game_surface)
        draw_grid(game_surface)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                elif event.key == pygame.K_LEFT:
                    snake_game.set_direction('left')
                elif event.key == pygame.K_RIGHT:
                    snake_game.set_direction('right')
                elif event.key == pygame.K_UP:
                    snake_game.set_direction('up')
                elif event.key == pygame.K_DOWN:
                    snake_game.set_direction('down')

        #update the snake game state
        snake_game.update() 

        clock.tick(40)  
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    play_game()
