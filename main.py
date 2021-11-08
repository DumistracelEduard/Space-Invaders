import pygame
from object_initializer import Initializer
from ui.Ui import Ui
import random
from entitati.bunker import Bunker

WIDTH = 900
HEIGHT = 600

FPS = 60

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (34, 203, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_PURPLE = (210, 0, 210)


def main():
    # Initialize imported pygame modules
    pygame.init()

    initializer = Initializer()

    # Set the window's caption
    pygame.display.set_caption("Space invaders")

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    background = pygame.image.load("images/space.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    '''background = pygame.Surface((WIDTH, HEIGHT))
    background = background.convert()
    background.fill(COLOR_BLACK)'''
    pygame.draw.line(background, COLOR_GREEN, [0, HEIGHT-50], [WIDTH, HEIGHT-50], 5)
    font = pygame.font.Font(None, 100)

    # Blit everything to screen
    screen.blit(background, (0, 0))

    # Update the screen
    pygame.display.flip()

    # Initialize game objects
    all_sprites_list = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    all_enemy_bullets = pygame.sprite.Group()
    all_ui_sprites = pygame.sprite.Group()
    all_bunker_bricks = pygame.sprite.Group()

    enemy_width3 = 40
    enemy_width2 = int(enemy_width3 * 22 / 24)
    enemy_width1 = int(enemy_width3 * 16 / 24)
    enemy_height = int((enemy_width3 * 16) / 24)

    player_width = enemy_width3+10
    player_height = int(player_width*256/414)

    player = initializer.initialize_player("images/cannon.png", WIDTH, HEIGHT, player_width, player_height)

    all_sprites_list.add(player)

    enemy_list = initializer.initialize_enemies(enemy_width1, enemy_width2, enemy_width3, enemy_height,
                                                "images/Alien3_2.png", "images/Alien1_2.png", "images/Alien2_1.png")

    for enemy in enemy_list:
        all_sprites_list.add(enemy)
        all_enemies.add(enemy)

    bunker_list = initializer.initialize_bunkers(WIDTH, HEIGHT)

    for bunker in bunker_list:
        all_sprites_list.add(bunker.brick_list)
        all_bunker_bricks.add(bunker.brick_list)

    score_file = "highscore.txt"
    ui = Ui(player.health, score_file)

    ui.score.rect.x = WIDTH / 2 - 100
    ui.score.rect.y = HEIGHT - 45

    ui.high_score.rect.x = WIDTH / 2 - 110
    ui.high_score.rect.y = HEIGHT - 20

    health_ui = []
    x = 15
    for health in range(player.health):
        ui.health_bar[health].rect.x = x
        ui.health_bar[health].rect.y = HEIGHT - 40
        health_ui.append(ui.health_bar[health])
        x += 60

    all_ui_sprites.add(ui.score)
    all_ui_sprites.add(ui.high_score)
    all_ui_sprites.add(health_ui)

    direction = 1

    enemy_tick = 300
    enemy_speed = int((WIDTH-(enemy_width3*11+170))/32)

    player_speed = 7

    MOVE_ENEMY = pygame.USEREVENT+1
    ENEMY_SHOOT = pygame.USEREVENT+2
    pygame.time.set_timer(MOVE_ENEMY, enemy_tick)
    pygame.time.set_timer(ENEMY_SHOOT, 500)

    is_playing = True

    txt = ''

    # Main loop
    while is_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
            if event.type == ENEMY_SHOOT:
                if len(all_enemies.sprites()) > 0:
                    enemies_shoot = random.choices(all_enemies.sprites(),
                                                   weights=[random.randint(1, 10) for e in all_enemies],
                                                   k=random.randint(1, 2))
                    for enemy in enemies_shoot:
                        bullet = enemy.shoot()
                        if bullet != None:
                            all_sprites_list.add(bullet)
                            all_enemy_bullets.add(bullet)
            if event.type == MOVE_ENEMY:
                if len(all_enemies.sprites()) > 0:
                    for enemy in all_enemies:
                        enemy.change_image()
                        if direction == 1:
                            enemy.move_right(enemy_speed)
                        else:
                            enemy.move_left(enemy_speed)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                while True:  # Infinite loop that will be broken when the user press the space bar again
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        is_playing = False
                        break
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        break  # Exit infinite loop

        for enemy in all_enemies:
            if enemy.rect.x > WIDTH-30-enemy.width:
                direction = -direction
                for enemy in all_enemies:
                    enemy.move_left(enemy_speed)
                    enemy.move_down(enemy.height)
                break
            elif enemy.rect.x < 30:
                direction = -direction
                for enemy in all_enemies:
                    enemy.move_right(enemy_speed)
                    enemy.move_down(enemy.height)
                break

        # Check for key presses and update paddles accordingly
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and player.rect.x > 30:
            player.move_left(player_speed)

        if keys_pressed[pygame.K_d] and player.rect.x < WIDTH-30-player.width:
            player.move_right(player_speed)

        if keys_pressed[pygame.K_LEFT] and player.rect.x > 30:
            player.move_left(player_speed)

        if keys_pressed[pygame.K_RIGHT] and player.rect.x < WIDTH-30-player.width:
            player.move_right(player_speed)

        if keys_pressed[pygame.K_SPACE]:
            bullet = player.shoot()
            if bullet != None:
                all_sprites_list.add(bullet)

        # Update game state
        if player.bullet.is_shot:
            player.bullet.move(-1)
        if player.bullet.rect.y < 0:
            player.bullet.is_shot = False
            all_sprites_list.remove(player.bullet)

        for bullet in all_enemy_bullets:
            bullet.move(1)

        for enemy in all_enemies:
            if enemy.bullet.rect.y > HEIGHT:
                enemy.bullet.is_shot = False
                all_enemy_bullets.remove(enemy.bullet)
                all_sprites_list.remove(enemy.bullet)

        if player.bullet.is_shot:
            enemy_collide_pbullet = pygame.sprite.spritecollide(player.bullet, all_enemies, True, pygame.sprite.collide_mask)
            for enemy in enemy_collide_pbullet:
                ui.score.change_score(ui.score.score+enemy.score)
                if ui.score.score > ui.high_score.score:
                    ui.high_score.change_score(ui.score.score)
                all_sprites_list.remove(enemy)
                player.bullet.is_shot = False
                all_sprites_list.remove(player.bullet)
                break
            bunker_colide_bullet = pygame.sprite.spritecollide(player.bullet, all_bunker_bricks, False, pygame.sprite.collide_mask)
            for brick in bunker_colide_bullet:
                brick.take_damage()
                if brick.health == 0:
                    all_bunker_bricks.remove(brick)
                    all_sprites_list.remove(brick)
                player.bullet.is_shot = False
                all_sprites_list.remove(player.bullet)
                break

        for brick in all_bunker_bricks:
            brick_collide_enemy = pygame.sprite.spritecollide(brick, all_enemy_bullets, False,
                                                              pygame.sprite.collide_mask)
            for bullet in brick_collide_enemy:
                brick.take_damage()
                if brick.health == 0:
                    all_bunker_bricks.remove(brick)
                    all_sprites_list.remove(brick)
                bullet.is_shot = False
                all_sprites_list.remove(bullet)
                all_enemy_bullets.remove(bullet)
                break

        player_collide_bullet = pygame.sprite.spritecollide(player, all_enemy_bullets, True, pygame.sprite.collide_mask)
        for bullet in player_collide_bullet:
            player.health -= 1
            if player.health <= 0:
                txt = 'Game Over'
            all_ui_sprites.remove(health_ui)
            health_ui.clear()
            x = 15
            for health in range(player.health):
                ui.health_bar[health].rect.x = x
                ui.health_bar[health].rect.y = HEIGHT - 40
                health_ui.append(ui.health_bar[health])
                x += 60
            all_ui_sprites.add(health_ui)
            all_sprites_list.remove(bullet)
            bullet.is_shot = False
            bullet.rect.y = 0

        for enemy in all_enemies:
            if enemy.rect.y+enemy.height >= player.rect.y:
                txt = 'Game Over'
                break

        all_sprites_list.update()
        all_ui_sprites.update()

        # Render current game state
        screen.blit(background, (0, 0))
        all_sprites_list.draw(screen)
        all_ui_sprites.draw(screen)
        if txt == 'Game Over':
            text = font.render(txt, True, (255, 0, 0))
            score = font.render(ui.score.score_type + str(ui.score.score), True, (255, 0, 255))
            high_score = font.render(ui.high_score.score_type + str(ui.high_score.score), True, (0, 0, 255))
            screen.blit(text, (WIDTH/2 - 200, HEIGHT/2 - 110))
            screen.blit(score, (WIDTH / 2 - 230, HEIGHT / 2 - 50))
            screen.blit(high_score, (WIDTH / 2 - 250, HEIGHT / 2 + 10))
            pygame.display.flip()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    is_playing = False
                    break
        if all_enemies.sprites() == []:
            txt = 'You Win'
            text = font.render(txt, True, (0, 255, 255))
            score = font.render(ui.score.score_type+str(ui.score.score), True, (255, 0, 255))
            high_score = font.render(ui.high_score.score_type+str(ui.high_score.score), True, (0, 0, 255))
            screen.blit(text, (WIDTH / 2 - 100, HEIGHT / 2 - 110))
            screen.blit(score, (WIDTH / 2 - 230, HEIGHT / 2 - 50))
            screen.blit(high_score, (WIDTH / 2 - 250, HEIGHT / 2 + 10))
            pygame.display.flip()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    is_playing = False
                    break

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()