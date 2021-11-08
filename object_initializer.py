from entitati.inamici import Enemy
from entitati.player import Player
from entitati.bunker import Bunker



class Initializer:
    def __init__(self):
        pass

    def initialize_player(self, color, WIDTH, HEIGHT, player_width, player_height):
        player = Player(color, player_width, player_height)
        player.rect.x = WIDTH / 2 - player_width/2
        player.rect.y = HEIGHT - 60 - player_height
        return player

    def initialize_bunkers(self, WIDTH, HEIGHT):
        x = 50
        y = HEIGHT - 180
        bunker_list = []
        for i in range(4):
            bunker_list.append(Bunker(96, 72, x, y))
            x += (WIDTH-96*4-100)/3+96
        return bunker_list

    def initialize_enemies(self, enemy_width1, enemy_width2, enemy_width3, enemy_height, color1, color2, color3):
        x = 40
        enemy_list = []
        for i in range(11):
            y = 80 + 3 * enemy_height + 30
            for k in range(2):
                enemy = Enemy(color3, enemy_width3, enemy_height, 10)
                enemy.rect.x = x
                enemy.rect.y = y
                y = y - enemy_height-10
                enemy_list.append(enemy)
            x += enemy_width2/22
            for k in range(2):
                enemy = Enemy(color2, enemy_width2, enemy_height, 20)
                enemy.rect.x = x
                enemy.rect.y = y
                y = y - enemy_height-10
                enemy_list.append(enemy)
            x += enemy_width1 * 3 / 16
            for k in range(1):
                enemy = Enemy(color1, enemy_width1, enemy_height, 30)
                enemy.rect.x = x
                enemy.rect.y = y
                y = y - enemy_height-10
                enemy_list.append(enemy)
            x = x - (enemy_width1 * 6 / 16) - (enemy_width2*2/22) + enemy_width3 + 17
        return enemy_list