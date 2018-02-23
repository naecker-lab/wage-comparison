from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
from .views import Question
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):

        yield (views.Introduction)
        yield Submission(views.Question, {'seq': ''}, timeout_happened=True, check_html=False)

        yield (views.Results)

        yield Submission(views.Question, {'seq': ''}, timeout_happened=True, check_html=False)

        yield(views.Results)


        
#Add bot that sometimes submits the right answer and sometime submits the wrong answer
#Add bot that always submits wrong answer
#Add bot that submits nothing, just lets timer expire