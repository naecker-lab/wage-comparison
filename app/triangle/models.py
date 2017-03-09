from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv

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

   

    #Calls CSV from location within app folder
    with open('triangle/triangle.csv') as f:
        payoff_set = list(csv.DictReader(f))

    #Defines number of rounds as number of rows in CSV
    #Additional rounds can be addded by adding rows to CSV
    num_rounds = len(payoff_set)



class Subsession(BaseSubsession):

    #Keeps track of which row of the CSV the  app is pulling from for the current question
    def before_session_starts(self):
        if self.round_number == 1:
            self.session.vars['questions'] = Constants.payoff_set
       
        #Gets current row and then selects columns to extracdt needed data
        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question = "For Set " + str(question_data['id']) + " , which point would you prefer?" 

#Defines how groups opterate
#Since we do not have groups, classis not used
class Group(BaseGroup):
    pass


#Defines attributes for each player
class Player(BasePlayer):
    question_id = models.PositiveIntegerField()
    question = models.CharField()
    submitted_answer = models.CharField(widget=widgets.RadioSelect())


    def current_question(self):
        return self.session.vars['questions'][self.round_number - 1]