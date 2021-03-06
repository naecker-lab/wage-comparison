from otree.api import Currency as c, currency_range
from otree.api import safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import numpy as np
import sys
import time
from otree.models_concrete import (PageTimeout, PageCompletion)
import random
import collections
import json 

def get_seq(size=Constants.seqsize, threshold=Constants.seqthreshold):
    # p = np.random.uniform(0.3,0.7)
    # seq1 = np.random.binomial(1, p, size=(Constants.seqsize, 1))
    # seq = seq1.tolist() # nested lists with same data, indices
    # file_path = "path.json" ## your path variable
    # json.dump(seq, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format
    seq = [random.random() for i in range(size)]
    seq = [0 if i < threshold else 1 for i in seq]
    
    return seq

def get_seqname(id):
    return 'seq' + str(id)

def update_seq_dict(seqdict, seq_id):
    seqname = get_seqname(seq_id)
    if seqname not in seqdict:
        seq = get_seq()
        corranswer = Constants.seqsize - sum(seq)
        seqdict[seqname] = {'seq_to_show': seq,
                            'corranswer': None,
                            'answer': None,
                            'name': str(seqname)}
    return seqdict


class Introduction(Page):
    # form_fields=['contribution']
    """Description of the game: How to play and returns expected"""

    #calls function to set the payoffs for each player
    def vars_for_template(self):
        self.group.set_payoffs()
        return {'x': self.player.contribution}

    def is_displayed(self):
        return self.round_number==1

    # def vars_for_template(self):
    #     x = self.player.contribution
    #     return {'x': x}


#This class sends information to the Questions.html page
class Question(Page):
    form_model = models.Player
    #form_fields = ['answer']

    #3-minute time limit
    # timeout_seconds = 30

    form_fields = ['seq']

    def get_timeout_seconds(self):
        return self.session.config['my_page_timeout_seconds']




    # def vars_for_template(self):
        #pull each matrix and its num of zeros
        #from the matrices list corresponding to the round number
        # if self.player.id_in_group == 1:
        #     m = Constants.matrices1[self.round_number-1]
        #     num_zero = Constants.zeros1[self.round_number-1]
        # #gather each array and replsce brackets with spaces for layout purposes
        #     matrixdict = {}
        #     for i in range(len(m)):
        #         matrixdict['m'+str(i+1)] = str(m[i]).replace('[','').replace(']','')
        # if self.player.id_in_group == 2:
        #     m = Constants.matrices2[self.round_number-1]
        #     num_zero = Constants.zeros2[self.round_number-1]
        # #gather each array and replsce brackets with spaces for layout purposes
        #     matrixdict = {}
        #     for i in range(len(m)):
        #         matrixdict['m'+str(i+1)] = str(m[i]).replace('[','').replace(']','')

        # questions_so_far = self.round_number-1

        # correct_so_far = sum([player.is_correct for player in self.player.in_previous_rounds()])



    def vars_for_template(self):
        # self.group.set_payoffs()


        #create array of 0's and 1's, and set up dictionary for the arrays and counter for correct answers
        seqdict = json.loads(self.player.seqdict)
        seqdict = update_seq_dict(seqdict, self.player.seqcounter)
        self.player.seqdict = json.dumps(seqdict)
        return {'seq': json.dumps(seqdict[get_seqname(self.player.seqcounter)])}


        # Returns these values to Question.html

        # return{
        #     #'series' : points,
        #     'matrix' : m,
        #     'num_zero' : num_zero,
        #     'm1' : matrixdict['m1'],
        #     'm2' : matrixdict['m2'],
        #     'm3' : matrixdict['m3'],
        #     'm4' : matrixdict['m4'],
        #     'm5' : matrixdict['m5'],
        #     'm6' : matrixdict['m6'],
        #     'm7' : matrixdict['m7'],
        #     'm8' : matrixdict['m8'],
        #     'm9' : matrixdict['m9'],
        #     'm10' : matrixdict['m10'],
        #     'questions_so_far' : questions_so_far,
        #     'correct_so_far' : correct_so_far,
        # }

    #check whether player's submitted answer is correct
#     def before_next_page(self):
#         self.player.check_correct()
#         if self.player.is_correct == True:
#             self.participant.vars["correct_answers"] +=1

# class ResultsWaitPage(WaitPage):
#     def is_displayed(self):
#         return self.round_number == Constants.num_rounds
#     def after_all_players_arrive(self):
#         self.group.average()

