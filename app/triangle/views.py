from otree.api import Currency as c, currency_range
from otree.api import safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np


#This class sends information to the Questions.html page
class Question(Page):
    form_model = models.Player
    form_fields = ['answer']

    #Creates text for answer options
     #def submitted_answer_choices(self):
         #qd = self.player.current_question()
    #     #Numbers for Option A
    #     a_p1 = int(100*float(qd['A_p1']))
    #     a_p3 = int(100*float(qd['A_p3']))
    #     a_p2 = int(100 - a_p1 - a_p3)
        
    #     #Numbers for Option B
    #     b_p1 = int(100*float(qd['B_p1']))
    #     b_p3 = int(100*float(qd['B_p3']))
    #     b_p2 = int(100 - a_p1 - a_p3)

    #     #Returns dynamic text options for A and B
         #return [
           # "How many zeros are in the table?"
          #  }

    #Creates data series that is passed to imbeded highchart triangle
    #Data takes form [[a1,a2],[b1,b2]]
    def vars_for_template(self):
        # #Array for single set of points
        # pointA = []
        # pointB = []
        # #Array to hold 2 sets of points
        # points = []
        # qd = self.player.current_question()

        # #Adding points for set A
        # pointA.append(float(qd['A_p1']))
        # pointA.append(float(qd['A_p3']))

        # #Adding points for set B
        # pointB.append(float(qd['B_p1']))
        # pointB.append(float(qd['B_p3']))

        # #Adding A and B to points
        # points.append(pointA)
        # points.append(pointB)

        # #This line is needed for the data to be passed to highcharts
        # #Without it the data is in the wrong form and will crash program
        # points = safe_json(points)

        m = np.random.randint(2, size=(10, 15))
        num_zero = (10*15) - np.count_nonzero(m)

        #Returns [[a1,a2],[b1,b2]] as a series
        return{
            #'series' : points,
            'matrix' : m,
            'num_zero' : num_zero,
        }

    def before_next_page(self):
       
        pass

#This class sends information to Results.html
class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        return {
            'player_in_all_rounds': player_in_all_rounds,
           
        }

#Order in which pages are displayed
page_sequence = [
    Question,
    Results
]