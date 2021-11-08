import pygame
from entitati.brick import Brick

WHITE = (255, 255, 255)

class Bunker(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()

        self.width = width
        self.height = height
        self.brick_list = []

        self.image = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        for i in range(3):
            for j in range(4):
                if i == 2 and (j == 1 or j == 2):
                    continue
                if i == j == 0:
                    self.brick_list.append(Brick("images/Bunker_top_left_0.png", int(self.width / 4), int(self.height / 3),
                                                 x+(self.width / 4)*j, y+(self.height / 3)*i))
                elif i == 0 and j == 3:
                    self.brick_list.append(Brick("images/Bunker_top_right_0.png", int(self.width / 4), int(self.height / 3),
                                                 x + (self.width / 4) * j, y + (self.height / 3) * i))
                elif i == j == 1:
                    self.brick_list.append(Brick("images/Bunker_bottom_left_0.png", int(self.width / 4), int(self.height / 3),
                                                 x + (self.width / 4) * j, y + (self.height / 3) * i))
                elif i == 1 and j == 2:
                    self.brick_list.append(Brick("images/Bunker_bottom_right_0.png", int(self.width / 4), int(self.height / 3),
                                                 x + (self.width / 4) * j, y + (self.height / 3) * i))
                else:
                    self.brick_list.append(Brick("images/Bunker_brick_0.png", int(self.width / 4), int(self.height / 3),
                                             x+(self.width / 4)*j, y+(self.height / 3)*i))
                self.image.blit(self.brick_list[-1].image, ((self.width / 4)*j, (self.height / 3)*i))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y