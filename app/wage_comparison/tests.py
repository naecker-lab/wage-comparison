from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
from .views import Question
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
        # submitted_answer = self.player.current_question()['choice1']
        # answer = num_zero
        yield (views.Introduction)
        yield Submission(views.Question, {'sumcorrect': 0}, check_html=False)

        yield (views.Results)
        # yield Submission(views.Question, {'sumcorrect': 0}, check_html=False)
        # yield (views.Results)


        # yield (views.Question, {'contribution': 50})
        # yield(views.Results)
        
