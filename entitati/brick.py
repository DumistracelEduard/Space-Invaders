import pygame

class Brick(pygame.sprite.Sprite):
    def __init__(self, picture, width, height, x, y):
        super().__init__()

        self.width = width
        self.height = height
        self.picture = picture
        self.health = 4

        self.image = pygame.image.load(self.picture).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def take_damage(self):
        self.health -= 1
        if self.health >= 1:
            self.picture = self.picture[:-5] + str(4-self.health) + '.png'
            self.image = pygame.image.load(self.picture).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))