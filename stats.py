class Stats():
    """Статистика класс"""

    def __init__(self):
        """Инициация статистики"""
        self.reset_stats()
        self.run_game = True
        with open('highscore.txt', 'r') as f:
            self.high_score = int(f.readline())

    def reset_stats(self):
        """Статистика во время игры"""
        self.guns_left = 2
        self.score = 0


