import pygame
import random
from game_settings import *
from copy import deepcopy
from random import randrange, choice

class SnakeSquare:
    def __init__(self, pos, surface, is_apple=False):
        self.pos = pos
        self.surface = surface
        self.is_apple = is_apple
        self.is_tail = False
        self.dir = [-1, 0]  # [x, y] direction

        if self.is_apple:
            self.dir = [0, 0]

    #drawing the snake square/apple based on its type and direction
    def draw(self, color=SNAKE_COLOR):
        x, y = self.pos[0], self.pos[1]
        ss, gs = SQUARE_SIZE, GAP_SIZE

        #calculate the rectangle coordinates and size for drawing the square.
        draw_rect = (x * ss + gs, y * ss + gs, ss - 2 * gs, ss - 2 * gs)

        if self.dir == [-1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, color, draw_rect)
            else:
                pygame.draw.rect(self.surface, color, (x * ss + gs, y * ss + gs, ss, ss - 2 * gs))

        elif self.dir == [1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, color, draw_rect)
            else:
                pygame.draw.rect(self.surface, color, (x * ss - gs, y * ss + gs, ss, ss - 2 * gs))

        elif self.dir == [0, 1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, color, draw_rect)
            else:
                pygame.draw.rect(self.surface, color, (x * ss + gs, y * ss - gs, ss - 2 * gs, ss))

        elif self.dir == [0, -1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, color, draw_rect)
            else:
                pygame.draw.rect(self.surface, color, (x * ss + gs, y * ss + gs, ss - 2 * gs, ss))

        if self.is_apple:
            pygame.draw.rect(self.surface, APPLE_COLOR, draw_rect)

    #update the position of the square based on its direction
    def move(self, direction):
        self.dir = direction
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]

    #check if the square is hitting the wall
    def hitting_wall(self):
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False


