import pygame
import random
import sys

pygame.init()

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 2 * GRID_X_OFFSET + 200
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 2 * GRID_Y_OFFSET

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

TETROMINO_SHAPES = {
    'I': [
        ['.....',
         '..#..',
         '..#..',
         '..#..',
         '..#..'],
        ['.....',
         '.....',
         '####.',
         '.....',
         '.....']
    ],
    'O': [
        ['.....',
         '.....',
         '.##..',
         '.##..',
         '.....']
    ],
    'T': [
        ['.....',
         '.....',
         '.#...',
         '###..',
         '.....'],
        ['.....',
         '.....',
         '.#...',
         '.##..',
         '.#...'],
        ['.....',
         '.....',
         '.....',
         '###..',
         '.#...'],
        ['.....',
         '.....',
         '.#...',
         '##...',
         '.#...']
    ],
    'S': [
        ['.....',
         '.....',
         '.##..',
         '##...',
         '.....'],
        ['.....',
         '.#...',
         '.##..',
         '..#..',
         '.....']
    ],
    'Z': [
        ['.....',
         '.....',
         '##...',
         '.##..',
         '.....'],
        ['.....',
         '..#..',
         '.##..',
         '.#...',
         '.....']
    ],
    'J': [
        ['.....',
         '.#...',
         '.#...',
         '##...',
         '.....'],
        ['.....',
         '.....',
         '#....',
         '###..',
         '.....'],
        ['.....',
         '.##..',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '..#..',
         '.....']
    ],
    'L': [
        ['.....',
         '..#..',
         '..#..',
         '.##..',
         '.....'],
        ['.....',
         '.....',
         '###..',
         '#....',
         '.....'],
        ['.....',
         '##...',
         '.#...',
         '.#...',
         '.....'],
        ['.....',
         '.....',
         '..#..',
         '###..',
         '.....']
    ]
}

TETROMINO_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

class Tetromino:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
        self.rotation = 0
        self.shapes = TETROMINO_SHAPES[shape]
    
    def get_rotated_shape(self):
        return self.shapes[self.rotation % len(self.shapes)]
    
    def get_cells(self):
        cells = []
        shape = self.get_rotated_shape()
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    cells.append((self.x + j, self.y + i))
        return cells

