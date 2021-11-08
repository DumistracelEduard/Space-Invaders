import pygame

class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("images/cannon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()