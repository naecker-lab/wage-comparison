from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
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
    players_per_group = 2
    num_rounds=2
    seqsize = 100
    seqthreshold=0.5
    price_per_correct_answer = 10
    endowment = c(0)
    rand2 = random.sample(set([0.5, 0.1]),1)
    rand2 = rand2[0]
    rand1 = 0.6 - rand2
    # instructions_template = 'wage_comparison/Instructions.html'
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

            #assigns players to different treaments
            # for p in self.get_players():
            #     if 'treatment' in self.session.config:
            #         p.treat = self.session.config['treatment']
            #     else:
            #         p.treat=random.choice(['wage', 'earnings'])
    # def set_currency(self):
    #     rand1 = random.sample(set([0.1, 0.5]),1)
    #     rand2 = 0.6 - rand1
    #     if self.player.id_in_group == 1:
    #         self.player.payoff = rand1
    #     if self.player.id_in_group==2:
    #         self.player.payoff = rand2

#Defines how groups opterate
#Since we do not have groups, class is not used
class Group(BaseGroup):
    # total_payoff = models.CurrencyField()
    # indiv_payoff = models.CurrencyField()
  # def average(self):
  #   players = self.get_players()
  #   total = 0
  #   for p in players:
  #       total+=p.participant.vars["correct_answers"]
  #   average = total/Constants.players_per_group
  #   for p in players:
  #       p.total = total
  #       p.average = average
    # def set_payoffs(self):
        # rand1 = random.sample(set([0.1, 0.5]),1)
        # rand1 = rand1[0]
        # rand2 = 0.6 - rand1
        # self.total_payoff = sum([p.contribution for p in self.get_players()])
        # if self.id_in_group == 1:
        #     self.indiv_payoff = rand1
        # if self.id_in_group==2:
        #     self.indiv_payoff = rand2
        # for p in self.get_players():
        #     p.payoff = self.indiv_payoff
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
    seqdict = models.TextField()
    seqcounter = models.IntegerField(initial=0)
    sumcorrect = models.IntegerField(initial=0)
    contribution = models.CurrencyField()
    total_payoff = models.CurrencyField()
    indiv_payoff = models.CurrencyField()

    def set_payoffs(self):
        if self.id_in_group==1:
            self.contribution = Constants.rand1
        if self.id_in_group==2:
            self.contribution = Constants.rand2



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


