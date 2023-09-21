import pygame

class Context:
    WIDTH, HEIGHT = 320, 240
    def __init__(self) -> None:
        pygame.init()

    def get_graphic(self):
        return pygame.display.set_mode((Context.WIDTH, Context.HEIGHT))
    
    def get_width(self):
        return Context.WIDTH
    
    def get_height(self):
        return Context.HEIGHT