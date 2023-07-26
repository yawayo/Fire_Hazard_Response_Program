class weight_checker:
    def __init__(self):
        super().__init__()
        self.node = None
        self.var_init()

    def var_init(self):

        self.node = {
            # 1 Floor room ###########################################################################

            # Escape Node
            'escape00': {},
            'stair0': {'escape00': 2, 'stair1': 10},

            # 2 Floor room ###########################################################################

            # room
            'room10': {'hallway00': 1},
            'room11': {'hallway01': 1},
            'room12': {'hallway08': 1},
            'room13': {'hallway10': 1},
            'room14': {'hallway12': 1},
            'room15': {'hallway14': 1},
            'room16': {'hallway15': 1},

            # hallway
            'hallway00': {'room10': 1,                 'hallway01': 1},
            'hallway01': {'room11': 1, 'hallway00': 1, 'hallway02': 1},
            'hallway02': {             'hallway01': 1, 'hallway03': 1},
            'hallway03': {             'hallway02': 1, 'hallway04': 1},
            'hallway04': {             'hallway03': 1, 'hallway05': 1},
            'hallway05': {             'hallway04': 1, 'hallway06': 1},
            'hallway06': {             'hallway05': 1, 'hallway07': 1},
            'hallway07': {             'hallway06': 1, 'hallway08': 1},
            'hallway08': {'room12': 1, 'hallway07': 1, 'hallway09': 1, 'stair1': 1},
            'hallway09': {             'hallway08': 1, 'hallway10': 1},
            'hallway10': {'room13': 1, 'hallway09': 1, 'hallway11': 1},
            'hallway11': {             'hallway10': 1, 'hallway12': 1},
            'hallway12': {'room14': 1, 'hallway11': 1, 'hallway13': 1},
            'hallway13': {             'hallway12': 1, 'hallway14': 1},
            'hallway14': {'room15': 1, 'hallway13': 1, 'hallway15': 1},
            'hallway15': {'room16': 1, 'hallway14': 1},

            # Stair
            'stair1': {'stair0': 2, 'hallway07': 1, 'stair2': 10},

            # 3 Floor room ###########################################################################

            # room
            'room20': {'hallway20': 1},
            'room21': {'hallway21': 1},
            'room22': {'hallway28': 1},
            'room23': {'hallway30': 1},
            'room24': {'hallway32': 1},
            'room25': {'hallway34': 1},
            'room26': {'hallway35': 1},

            # hallway
            'hallway20': {'room20': 1,                 'hallway21': 1},
            'hallway21': {'room21': 1, 'hallway20': 1, 'hallway22': 1},
            'hallway22': {             'hallway21': 1, 'hallway23': 1},
            'hallway23': {             'hallway22': 1, 'hallway24': 1},
            'hallway24': {             'hallway23': 1, 'hallway25': 1},
            'hallway25': {             'hallway24': 1, 'hallway26': 1},
            'hallway26': {             'hallway25': 1, 'hallway27': 1},
            'hallway27': {             'hallway26': 1, 'hallway28': 1},
            'hallway28': {'room22': 1, 'hallway27': 1, 'hallway29': 1, 'stair2': 1},
            'hallway29': {             'hallway28': 1, 'hallway30': 1},
            'hallway30': {'room23': 1, 'hallway29': 1, 'hallway31': 1},
            'hallway31': {             'hallway30': 1, 'hallway32': 1},
            'hallway32': {'room24': 1, 'hallway31': 1, 'hallway33': 1},
            'hallway33': {             'hallway32': 1, 'hallway34': 1},
            'hallway34': {'room25': 1, 'hallway33': 1, 'hallway35': 1},
            'hallway35': {'room26': 1, 'hallway34': 1},

            # Stair
            'stair2': {'stair1': 2, 'hallway27': 1, 'stair3': 10},

            # 4 Floor room ###########################################################################

            # room
            'room30': {'hallway40': 1},
            'room31': {'hallway41': 1},
            'room32': {'hallway48': 1},
            'room33': {'hallway50': 1},
            'room34': {'hallway52': 1},
            'room35': {'hallway54': 1},
            'room36': {'hallway55': 1},

            # hallway
            'hallway40': {'room30': 1,                 'hallway41': 1},
            'hallway41': {'room31': 1, 'hallway40': 1, 'hallway42': 1},
            'hallway42': {             'hallway41': 1, 'hallway43': 1},
            'hallway43': {             'hallway42': 1, 'hallway44': 1},
            'hallway44': {             'hallway43': 1, 'hallway45': 1},
            'hallway45': {             'hallway44': 1, 'hallway46': 1},
            'hallway46': {             'hallway45': 1, 'hallway47': 1},
            'hallway47': {             'hallway46': 1, 'hallway48': 1},
            'hallway48': {'room32': 1, 'hallway47': 1, 'hallway49': 1, 'stair3': 1},
            'hallway49': {             'hallway48': 1, 'hallway50': 1},
            'hallway50': {'room33': 1, 'hallway49': 1, 'hallway51': 1},
            'hallway51': {             'hallway50': 1, 'hallway52': 1},
            'hallway52': {'room34': 1, 'hallway51': 1, 'hallway53': 1},
            'hallway53': {             'hallway52': 1, 'hallway54': 1},
            'hallway54': {'room35': 1, 'hallway53': 1, 'hallway55': 1},
            'hallway55': {'room16': 1, 'hallway54': 1},

            # Stair
            'stair3': {'stair2': 2, 'hallway47': 1, 'stair4': 10},

            # 5 Floor room ###########################################################################

            # room
            'room40': {'hallway60': 1},
            'room41': {'hallway61': 1},
            'room42': {'hallway68': 1},
            'room43': {'hallway70': 1},
            'room44': {'hallway72': 1},
            'room45': {'hallway74': 1},
            'room46': {'hallway75': 1},

            # hallway
            'hallway60': {'room40': 1,                 'hallway61': 1},
            'hallway61': {'room41': 1, 'hallway60': 1, 'hallway62': 1},
            'hallway62': {             'hallway61': 1, 'hallway63': 1},
            'hallway63': {             'hallway62': 1, 'hallway64': 1},
            'hallway64': {             'hallway63': 1, 'hallway65': 1},
            'hallway65': {             'hallway64': 1, 'hallway66': 1},
            'hallway66': {             'hallway65': 1, 'hallway67': 1},
            'hallway67': {             'hallway66': 1, 'hallway68': 1},
            'hallway68': {'room42': 1, 'hallway67': 1, 'hallway69': 1, 'stair4': 1},
            'hallway69': {             'hallway68': 1, 'hallway70': 1},
            'hallway70': {'room43': 1, 'hallway69': 1, 'hallway71': 1},
            'hallway71': {             'hallway70': 1, 'hallway72': 1},
            'hallway72': {'room44': 1, 'hallway71': 1, 'hallway73': 1},
            'hallway73': {             'hallway72': 1, 'hallway74': 1},
            'hallway74': {'room45': 1, 'hallway73': 1, 'hallway75': 1},
            'hallway75': {'room46': 1, 'hallway74': 1},

            # Stair
            'stair4': {'stair3': 2, 'hallway67': 1, 'stair5': 10},

            # Stair
            'stair5': {'stair4': 2, 'escape01': 1},

            # Roof
            'escape01': {},
        }