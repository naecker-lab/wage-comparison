from otree.api import Currency as c, currency_range
from otree.api import safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants



class Question(Page):
    form_model = models.Player
    form_fields = ['submitted_answer']

    def submitted_answer_choices(self):
        qd = self.player.current_question()
        return [
           qd['a_p1']+"%"+" chance of "+qd['payoff1']+", "+qd['a_p2']+"%"+" chance of "+qd['payoff2']+", or "+qd['a_p3']+"%"+" chance of "+qd['payoff3'],
           qd['b_p1']+"%"+" chance of "+qd['payoff1']+", "+qd['b_p2']+"%"+" chance of "+qd['payoff2']+", or "+qd['b_p3']+"%"+" chance of "+qd['payoff3'],
        ]

    def vars_for_template(self):
        points = []
        points2 = []
        qd = self.player.current_question()

        points.append(float(qd['A_p1']))
        points.append(float(qd['A_p3']))
        points2.append(points)

        points = []
        points.append(float(qd['B_p1']))
        points.append(float(qd['B_p3']))
        points2.append(points)

        points2 = safe_json(points2)
        return{
            'series' : points2,
        }

    def before_next_page(self):
       
        pass


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {
            'player_in_all_rounds': player_in_all_rounds,
           
        }


page_sequence = [
    Question,
    Results
]
