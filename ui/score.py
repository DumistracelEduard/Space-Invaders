import pygame

WHITE = (255, 255, 255)

class Score(pygame.sprite.Sprite):
    def __init__(self, file_name = None, score_type = 'Score: '):
        super().__init__()

        self.score_type = score_type
        self.score = 0

        self.file_name = file_name

        if self.file_name != None:
            f = open(self.file_name, 'rt')
            self.score = int(f.readline())
            f.close()

        self.image = pygame.Surface([200, 50], pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.font = pygame.font.Font(None, 30)
        self.image = self.font.render(self.score_type+str(self.score), True, (255, 255, 255))

        self.rect = self.image.get_rect()

    def save_score(self):
        f = open(self.file_name, 'wt')
        f.write(str(self.score))
        f.close()

    def change_score(self, score):
        self.score = score
        self.image = self.font.render(self.score_type + str(self.score), True, (255, 255, 255))
        if self.file_name != None:
            self.save_score()