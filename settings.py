from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='wci_standard',
    #     display_name='WCI - blue large - random gain/loss',
    #     app_sequence=['wci'],
    #     num_demo_participants=4,
    # ),
    dict(
        name='wci_gain',
        display_name='WCI - blue large - gain',
        app_sequence=['wci'],
        num_demo_participants=4,
        treatment=1
    ),
    dict(
        name='wci_loss',
        display_name='WCI - blue large - loss',
        app_sequence=['wci'],
        num_demo_participants=4,
        treatment=2
    ),
    dict(
        name='wci_gain_twice',
        display_name='WCI - blue large - gain - same twice',
        app_sequence=['wci'],
        num_demo_participants=4,
        treatment=5
    ),
    dict(
        name='wci_loss_twice',
        display_name='WCI - blue large - loss - same twice',
        app_sequence=['wci'],
        num_demo_participants=4,
        treatment=6
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.75,
    doc="",
    mturk_hit_settings=dict(
        keywords='bonus, study, choices, research, risk',
        title='Short Decision-Making Study (5 min)',
        description='Take two decisions and earn a fixed payment of $0.75 in 5 minutes.',
        frame_height=700,
        template='wci/mturk_template.html',
        minutes_allotted_per_assignment=20,
        expiration_hours=3,
        qualification_requirements=[
            {
                'QualificationTypeId': '00000000000000000071',
                'Comparator': 'EqualTo',
                'LocaleValues': [{'Country': "US"}]
            },
            {
                'QualificationTypeId': '3PUFTE5I6TEJB17LHBU2381230XW29',
                'Comparator': 'DoesNotExist'
            },
        ],
        grant_qualification_id='3PUFTE5I6TEJB17LHBU2381230XW29',
    )
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '6778469215079'
