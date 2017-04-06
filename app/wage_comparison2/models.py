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
    name_in_url = 'counting-zeros2'
    #This is a 1-player game, so there are no groups of players
    players_per_group = 2
    num_rounds=10
    guess_max = 150

    #Create list of the matrices, and list of the number of zeros for each matrix
    #For each round number, the corresponding matrix and its number of zeros will be pulled
    i=0
    p=0
    matrices=[]
    zeros=[]
    while i<num_rounds:
      p=np.random.uniform(0.3,0.7)
      matrices.append(np.random.binomial(1, p, size=(10, 15)))
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
    #player's answer for each matrix
    answer = models.PositiveIntegerField(max=Constants.guess_max)
    #checks if player's answer matches the solution
    is_correct = models.BooleanField()
    #matrix number of zeros solution - will use for Results page
    solution = models.PositiveIntegerField()
    question_correct = models.BooleanField()

    #function that checks if player's answer is correct
    def check_correct(self):
      self.solution = Constants.zeros[self.round_number-1]
      self.is_correct = (self.answer == Constants.zeros[self.round_number-1])


