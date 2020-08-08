import pygame
import pygame_menu
from game_items import Wall, Shape

class Scene(object):

    def __init__(self):
        pass

    def draw(self, surface):
        raise NotImplementedError
    
    def update(self, events):
        raise NotImplementedError

    def get_scene_type(self):
        raise NotImplementedError
    
class GameplayScene(Scene):

    def __init__(self, screen_x, screen_y, game_frame_left, game_frame_top, game_frame_width, game_frame_height, block_width_height, fall_update_factor):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.game_frame_left = game_frame_left
        self.game_frame_top = game_frame_top
        self.game_frame_width = game_frame_width
        self.game_frame_heignt = game_frame_height
        self.block_width_height = block_width_height
        self.fall_update_factor = fall_update_factor
        self.update_factor = 0
        self.width_block_no = int(self.game_frame_width / self.block_width_height)
        self.height_block_no = int(self.game_frame_heignt / self.block_width_height)

        # init focused shape
        self.focused_shape_x = (int((self.game_frame_width / self.block_width_height) / 2) - 1) * self.block_width_height
        self.focused_shape_y = -(self.block_width_height * 2)
        self.focused_shape = Shape(self.focused_shape_x, self.focused_shape_y, self.block_width_height)

        # init invisible walls - left, right, bottom
        self.wall_left = Wall(self.game_frame_left - self.block_width_height, self.focused_shape_y, self.block_width_height, screen_y, (0,0,0))
        self.wall_right = Wall(self.game_frame_left + self.game_frame_width, self.focused_shape_y, self.block_width_height, screen_y, (0,0,0))
        self.wall_bottom = Wall(self.game_frame_left, screen_y, self.game_frame_width, self.block_width_height, (0,0,0))
        self.wall_top = Wall(self.game_frame_left, -(self.block_width_height), self.game_frame_left + self.game_frame_width, self.block_width_height, (0,0,0))

        # init next focused shape and frame
        self.next_focused_shape_x = self.block_width_height * 16
        self.next_focused_shape_y = self.block_width_height * 5
        self.next_focused_shape = Shape(self.next_focused_shape_x, self.next_focused_shape_y, self.block_width_height)
        self.next_focused_shape_frame_rect = pygame.Rect(self.game_frame_width + (self.block_width_height * 2), self.block_width_height * 3, self.block_width_height * 6, self.block_width_height * 5)

        # init rest of blocks logic
        self.fixed_rects = []
        self.fixed_rects_color = []
        self.column_count_per_row = [[0 for _ in range(self.width_block_no)] for _ in range(self.height_block_no)]
        self.fixed_rects_dict = {}
        self.grid = [[False for _ in range(self.width_block_no)] for _ in range(self.height_block_no)]

    def get_scene_type(self):
        return 2

    def draw(self, surface):
        # background fill
        surface.fill((0, 0, 0))

        # walls
        self.wall_left.draw(surface)
        self.wall_right.draw(surface)
        self.wall_bottom.draw(surface)
        
        # frame background and outline
        pygame.draw.rect(surface, pygame.Color(64, 64, 64), pygame.Rect(self.game_frame_left, self.game_frame_top, self.game_frame_width, self.game_frame_heignt))
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255),pygame.Rect(self.game_frame_left, self.game_frame_top, self.game_frame_width,self.game_frame_heignt), 2)

        for i in range(self.game_frame_left, self.game_frame_left + self.game_frame_width + self.block_width_height, self.block_width_height):
            pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), pygame.Rect(i, 0, 1, self.screen_y))
        for j in range(0, self.screen_y + self.block_width_height, self.block_width_height):
            pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), pygame.Rect(self.game_frame_left, j, self.game_frame_width, 1))

        # focused frame
        pygame.draw.rect(surface, pygame.Color(255,255,255,255), self.next_focused_shape_frame_rect, 2)

        # next focused shape
        self.next_focused_shape.draw(surface)

        # focused shape
        self.focused_shape.draw(surface)

        # rest of blocks
        for y in range(0, len(self.grid)):
            for x in range(0, len(self.grid[y])):
                if (self.grid[y][x] != False):
                    rgb1, rgb2 = self.grid[y][x]
                    rect = pygame.Rect(x * self.block_width_height, y * self.block_width_height, self.block_width_height, self.block_width_height)
                    pygame.draw.rect(surface, rgb1, rect)
                    pygame.draw.rect(surface, rgb2, rect, 2)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # focused shape rotate
                    self.focused_shape.rotate() # need to fix
                elif event.key == pygame.K_LEFT: # focused shape move left
                    self.focused_shape.move_left()
                    if self.focused_shape.has_collide_wall(self.wall_left):
                        self.focused_shape.move_right()
                elif event.key == pygame.K_RIGHT: # focused shape move right
                    self.focused_shape.move_right()
                    if self.focused_shape.has_collide_wall(self.wall_right):
                        self.focused_shape.move_left()

        # focused shape
        if self.update_factor == self.fall_update_factor:
            self.focused_shape.update()
            self.update_factor = 0
        else:
            self.update_factor += 1

        # collision bottom wall
        if self.focused_shape.has_collide_wall(self.wall_bottom): # or self.focused_shape.has_collide_fixed(self.fixed_rects): # need to fix this
            self.focused_shape.move_up()
            self.fixed_rects.extend(self.focused_shape.rect_list)
            for i in range(0, len(self.focused_shape.rect_list)):
                rect = self.focused_shape.rect_list[i]
                x = int(rect.x / self.block_width_height)
                y = int(rect.y / self.block_width_height)
                self.grid[y][x] = (self.focused_shape.rgb1, self.focused_shape.rgb2)
            self.next_focused_shape.reset_coordinates(self.focused_shape_x,self.focused_shape_y)
            self.focused_shape = self.next_focused_shape
            self.next_focused_shape = Shape(self.next_focused_shape_x, self.next_focused_shape_y, self.block_width_height)
            
        # collision top wall - fixed shapes

        # row full deletion
        for row in reversed(self.grid):
            row_fill = 0
            for cell in row:
                if (cell == False):
                    break
                else:
                    row_fill += 1
            if (row_fill == self.width_block_no):
                index = self.grid.index(row)
                print("row " + str(index) + " is full")
                self.grid[index] = [False for _ in range(self.width_block_no)]
                #iterate through rows above this row to shift down
                print(*self.grid, sep="\n")
                print("\n")
                for i in range(index, -1, -1):
                    if (i > 0):
                        self.grid[i] = self.grid[i -1]
                    else:
                        self.grid[i] = [False for _ in range(self.width_block_no)]
                print(*self.grid, sep="\n")