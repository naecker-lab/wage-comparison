from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
from .views import Question
from otree.api import Submission


class PlayerBot(Bot):

    def play_round(self):
    	assert self.player.totalearnings==None
    	if self.subsession.round_number==1:
    		yield(views.Introduction)
    	yield Submission(views.Question, {'seq': ''}, timeout_happened=True, check_html=False)
    	assert self.player.totalearnings==0
    	yield (views.Results)