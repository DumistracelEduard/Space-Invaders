import pygame

WHITE = (255, 255, 255)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, color, width, height,  speed):
        super().__init__()

        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.is_shot = False

        if type(color) == type(()):
            self.image = pygame.Surface([10, 20])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            pygame.draw.line(self.image, self.color, [0, 0], [0, 20], 10)
        else:
            self.image = pygame.image.load(color).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

    def move(self, pixels):
        self.rect.y += pixels*self.speed