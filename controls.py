import pygame, sys
from bullet import Bullet
from ino import Ino
import time

def events(screen, gun, bullets):
    """Обработка событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            """Вправо"""
            if event.key == pygame.K_d:
                gun.mright = True
            elif event.key == pygame.K_a:
                gun.mleft = True
                """Влево"""
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)
                """Пуля"""
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                gun.mright = False
            elif event.key == pygame.K_a:
                gun.mleft = False


def update(background_image, screen, stats, sc, gun, inos, bullets):
    """Обновление экрана"""
    screen.blit(background_image, (0, 0))
    gun.update_gun()  # Обновление позиции пушки
    gun.output()  # Рисование пушки
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    inos.draw(screen)
    pygame.display.update()  # Используйте pygame.display.update() вместо pygame.display.flip()


def update_bullets(screen, stats, sc, inos, bullets):
    """Удаление пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for inos in collisions.values():
            stats.score += 10 * len(inos)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    if len(inos) == 0:
        bullets.empty()
        create_army(screen, inos)

    screen.fill((0, 0, 0), (0, 800, 800, 100))  # Закрашиваем нижнюю полоску черным цветом
    pygame.display.update()  # Используйте pygame.display.update() вместо pygame.display.flip()


def gun_kill(stats, screen, sc, gun, inos, bullets):
    """Столкновение пушки с пришельцами"""
    if stats.guns_left > 0:
        stats.guns_left -= 1
        sc.image_guns()
        inos.empty()
        bullets.empty()
        create_army(screen, inos)
        gun.create_gun()
        time.sleep(1)
    else:
        stats.run_game = False
        sys.exit()

def update_inos(stats, screen, sc, gun, inos, bullets):
    """Обновление местоположения пришельцев"""
    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(stats, screen, sc, gun, inos, bullets)
    inos_check(stats, screen, sc, gun, inos, bullets)

def inos_check(stats, screen, sc, gun, inos, bullets):
    """Проверка края экрана"""
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, sc, gun, inos, bullets)
            break

def create_army(screen, inos):
    """Армия пришельцев"""
    ino = Ino(screen)
    ino_width = ino.rect.width
    number_ino_x = int((700 - 2 * ino_width) / ino_width)
    ino_height = ino.rect.height
    number_ino_y = int((800 - 100 - 2 * ino_height) / ino_height)

    for row_number in range(number_ino_y - 6):
        for ino_number in range(number_ino_x):
            ino = Ino(screen)
            ino.x = ino_width + (ino_width * ino_number)
            ino.y = ino_height + (ino_height * row_number)
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + (ino.rect.height * row_number)
            inos.add(ino)

def check_high_score(stats, sc):
    """Проверка новых рекордов"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('highscore.txt', 'w') as f:
            f.write(str(stats.high_score))