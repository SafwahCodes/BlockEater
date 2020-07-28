import pygame
from scenes import GameplayScene

class Main(object):

    def __init__(self, screen_x, screen_y, game_frame_left, game_frame_top, game_frame_width, game_frame_height, block_width_height):
        pygame.init()
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.surface = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption("Block Eater")
        self.clock = pygame.time.Clock()
        self.main_loop_running = True
        self.gameplay_fall_update_factor = 45

        # init game variables
        self.game_frame_left = game_frame_left
        self.game_frame_top = game_frame_top
        self.game_frame_width = game_frame_width
        self.game_frame_heignt = game_frame_height
        self.block_width_height = block_width_height

        # init initial scene
        self.scene = GameplayScene(self.screen_x, self.screen_y, game_frame_left, game_frame_top, game_frame_width, game_frame_height, block_width_height, self.gameplay_fall_update_factor)

    def main_loop(self):
        update_factor = 0
        while self.main_loop_running:

            if pygame.event.get(pygame.QUIT):
                self.main_loop_running = False

            #if update_factor == 45: # slows down block fall
            self.scene.update(pygame.event.get())
            #    update_factor = 0
            #else:
            #    update_factor += 1

            self.scene.draw(self.surface)

            pygame.display.update()
            self.clock.tick(60)

main = Main(440, 400, 0, 0, 240, 400, 20)
main.main_loop()

pygame.quit()
quit()