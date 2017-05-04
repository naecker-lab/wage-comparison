from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np
import random
import json
from django import forms

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
    name_in_url = 'counting-zeros1'
    #This is a 1-player game, so there are no groups of players
    players_per_group = 2
    num_rounds=1
    seqsize = 10
    seqthreshold=0.5
    price_per_correct_answer = 10
    #guess_max = 150

    #Create list of the matrices, and list of the number of zeros for each matrix
    #For each round number, the corresponding matrix and its number of zeros will be pulled
    # i1=0
    # p1=0
    # matrices1=[]
    # zeros1=[]
    # while i1<num_rounds:
    #   p1=np.random.uniform(0.3,0.7)
    #   matrices1.append(np.random.binomial(1, p1, size=(10, 15)))
    #   zeros1.append((10*15) - np.count_nonzero(matrices1[i1]))
    #   i1=i1+1

    # i2=0
    # p2=0
    # matrices2=[]
    # zeros2=[]
    # while i2<num_rounds:
    #   p2=np.random.uniform(0.3,0.7)
    #   matrices2.append(np.random.binomial(1, p2, size=(10, 15)))
    #   zeros2.append((10*15) - np.count_nonzero(matrices2[i2]))
    #   i2=i2+1


class Subsession(BaseSubsession):
  def before_session_starts(self):
    # if self.round_number == 1:
    #   for p in self.get_players():
    #     p.participant.vars['correct_answers'] = 0
    for p in self.get_players():
      p.seqdict=json.dumps({})

#Defines how groups opterate
#Since we do not have groups, class is not used
class Group(BaseGroup):
  # def average(self):
  #   players = self.get_players()
  #   total = 0
  #   for p in players:
  #       total+=p.participant.vars["correct_answers"]
  #   average = total/Constants.players_per_group
  #   for p in players:
  #       p.total = total
  #       p.average = average
  pass



#Defines attributes for each player
class Player(BasePlayer):
    # #player's answer for each matrix
    # #answer = models.PositiveIntegerField(max=Constants.guess_max)
    # #checks if player's answer matches the solution
    # is_correct = models.BooleanField()
    # #matrix number of zeros solution - will use for Results page
    # solution = models.PositiveIntegerField()
    # question_correct = models.BooleanField()
    # average = models.FloatField()
    # total = models.FloatField()
    seqdict=models.TextField()
    seqcounter=models.IntegerField(initial=0)
    sumcorrect=models.IntegerField(initial=0)


    #function that checks if player's answer is correct
    # def check_correct(self):
    #   if self.id_in_group==1:
    #     self.solution = Constants.zeros1[self.round_number-1]
    #     self.is_correct = (self.answer == Constants.zeros1[self.round_number-1])
    #   if self.id_in_group==2:
    #     self.solution = Constants.zeros2[self.round_number-1]
    #     self.is_correct = (self.answer == Constants.zeros2[self.round_number-1])

    # def other_player(self):
    #   return self.get_others_in_group()[0]