class TetrisGame:
    def __init__(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_random_tetromino()
        self.next_piece = self.get_random_tetromino()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.game_over = False
        self.move_time = 0
        self.move_speed = 150
        self.down_time = 0
        self.down_speed = 100
        self.last_move_left = False
        self.last_move_right = False
        self.last_move_down = False
        self.lock_delay = 0
        self.lock_delay_time = 500
        
    def get_random_tetromino(self):
        shape = random.choice(list(TETROMINO_SHAPES.keys()))
        color = TETROMINO_COLORS[shape]
        return Tetromino(shape, color)
    
    def is_valid_position(self, piece, dx=0, dy=0, rotation=None):
        if rotation is None:
            rotation = piece.rotation
        
        old_rotation = piece.rotation
        piece.rotation = rotation
        
        for x, y in piece.get_cells():
            new_x, new_y = x + dx, y + dy
            if (new_x < 0 or new_x >= GRID_WIDTH or 
                new_y >= GRID_HEIGHT or 
                (new_y >= 0 and self.grid[new_y][new_x] != BLACK)):
                piece.rotation = old_rotation
                return False
        
        piece.rotation = old_rotation
        return True
    
    def place_piece(self, piece):
        for x, y in piece.get_cells():
            if y >= 0:
                self.grid[y][x] = piece.color
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(cell != BLACK for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        
        lines_cleared = len(lines_to_clear)
        self.lines_cleared += lines_cleared
        self.score += lines_cleared * 100 * self.level
        
        if self.lines_cleared >= self.level * 10:
            self.level += 1
            self.fall_speed = max(50, self.fall_speed - 50)
    
    def update(self, dt, keys_pressed):
        if self.game_over:
            return
        
        self.move_time += dt
        self.down_time += dt
        self.lock_delay += dt
        
        left_pressed = keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]
        right_pressed = keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]
        down_pressed = keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]
        
        if left_pressed and (not self.last_move_left or self.move_time >= self.move_speed):
            if self.move_piece(-1):
                self.lock_delay = 0
            self.move_time = 0
        elif right_pressed and (not self.last_move_right or self.move_time >= self.move_speed):
            if self.move_piece(1):
                self.lock_delay = 0
            self.move_time = 0
        
        if down_pressed and (not self.last_move_down or self.down_time >= self.down_speed):
            if self.is_valid_position(self.current_piece, dy=1):
                self.current_piece.y += 1
                self.score += 1
            self.down_time = 0
        
        self.last_move_left = left_pressed
        self.last_move_right = right_pressed
        self.last_move_down = down_pressed
        
        if not (left_pressed or right_pressed):
            self.move_time = 0
        
        if not down_pressed:
            self.down_time = 0
        
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if self.is_valid_position(self.current_piece, dy=1):
                self.current_piece.y += 1
                self.lock_delay = 0
            else:
                if self.lock_delay >= self.lock_delay_time:
                    self.place_piece(self.current_piece)
                    self.clear_lines()
                    self.current_piece = self.next_piece
                    self.next_piece = self.get_random_tetromino()
                    self.lock_delay = 0
                    
                    # Check if new piece can be placed, try a few positions up if needed
                    placed = False
                    for y_offset in range(0, 4):
                        self.current_piece.y = -y_offset
                        if self.is_valid_position(self.current_piece):
                            placed = True
                            break
                    
                    if not placed:
                        self.game_over = True
            
            self.fall_time = 0
    
    def move_piece(self, dx):
        if self.is_valid_position(self.current_piece, dx=dx):
            self.current_piece.x += dx
            return True
        return False
    
    def rotate_piece(self):
        new_rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shapes)
        if self.is_valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece.rotation = new_rotation
    
    def drop_piece(self):
        while self.is_valid_position(self.current_piece, dy=1):
            self.current_piece.y += 1
        self.score += 2
    
    def restart(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.get_random_tetromino()
        self.next_piece = self.get_random_tetromino()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 0
        self.fall_speed = 500
        self.game_over = False
        self.move_time = 0
        self.down_time = 0
        self.last_move_left = False
        self.last_move_right = False
        self.last_move_down = False
        self.lock_delay = 0
        
        # Ensure the starting piece can be placed
        for y_offset in range(0, 4):
            self.current_piece.y = -y_offset
            if self.is_valid_position(self.current_piece):
                break

def draw_grid(screen, game):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(
                GRID_X_OFFSET + x * CELL_SIZE,
                GRID_Y_OFFSET + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, game.grid[y][x], rect)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_piece(screen, piece):
    for x, y in piece.get_cells():
        if y >= 0:
            rect = pygame.Rect(
                GRID_X_OFFSET + x * CELL_SIZE,
                GRID_Y_OFFSET + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, piece.color, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_text(screen, text, x, y, size=24, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_next_piece(screen, piece, x, y):
    shape = piece.get_rotated_shape()
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell == '#':
                rect = pygame.Rect(
                    x + j * 20,
                    y + i * 20,
                    20,
                    20
                )
                pygame.draw.rect(screen, piece.color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    
    game = TetrisGame()
    
    while True:
        dt = clock.tick(60)
        keys_pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    game.drop_piece()
                elif event.key == pygame.K_r and game.game_over:
                    game.restart()
        
        game.update(dt, keys_pressed)
        
        screen.fill(BLACK)
        draw_grid(screen, game)
        
        if not game.game_over:
            draw_piece(screen, game.current_piece)
        
        info_x = GRID_X_OFFSET + GRID_WIDTH * CELL_SIZE + 20
        draw_text(screen, f"Score: {game.score}", info_x, 50)
        draw_text(screen, f"Level: {game.level}", info_x, 80)
        draw_text(screen, f"Lines: {game.lines_cleared}", info_x, 110)
        
        draw_text(screen, "Next:", info_x, 150, size=18)
        draw_next_piece(screen, game.next_piece, info_x, 170)
        
        if game.game_over:
            draw_text(screen, "GAME OVER", info_x, 280, color=RED)
            draw_text(screen, "Press R to restart", info_x, 310, size=18)
        
        draw_text(screen, "Controls:", info_x, 360, size=20)
        draw_text(screen, "A/D or Left/Right: Move", info_x, 390, size=16)
        draw_text(screen, "W or Up: Rotate", info_x, 410, size=16)
        draw_text(screen, "S or Down: Soft drop", info_x, 430, size=16)
        draw_text(screen, "Space: Hard drop", info_x, 450, size=16)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()