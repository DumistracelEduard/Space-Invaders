import pygame
from entitati.bullet import Bullet

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, width, height, score):
        super().__init__()

        self.width = width
        self.height = height
        self.color = color
        self.score = score
        self.bullet = Bullet("images/Enemy_bullet.png", 10, 20, 10)

        if type(color) == type(()):
            self.image = pygame.Surface([width, height])
            self.image.fill(WHITE)
            self.image.set_colorkey(WHITE)
            pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        else:
            self.image = pygame.image.load(color).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

    def move_right(self, pixels):
        self.rect.x += pixels

    def move_left(self, pixels):
        self.rect.x -= pixels

    def move_down(self, pixels):
        self.rect.y += pixels

    def change_image(self):
        if type(self.color) == type(''):
            if '1.png' in self.color:
                self.color = self.color[:-5]+'2.png'
            else:
                self.color = self.color[:-5]+'1.png'
            self.image = pygame.image.load(self.color).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def shoot(self):
        if not self.bullet.is_shot:
            self.bullet.is_shot = True
            self.bullet.rect.x = self.rect.x + self.width/2
            self.bullet.rect.y = self.rect.y + self.height/2
            return self.bullet


