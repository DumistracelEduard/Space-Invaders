from ui.health_bar import HealthBar
from ui.score import Score

class Ui():
    def __init__(self, health, file_name):
        self.health_bar = []
        for i in range(health):
            self.health_bar.append(HealthBar())
        self.score = Score(score_type='Your Score: ')
        self.high_score = Score(file_name, "High Score: ")
