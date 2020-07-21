import pygame
import pygame_menu
from game_items import Shape

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

    def __init__(self, screen_x, screen_y, game_frame_left, game_frame_top, game_frame_width, game_frame_height, block_width_height):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.game_frame_left = game_frame_left
        self.game_frame_top = game_frame_top
        self.game_frame_width = game_frame_width
        self.game_frame_heignt = game_frame_height
        self.block_width_height = block_width_height

        # init next focused shape
        self.next_focused_shape = Shape(500, 100, self.block_width_height)

        # init focused shape
        self.focused_shape = Shape(280,-(40), self.block_width_height)

        # init rest of blocks logic
        
    
    def get_scene_type(self):
        return 2

    def draw(self, surface):
        # draw background fill
        surface.fill((0, 0, 0))
        
        # draw frame background and outline
        pygame.draw.rect(surface, pygame.Color(64, 64, 64), pygame.Rect(self.game_frame_left, self.game_frame_top, self.game_frame_width, self.game_frame_heignt))
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255),pygame.Rect(self.game_frame_left, self.game_frame_top, self.game_frame_width,self.game_frame_heignt), 2)

        for i in range(self.game_frame_left, self.game_frame_left + self.game_frame_width + self.block_width_height, self.block_width_height):
            pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), pygame.Rect(i, 0, 1, self.screen_y))
        for j in range(0, self.screen_y + self.block_width_height, self.block_width_height):
            pygame.draw.rect(surface, pygame.Color(255, 255, 255, 255), pygame.Rect(self.game_frame_left, j, self.game_frame_width, 1))

        # draw focused frame
        pygame.draw.rect(surface, pygame.Color(255,255,255,255), pygame.Rect(450,60,120,100), 2)

        # draw next focused shape
        self.next_focused_shape.draw(surface)

        # draw focused shape
        self.focused_shape.draw(surface)

        # draw rest of blocks

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass # focused shape rotate

        self.focused_shape.update()