class SnakeGame:
    # initialize the game with initial settings
    def __init__(self, surface):
        self.surface = surface
        self.is_dead = False
        self.squares_start_pos = [[ROWS // 2 + i, ROWS // 2] for i in range(INITIAL_SNAKE_LENGTH)]
        self.turns = {}
        self.dir = [-1, 0]
        self.score = 0
        self.moves_without_eating = 0
        self.apple = SnakeSquare([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)

        #create the initial snake
        self.squares = []
        for pos in self.squares_start_pos:
            self.squares.append(SnakeSquare(pos, self.surface))

        self.head = self.squares[0]
        self.tail = self.squares[-1]
        self.tail.is_tail = True

        self.path = []
        self.is_virtual_snake = False
        self.total_moves = 0
        self.won_game = False

    # draw the apple & the snake on the surface
    def draw(self):
        self.apple.draw(APPLE_COLOR)
        self.head.draw(HEAD_COLOR)
        for sqr in self.squares[1:]:
            if self.is_virtual_snake:
                sqr.draw(VIRTUAL_SNAKE_COLOR)
            else:
                sqr.draw()

    # set the direction of the snake based on user input
    def set_direction(self, direction):
        new_direction = {
            'left': [-1, 0],
            'right': [1, 0],
            'up': [0, -1],
            'down': [0, 1]
        }.get(direction)

        if new_direction and (new_direction[0] != -self.dir[0] or new_direction[1] != -self.dir[1]):
            self.dir = new_direction
            self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    #handle keyboard and other events
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # set snake direction using keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.set_direction('left')
        elif keys[pygame.K_RIGHT]:
            self.set_direction('right')
        elif keys[pygame.K_UP]:
            self.set_direction('up')
        elif keys[pygame.K_DOWN]:
            self.set_direction('down')

    #move the snake based on its direction and turns
    def move(self):
        for j, sqr in enumerate(self.squares):
            p = (sqr.pos[0], sqr.pos[1])
            if p in self.turns:
                turn = self.turns[p]
                sqr.move([turn[0], turn[1]])
                if j == len(self.squares) - 1:
                    self.turns.pop(p)
            else:
                sqr.move(sqr.dir)
        self.moves_without_eating += 1

    #add a new square to the snake when it eats an apple
    def add_square(self):
        self.squares[-1].is_tail = False
        tail = self.squares[-1]  

        direction = tail.dir
        if direction == [1, 0]:
            self.squares.append(SnakeSquare([tail.pos[0] - 1, tail.pos[1]], self.surface))
        if direction == [-1, 0]:
            self.squares.append(SnakeSquare([tail.pos[0] + 1, tail.pos[1]], self.surface))
        if direction == [0, 1]:
            self.squares.append(SnakeSquare([tail.pos[0], tail.pos[1] - 1], self.surface))
        if direction == [0, -1]:
            self.squares.append(SnakeSquare([tail.pos[0], tail.pos[1] + 1], self.surface))

        self.squares[-1].dir = direction
        self.squares[-1].is_tail = True  

    #reset the game
    def reset(self):
        self.__init__(self.surface)

    #check if the snake is hitting itself
    def hitting_self(self):
        for sqr in self.squares[1:]:
            if sqr.pos == self.head.pos:
                return True

    #generate a new apple in a random position
    def generate_apple(self):
        self.apple = SnakeSquare([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)
        if not self.is_position_free(self.apple.pos):
            self.generate_apple()

    #check if the snake's head is on the apple
    def eating(self):
        if self.head.pos == self.apple.pos and not self.is_virtual_snake and not self.won_game:
            self.generate_apple()
            self.moves_without_eating = 0
            self.score += 1
            return True

    #set the direction to move towards a given position
    def go_to(self, position): 
        if self.head.pos[0] - 1 == position[0]:
            self.set_direction('left')
        if self.head.pos[0] + 1 == position[0]:
            self.set_direction('right')
        if self.head.pos[1] - 1 == position[1]:
            self.set_direction('up')
        if self.head.pos[1] + 1 == position[1]:
            self.set_direction('down')

    #check if a given position is free (not occupied by the snake)
    def is_position_free(self, position):
        if position[0] >= ROWS or position[0] < 0 or position[1] >= ROWS or position[1] < 0:
            return False
        for sqr in self.squares:
            if sqr.pos == position:
                return False
        return True

    # BFS algorithm for pathfinding
    def bfs(self, start, end):  
        q = [start]  
        visited = {tuple(pos): False for pos in GRID}
        visited[start] = True
        prev = {tuple(pos): None for pos in GRID}

        while q:  
            node = q.pop(0)
            neighbors = ADJACENCY_DICT[node]
            for next_node in neighbors:
                if self.is_position_free(next_node) and not visited[tuple(next_node)]:
                    q.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list()
        p_node = end 

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:
                return []
            p_node = prev[p_node]
            if p_node == start:
                path.append(end)
                return path
            path.insert(0, p_node)

        return []  # path not available

    # creates a copy (virtual) of snake 
    def create_virtual(self):  
        v_snake = SnakeGame(self.surface)
        for i in range(len(self.squares) - len(v_snake.squares)):
            v_snake.add_square()

        for i, sqr in enumerate(v_snake.squares):
            sqr.pos = deepcopy(self.squares[i].pos)
            sqr.dir = deepcopy(self.squares[i].dir)

        v_snake.dir = deepcopy(self.dir)
        v_snake.turns = deepcopy(self.turns)
        v_snake.apple.pos = deepcopy(self.apple.pos)
        v_snake.apple.is_apple = True
        v_snake.is_virtual_snake = True

        return v_snake

    # get the path from the head to the tail
    def get_path_to_tail(self):
        tail_pos = deepcopy(self.squares[-1].pos)
        self.squares.pop(-1)
        path = self.bfs(tuple(self.head.pos), tuple(tail_pos))
        self.add_square()
        return path

    # get valid neighboring positions
    def get_available_neighbors(self, pos):
        valid_neighbors = []
        neighbors = get_neighbors(tuple(pos))
        for n in neighbors:
            if self.is_position_free(n) and self.apple.pos != n:
                valid_neighbors.append(tuple(n))
        return valid_neighbors

    # find the longest path to the tail
    def longest_path_to_tail(self):
        neighbors = self.get_available_neighbors(self.head.pos)
        path = []
        if neighbors:
            max_distance = -9999
            for n in neighbors:
                if distance(n, self.squares[-1].pos) > max_distance:
                    v_snake = self.create_virtual()
                    v_snake.go_to(n)
                    v_snake.move()
                    if v_snake.eating():
                        v_snake.add_square()
                    if v_snake.get_path_to_tail():
                        path.append(n)
                        max_distance = distance(n, self.squares[-1].pos)
            if path:
                return [path[-1]]
        return []

    # find any safe move for the snake
    def any_safe_move(self):
        neighbors = self.get_available_neighbors(self.head.pos)
        if neighbors:
            random_move = random.choice(neighbors)
            v_snake = self.create_virtual()
            v_snake.go_to(random_move)
            v_snake.move()
            if v_snake.get_path_to_tail():
                return [random_move]
        return self.get_path_to_tail()

    # set the path for the snake to follow
    def set_path(self):
        if self.score == SNAKE_MAX_LENGTH - 1 and self.apple.pos in get_neighbors(self.head.pos):  # Use imported get_neighbors
            winning_path = [tuple(self.apple.pos)]
            print('Snake is about to win')
            return winning_path

        v_snake = self.create_virtual()
        path_1 = v_snake.bfs(tuple(v_snake.head.pos), tuple(v_snake.apple.pos))
        path_2 = []

        if path_1:
            for pos in path_1:
                v_snake.go_to(pos)
                v_snake.move()

            v_snake.add_square() 
            path_2 = v_snake.get_path_to_tail()

        if path_2:  
            return path_1  

        if self.longest_path_to_tail() and \
                self.score % 2 == 0 and \
                self.moves_without_eating < MAX_MOVES_WITHOUT_EATING / 2:
            return self.longest_path_to_tail()

        if self.any_safe_move():
            return self.any_safe_move()

        if self.get_path_to_tail():
            return self.get_path_to_tail()

        print('No available path, snake in danger!')
        return []

    # update the game state
    def update(self):
        self.handle_events()
        self.path = self.set_path()
        if self.path:
            self.go_to(self.path[0])
        self.draw()
        self.move()
        
        if self.score == ROWS * ROWS - INITIAL_SNAKE_LENGTH:
            self.won_game = True
            print("Snake won the game after {} moves".format(self.total_moves))
            pygame.time.wait(1000 * WAIT_SECONDS_AFTER_WIN)
            return 1
        
        self.total_moves += 1
        
        if self.hitting_self() or self.head.hitting_wall():
            print("Snake is dead")
            self.is_dead = True
            self.reset()
        
        if self.moves_without_eating == MAX_MOVES_WITHOUT_EATING:
            self.is_dead = True
            print("Snake got stuck")
            self.reset()
        
        if self.eating():
            self.add_square()