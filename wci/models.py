from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
)

import random

author = 'Christian König genannt Kersting'

doc = """
This is software for an experiment to directly test Weak Certainty Independence.
The project is co-authored with Christopher Kops and Stefan T. Trautmann.
"""


class Constants(BaseConstants):
    name_in_url = 'wci'
    players_per_group = None
    num_rounds = 1

    # define treatment and order names
    treatment_names = {
        1: "blue large - gain",
        2: "blue large - loss",
        3: "blue small - gain",
        4: "blue small - loss",
        5: "blue large - gain - both",
        6: "blue large - loss - both"
    }

    # define order names
    order_names = {
        1: "blue first",
        2: "blue second"
    }

    # bets that imply preference for risky over ambiguous box
    bet_on_risky_box = [1, 3]


    # Depending on treatment, order and decision numner,
    # which bets correspond to a preference for black over white, i.e. where does black yield a higher payoff?
    # bet_on_black_winning = [1, 2]

    # economist indicator
    economics_expressions = [
        "economist", "economics", "economy", "economic"
    ]

    treatments_to_play_if_random = [1, 2]


class Subsession(BaseSubsession):
    def creating_session(self):
        # setup player objects
        for player in self.get_players():
            # set treatment
            if 'treatment' in self.session.config:
                player.treatment = self.session.config['treatment']
            else:
                player.treatment = random.choice(Constants.treatments_to_play_if_random)

            # set gain / loss domain treatment indicators
            if player.treatment in [1, 3, 5]:
                player.gain_domain = True
            else:
                player.gain_domain = False

            player.loss_domain = not player.gain_domain

            # set low / high expected value in blue state indicators
            if player.treatment in [3, 4]:
                player.blue_small_amount = True
            else:
                player.blue_small_amount = False

            player.blue_large_amount = not player.blue_small_amount

            # set treatment name
            player.treatment_name = Constants.treatment_names[player.treatment]


            # set order
            if 'order' in self.session.config:
                player.decision_order = self.session.config['order']
            else:
                player.decision_order = random.randint(1, 2)

            # set order name
            player.order_name = Constants.order_names[player.decision_order]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Treatment and order
    treatment = models.IntegerField(min=1, max=6)
    treatment_name = models.StringField()
    decision_order = models.IntegerField(min=1, max=2)
    order_name = models.StringField()

    captcha = models.BooleanField(initial=False)

    def captcha_error_message(self, value):
        if not value:
            return "Please complete the captcha."

    # choices
    decision1 = models.IntegerField(choices=[(1,""), (2, ""), (3, ""), (4, "")], widget=widgets.RadioSelect)
    decision2 = models.IntegerField(choices=[(1,""), (2, ""), (3, ""), (4, "")], widget=widgets.RadioSelect)


    # demographics
    age = models.IntegerField(verbose_name="How old are you?", max=120)
    gender = models.StringField(choices=["female", "male", "other", "I prefer not to tell"],
        label="What is your gender?", widget=widgets.RadioSelectHorizontal)
    education = models.IntegerField(verbose_name="Which is the highest level of education you have attained?",
        choices=[
            (1, "some High School"),
            (2, "High School Graduate"),
            (3, "some College, no degree"),
            (4, "Associates degree"),
            (5, "Bachelor’s degree"),
            (6, "Master’s degree"),
            (7, "Doctorate degree")
        ],
        widget=widgets.RadioSelect
    )
    field_of_study = models.StringField(label="If you have at least some college education, what is/was your field of study?", blank=True)
    occupation = models.StringField(label="What is your main occupation?")
    nationality = models.StringField()

    # additional variables computed from inputs:
    female = models.BooleanField()
    economist = models.BooleanField()

    decision_blue = models.IntegerField(min=1, max=4)
    decision_grey = models.IntegerField(min=1, max=4)

    ambiguity_averse_decision1 = models.BooleanField()
    ambiguity_averse_decision2 = models.BooleanField()
    ambiguity_averse_blue = models.BooleanField()
    ambiguity_averse_grey = models.BooleanField()

    wci_violated = models.BooleanField()

    gain_domain = models.BooleanField()
    loss_domain = models.BooleanField()

    blue_small_amount = models.BooleanField()
    blue_large_amount = models.BooleanField()

    def set_demographic_indicators(self):
        if self.gender == "female":
            self.female = True
        else:
            self.female = False

        if self.field_of_study:
            if any(word in self.field_of_study.lower() for word in Constants.economics_expressions):
                self.economist = True
            else:
                self.economist = False
        else:
            self.economist = False

    def set_ambiguity_aversion(self):
        if self.decision1 in Constants.bet_on_risky_box:
            self.ambiguity_averse_decision1 = True
        else: 
            self.ambiguity_averse_decision1 = False

        if self.decision2 in Constants.bet_on_risky_box:
            self.ambiguity_averse_decision2 = True
        else: 
            self.ambiguity_averse_decision2 = False

    def check_wci_violation(self):
        if self.ambiguity_averse_blue != self.ambiguity_averse_grey:
            self.wci_violated = True
        else:
            self.wci_violated = False

    def prepare_data_for_analysis(self):
        self.set_ambiguity_aversion()
        if self.treatment not in [5, 6]:
            self.set_order_invariant_vars()
            self.check_wci_violation()

        self.set_demographic_indicators()

    def set_order_invariant_vars(self):
        if self.decision_order == 1:
            self.decision_blue = self.decision1
            self.decision_grey = self.decision2

            self.ambiguity_averse_blue = self.ambiguity_averse_decision1
            self.ambiguity_averse_grey = self.ambiguity_averse_decision2

        else:
            self.decision_blue = self.decision2
            self.decision_grey = self.decision1

            self.ambiguity_averse_blue = self.ambiguity_averse_decision2
            self.ambiguity_averse_grey = self.ambiguity_averse_decision1
