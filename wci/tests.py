from otree.api import Currency as c, currency_range
from otree.api import SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants

from random import randint, choice
import itertools


class PlayerBot(Bot):

    def play_round(self):
        ## define valid inputs with solutions
        if 'simulate' in self.session.config:
            valid_decision1 = randint(1,4)
            valid_decision2 = randint(1,4)
            valid_questionnaire = {
                    'age': randint(18, 60),
                    'gender': choice(['male', 'female', 'other', 'I prefer not to tell']),
                    'education': randint(1, 7),
                    'field_of_study': choice(['economics', 'business', 'law', 'other']),
                    'occupation': choice(['student', 'teacher', 'other']),
                    'nationality': 'US',
                }
        else:
            valid_decision1 = 1
            valid_decision2 = 2
            valid_questionnaire = {
                    'age': 25,
                    'gender': 'female',
                    'education': 5,
                    'field_of_study': 'economics',
                    'occupation': 'student',
                    'nationality': 'US',
                }


        test_data = {
            'Introduction': {
                'invalid_inputs': {
                    'captcha_input': ['', 'a', -1, 0, 1, 19, 20, self.player.captcha_solution-1]
                },
                'valid_inputs': {
                    'captcha_input': self.player.captcha_solution
                }
            },
            'Decision1': {
                'invalid_inputs': {
                    'decision1': ['', 'a', -1, 0, 5]
                },
                'valid_inputs': {
                    'decision1': valid_decision1
                }
            },
            'Decision2': {
                'invalid_inputs': {
                    'decision2': ['', 'a', -1, 0, 5]
                },
                'valid_inputs': {
                    'decision2': valid_decision2
                }
            },
            'Questionnaire': {
                'invalid_inputs': {
                    'age': [-1, 'a', '', 130],
                    'gender': [1, 'cool', ''],
                    'education': [-1, 0, 'a', ''],
                    'field_of_study': [''],
                    'occupation': [''],
                    'nationality': ['GER', 'USA', 2],
                },
                'valid_inputs': valid_questionnaire
            }
        }

        ## Introduction
        # check invalid captcha inputs
        if not 'simulate' in self.session.config:
            for invalid_input in test_data['Introduction']['invalid_inputs']['captcha_input']:
                yield SubmissionMustFail(pages.Introduction, {'captcha_input': invalid_input})

        # valid captcha
        yield (pages.Introduction, test_data['Introduction']['valid_inputs'])


        ## Instructions 1 and 2 do not have any inputs
        yield (pages.Instructions1)
        yield (pages.Instructions2)
        yield (pages.DecisionAnnouncement)

        ## Decision 1
        # check invalid bet entries:
        if not 'simulate' in self.session.config:
            for invalid_input in test_data['Decision1']['invalid_inputs']['decision1']:
                yield SubmissionMustFail(pages.Decision1, {'decision1': invalid_input})

        # valid input
        yield (pages.Decision1, test_data['Decision1']['valid_inputs'])
        

        ## Decision 2
        # check invalid bet entries:
        if not 'simulate' in self.session.config:
            for invalid_input in test_data['Decision2']['invalid_inputs']['decision2']:
                yield SubmissionMustFail(pages.Decision2, {'decision2': invalid_input})

        # valid input
        yield (pages.Decision2, test_data['Decision2']['valid_inputs'])


        ## Questionnaire
        # check invalid inputs by combining all invalid inputs
        # these are only run, if specified in session config
        if not 'simulate' in self.session.config:
            keys, values = zip(*test_data['Questionnaire']['invalid_inputs'].items())
            for v in itertools.product(*values):
                yield SubmissionMustFail(pages.Questionnaire, dict(zip(keys, v)))

            # manually check invalid input "college education but no field of study"
            yield SubmissionMustFail(pages.Questionnaire, {
                'age': 30,
                'gender': 'male',
                'education': 5,
                'field_of_study': '',
                'occupation': 'Teacher',
                'nationality': 'US',
            })

        # check valid inputs
        yield (pages.Questionnaire, test_data['Questionnaire']['valid_inputs'])


        ## Ending does not have any inputs
        yield (pages.Ending)

        if not 'simulate' in self.session.config:
            ## Check if indicators are correct
            # economics
            assert self.player.economist 

            # gender
            assert self.player.female

            # order of decisions to order-invariant variables
            if self.player.order == 1:
                assert self.player.decision_blue == 1
                assert self.player.decision_grey == 2

                assert self.player.ambiguity_averse_blue
                assert not self.player.ambiguity_averse_grey

            else:
                assert self.player.decision_blue == 2
                assert self.player.decision_grey == 1

                assert not self.player.ambiguity_averse_blue
                assert self.player.ambiguity_averse_grey

            # WCI
            assert self.player.wci_violated

            if self.player.treatment in [1, 3]:
                assert self.player.gain_domain
                assert not self.player.loss_domain
            else:
                assert self.player.loss_domain
                assert not self.player.gain_domain

            if self.player.treatment in [1, 2]:
                assert self.player.blue_large_amount
                assert not self.player.blue_small_amount
            else:
                assert self.player.blue_small_amount
                assert not self.player.blue_large_amount

        # check indicators