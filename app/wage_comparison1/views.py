from otree.api import Currency as c, currency_range
from otree.api import safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np
import sys
import time
from otree.models_concrete import (PageTimeout, PageCompletion)

from .gto_timeout_page import GTOPage



class Introduction(Page):
    pass

#This class sends information to the Questions.html page
class Question(GTOPage):
    general_timeout=True

    form_model = models.Player
    form_fields = ['answer']

    def vars_for_template(self):
        #pull each matrix and its num of zeros
        #from the matrices list corresponding to the round number
        if self.player.id_in_group == 1:
            m = Constants.matrices1[self.round_number-1]
            num_zero = Constants.zeros1[self.round_number-1]
        #gather each array and replsce brackets with spaces for layout purposes
            matrixdict = {}
            for i in range(len(m)):
                matrixdict['m'+str(i+1)] = str(m[i]).replace('[','').replace(']','')
        if self.player.id_in_group == 2:
            m = Constants.matrices2[self.round_number-1]
            num_zero = Constants.zeros2[self.round_number-1]
        #gather each array and replsce brackets with spaces for layout purposes
            matrixdict = {}
            for i in range(len(m)):
                matrixdict['m'+str(i+1)] = str(m[i]).replace('[','').replace(']','')

        questions_so_far = self.round_number-1

        correct_so_far = sum([player.is_correct for player in self.player.in_previous_rounds()])


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
            'questions_so_far' : questions_so_far,
            'correct_so_far' : correct_so_far,
        }

    #check whether player's submitted answer is correct
    def before_next_page(self):
        self.player.check_correct()
        if self.player.is_correct == True:
            self.participant.vars["correct_answers"] +=1

class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def after_all_players_arrive(self):
        self.group.average()


#This class sends information to Results.html
class Results(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        #adds up all the times the player was correct
        # problem: is_correct is not defined therefore looking for the sum does not occur
        # correct = sum([player.is_correct for player in player_in_all_rounds])

        return {
            'player_in_all_rounds': player_in_all_rounds,
            'questions_correct': correct,
            'average': self.player.average
        }

#Order in which pages are displayed
page_sequence = [
    Question,
    ResultsWaitPage,
    Results,
]
