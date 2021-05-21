from ._builtin import Page

import pycountry


class Introduction(Page):
    form_model = 'player'
    form_fields = ['captcha']


class Instructions1(Page):
    pass


class Instructions2(Page):
    pass


class DecisionAnnouncement(Page):
    def vars_for_template(self):
        return {
            'separator': self.session.config.get('separator_page', False)
        }

class Decision1(Page):
    form_model = 'player'
    form_fields = ['decision1']


class DecisionAnnouncement2(Page):
    def is_displayed(self):
        return self.session.config.get('separator_page', False)

class Decision2(Page):
    form_model = 'player'
    form_fields = ['decision2']


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'nationality', 'education', 'field_of_study', 'occupation']

    def vars_for_template(self):
        return {
            'country_list': sorted(list(pycountry.countries), key=lambda x: x.name),
        }

    def error_message(self, input_values):
        if input_values['education'] >= 3 and not input_values['field_of_study']:
            return "Please provide your field of study."

    def before_next_page(self):
        self.player.prepare_data_for_analysis()


class Ending(Page):
    pass


page_sequence = [
    Introduction,
    Instructions1,
    Instructions2,
    DecisionAnnouncement,
    Decision1,
    DecisionAnnouncement2,
    Decision2,
    Questionnaire,
    Ending
]