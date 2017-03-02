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


class Constants(BaseConstants):
    name_in_url = 'triangle'
    players_per_group = None

    with open('triangle/triangle.csv') as f:
        payoff_set = list(csv.DictReader(f))

    num_rounds = len(payoff_set)


class Subsession(BaseSubsession):


    def before_session_starts(self):
        if self.round_number == 1:
            self.session.vars['questions'] = Constants.payoff_set
       

        for p in self.get_players():
            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question = question_data['payoffset']



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    question_id = models.PositiveIntegerField()
    question = models.CharField()
    submitted_answer = models.CharField(widget=widgets.RadioSelect())


    def current_question(self):
        return self.session.vars['questions'][self.round_number - 1]


