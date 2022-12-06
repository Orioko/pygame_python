import pygame

class Bullet(pygame.sprite.Sprite):

    def __init__(self, screen, gun):
        """Создаю пулю в позиции пушки"""
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 7, 7)
        self.color = 237, 28, 35
        self.speed = 4.5
        self.rect.centerx = gun.rect.centerx
        self.rect.top = gun.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """Перемещение пули вверх"""
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Рисуем пулю"""
        pygame.draw.rect(self.screen, self.color, self.rect)