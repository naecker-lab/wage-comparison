from otree.api import Currency as c, currency_range
from otree.api import safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np
import sys


#This class sends information to the Questions.html page
class Question(Page):
    form_model = models.Player
    form_fields = ['answer']

    def vars_for_template(self):
        m = Constants.matrices[self.round_number-1]
        num_zero = Constants.zeros[self.round_number-1]
        #m = np.random.randint(2, size=(10, 15))
        #num_zero = (10*15) - np.count_nonzero(m)
        matrixdict = {}
        for i in range(len(m)):
            matrixdict['m'+str(i+1)] = str(m[i]).replace('[','').replace(']','')
        # Took away repeated code.

        # Returns these values to Question.html
        return{
            #'series' : points,
            'matrix' : m,
            'num_zero' : num_zero,
            'm1' : matrixdict['m1'],
            'm2' : matrixdict['m2'],
            'm3' : matrixdict['m3'],
            'm4' : matrixdict['m4'],
            'm5' : matrixdict['m5'],
            'm6' : matrixdict['m6'],
            'm7' : matrixdict['m7'],
            'm8' : matrixdict['m8'],
            'm9' : matrixdict['m9'],
            'm10' : matrixdict['m10'],
        }


    def before_next_page(self):
        self.player.check_correct()

#This class sends information to Results.html
class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        correct = sum([player.is_correct for player in player_in_all_rounds])

        return {
            'player_in_all_rounds': player_in_all_rounds,
            'questions_correct': correct,
        }

#Order in which pages are displayed
page_sequence = [
    Question,
    Results
]