#after both players have reached the time limit, avg earnings/wages will be calculated
class ResultsWaitPage(WaitPage):
    # self.player.set_payoffs()
    # seqdict = json.loads(self.player.seqdict)
    # keys = [k for k, v in seqdict.items() if not v['answer']]
    # for x in keys:
    #     del seqdict[x]
    # for key, value in seqdict.items():
    #     seqdict[key]['corranswer'] = Constants.seqsize - sum(value['seq_to_show'])
    #     seqdict[key]['iscorrect'] = seqdict[key]['corranswer'] == int(seqdict[key]['answer'])
    #     seqdict[key]['seq_to_show'] = ''.join(str(e) for e in value['seq_to_show'])
    # self.player.sumcorrect = sum([v['iscorrect'] for k, v in seqdict.items()])
    # self.player.payoff = self.player.sumcorrect * \
    #     self.player.contribution
    

    def is_displayed(self):
        self.group.set_payoffs()
        seqdict = json.loads(self.player.seqdict)
        keys = [k for k, v in seqdict.items() if not v['answer']]
        for x in keys:
            del seqdict[x]
        for key, value in seqdict.items():
            seqdict[key]['corranswer'] = Constants.seqsize - sum(value['seq_to_show'])
            seqdict[key]['iscorrect'] = seqdict[key]['corranswer'] == int(seqdict[key]['answer'])
            seqdict[key]['seq_to_show'] = ''.join(str(e) for e in value['seq_to_show'])
        self.player.sumcorrect = sum([v['iscorrect'] for k, v in seqdict.items()])
        self.player.payoff = self.player.sumcorrect * \
            self.player.contribution
        # return self.round_number==1
        # self.group.average()
        return {'seq': seqdict}
    def after_all_players_arrive(self):
        # self.player.set_payoffs()
        # seqdict = json.loads(self.player.seqdict)
        # keys = [k for k, v in seqdict.items() if not v['answer']]
        # for x in keys:
        #     del seqdict[x]
        # for key, value in seqdict.items():
        #     seqdict[key]['corranswer'] = Constants.seqsize - sum(value['seq_to_show'])
        #     seqdict[key]['iscorrect'] = seqdict[key]['corranswer'] == int(seqdict[key]['answer'])
        #     seqdict[key]['seq_to_show'] = ''.join(str(e) for e in value['seq_to_show'])
        # self.player.sumcorrect = sum([v['iscorrect'] for k, v in seqdict.items()])
        # self.player.payoff = self.player.sumcorrect * \
        #     self.player.contribution
        # self.participant.vars['sequence'] = seqdict
        # if self.round_number == 1:
        self.group.averageearnings()
        self.group.averagewages()
		




# class Information_Wage(Page):
# 	def vars_for_template(self):
# 		x = "hello"
# 		return {'x': x}
# 	def is_displayed(self):
# 		return self.player.treat=='wage'


# class Information_Earnings(Page):
# 	def vars_for_template(self):
# 		x = "hello"
# 		return {'x': x}
# 	def is_displayed(self):
# 		return self.player.treat=='earnings'

#This class sends information to Results.html
class Results(Page):
    # def vars_for_templates(self):
    # 	return{'seq': self.participant.vars['sequence']}
    # def vars_for_template(self):
        # player_in_all_rounds = self.player.in_all_rounds()
        # #adds up all the times the player was correct
        # correct = sum([player.is_correct for player in player_in_all_rounds])

        # return {
        #     'player_in_all_rounds': player_in_all_rounds,
        #     'questions_correct': correct,
        #     'average': self.player.average

        # }

    def vars_for_template(self):
        
        self.group.set_payoffs()
        sequencedict = json.loads(self.player.seqdict)
        keys = [k for k, v in sequencedict.items() if not v['answer']]
        for x in keys:
            del sequencedict[x]
        for key, value in sequencedict.items():
            sequencedict[key]['corranswer'] = Constants.seqsize - sum(value['seq_to_show'])
            sequencedict[key]['iscorrect'] = sequencedict[key]['corranswer'] == int(sequencedict[key]['answer'])
            sequencedict[key]['seq_to_show'] = ''.join(str(e) for e in value['seq_to_show'])
        self.player.sumcorrect = sum([v['iscorrect'] for k, v in sequencedict.items()])
        
        self.player.payoff = self.player.sumcorrect * \
            self.player.contribution
        
        # if self.round_number == 1:
        if self.player.treat=='earnings':
            # self.player.avgearnings = (self.player.totalearnings - self.player.payoff)/(Constants.players_per_group - 1)
            self.player.avgearnings=(self.player.totalearnings - self.player.payoff)/(len(self.group.get_players())-1)

        if self.player.treat=='wage':
            self.player.avgwages = (self.player.totalwages-self.player.contribution)/(len(self.group.get_players())-1)


        # self.participant.vars['sequence'] = seqdict
        # self.group.average()
        # seq = self.participant.vars['sequence']

        # self.group.average()
        
        return {'seq': sequencedict,}

page_sequence = [
    Introduction,
    Question,
    ResultsWaitPage,
    # Information_Earnings,
    # Information_Wage,
    Results,

]
