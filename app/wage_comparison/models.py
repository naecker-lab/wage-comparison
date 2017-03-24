from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np

author = 'Your name here'

doc = """
A quiz app that reads its questions from a spreadsheet
(see triangle.csv in this directory).
There is 1 set of payoffs withing the triangle per page;
the number of pages in the game
is determined by the number of payoff sets in the CSV.
See the comment below about how to randomize the order of pages.
"""

#Defines attributes of game that remain constant throughout game
class Constants(BaseConstants):
    name_in_url = 'counting-zeros'
    #This is a 1-player game, so there are no groups of players
    players_per_group = None
    num_rounds=5
    guess_max = 150

    i=0
    matrices=[]
    zeros=[]
    while i<num_rounds:
      matrices.append(np.random.randint(2, size=(10, 15)))
      zeros.append((10*15) - np.count_nonzero(matrices[i]))
      i=i+1


class Subsession(BaseSubsession):
  pass

#Defines how groups opterate
#Since we do not have groups, class is not used
class Group(BaseGroup):
    pass


#Defines attributes for each player
class Player(BasePlayer):
    answer = models.PositiveIntegerField(max=Constants.guess_max)
    is_correct = models.BooleanField()
    solution = models.PositiveIntegerField()

    def check_correct(self):
      self.solution = Constants.zeros[self.round_number-1]
      self.is_correct = (self.answer == Constants.zeros[self.round_number-1])
