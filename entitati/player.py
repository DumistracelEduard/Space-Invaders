import pygame
from entitati.bullet import Bullet

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.width = width
        self.height = height
        self.color = color
        self.bullet = Bullet("images/Player_bullet.png", 7, 20, 10)
        self.health = 3

        if type(color) == type(()):
            self.image = pygame.Surface([width, height])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            pygame.draw.rect(self.image, self.color, [0, int(self.height/2), self.width, self.height])
            pygame.draw.line(self.image, self.color, [int(self.width/2), 0], [int(self.width/2), self.height], 5)
        else:
            self.image = pygame.image.load(color).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

    def move_right(self, pixels):
        self.rect.x += pixels

    def move_left(self, pixels):
        self.rect.x -= pixels

    def shoot(self):
        if not self.bullet.is_shot:
            self.bullet.is_shot = True
            self.bullet.rect.x = self.rect.x + self.width / 2
            self.bullet.rect.y = self.rect.y
            return self.bullet