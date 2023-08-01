class weight_checker:
    def __init__(self):
        super().__init__()
        self.node = None
        self.map = None
        self.level = None
        self.var_init()

    def var_init(self):

        self.node = {
            # 1 Floor room ###########################################################################

            # Escape Node
            'escape00': {'stair0': 10},
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
            'stair1': {'stair0': 2, 'hallway08': 1, 'stair2': 10},

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
            'stair2': {'stair1': 2, 'hallway28': 1, 'stair3': 10},

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
            'stair3': {'stair2': 2, 'hallway48': 1, 'stair4': 10},

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
            'stair4': {'stair3': 2, 'hallway68': 1, 'stair5': 10},

            # Stair
            'stair5': {'stair4': 2, 'escape01': 1},

            # Roof
            'escape01': {'stair5': 10},
        }
        self.map = {
            # 1 Floor ###########################################################################
            '1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': [],
            '7': [],
            '8': [],
            '9': [],
            '10': [],
            '11': [],

            # 2 Floor ###########################################################################
            '12': ['room10', 'hallway00'],    # 201
            '13': ['room10', 'hallway00'],
            '14': ['room10', 'hallway00'],
            '15': ['room10', 'hallway00'],
            '16': ['room10', 'hallway00'],
            '17': ['room10', 'hallway00'],
            '18': ['room11', 'hallway01'],    # 202
            '19': ['room11', 'hallway01'],
            '20': ['room11', 'hallway01'],
            '21': ['room11', 'hallway01'],
            '22': ['room11', 'hallway01'],
            '23': ['hallway02'],
            '24': ['hallway05'],
            '25': ['room12', 'hallway08'],    # 203
            '26': ['room12', 'hallway08'],
            '27': ['room12', 'hallway08'],
            '28': ['room12', 'hallway08'],
            '29': ['room12', 'hallway08'],
            '30': ['hallway07'],
            '31': ['stair1'],
            '32': ['room13', 'hallway10'],    # 204
            '33': ['room13', 'hallway10'],
            '34': ['room13', 'hallway10'],
            '35': ['room13', 'hallway10'],
            '36': ['room13', 'hallway10'],
            '37': ['room13', 'hallway10'],
            '38': ['room14', 'hallway12'],    # 205
            '39': ['room14', 'hallway12'],
            '40': ['room14', 'hallway12'],
            '41': ['room14', 'hallway12'],
            '42': ['room14', 'hallway12'],
            '43': ['room14', 'hallway12'],
            '44': ['hallway12'],
            '45': ['room15', 'hallway14'],    # 206
            '46': ['room15', 'hallway14'],
            '47': ['room15', 'hallway14'],
            '48': ['room15', 'hallway14'],
            '49': ['room15', 'hallway14'],
            '50': ['room15', 'hallway14'],
            '51': ['room16', 'hallway15'],    # 207
            '52': ['room16', 'hallway15'],
            '53': ['room16', 'hallway15'],
            '54': ['room16', 'hallway15'],
            '55': ['room16', 'hallway15'],
            '56': ['room16', 'hallway15'],
            '57': ['room16', 'hallway15'],

            # 3 Floor ###########################################################################
            '58': ['room20', 'hallway20'],    # 301
            '59': ['room20', 'hallway20'],
            '60': ['room20', 'hallway20'],
            '61': ['room20', 'hallway20'],
            '62': ['room20', 'hallway20'],
            '63': ['room20', 'hallway20'],
            '64': ['room20', 'hallway20'],
            '65': ['room21', 'hallway21'],    # 302
            '66': ['room21', 'hallway21'],
            '67': ['room21', 'hallway21'],
            '68': ['room21', 'hallway21'],
            '69': ['room21', 'hallway21'],
            '70': ['room21', 'hallway21'],
            '71': ['hallway22'],
            '72': ['hallway25'],
            '73': ['room22', 'hallway28'],    # 303
            '74': ['room22', 'hallway28'],
            '75': ['room22', 'hallway28'],
            '76': ['room22', 'hallway28'],
            '77': ['room22', 'hallway28'],
            '78': ['room22', 'hallway28'],
            '79': ['hallway27'],
            '80': ['stair2'],
            '81': ['room23', 'hallway30'],    # 304
            '82': ['room23', 'hallway30'],
            '83': ['room23', 'hallway30'],
            '84': ['room23', 'hallway30'],
            '85': ['room23', 'hallway30'],
            '86': ['room23', 'hallway30'],
            '87': ['room24', 'hallway32'],    # 305
            '88': ['room24', 'hallway32'],
            '89': ['room24', 'hallway32'],
            '90': ['room24', 'hallway32'],
            '91': ['room24', 'hallway32'],
            '92': ['room24', 'hallway32'],
            '93': ['hallway32'],
            '94': ['room25', 'hallway34'],    # 306
            '95': ['room25', 'hallway34'],
            '96': ['room25', 'hallway34'],
            '97': ['room25', 'hallway34'],
            '98': ['room25', 'hallway34'],
            '99': ['room25', 'hallway34'],
            '100': ['room26', 'hallway35'],    # 307
            '101': ['room26', 'hallway35'],
            '102': ['room26', 'hallway35'],
            '103': ['room26', 'hallway35'],
            '104': ['room26', 'hallway35'],
            '105': ['room26', 'hallway35'],
            '106': ['room26', 'hallway35'],

            # 4 Floor ###########################################################################
            '107': ['room30', 'hallway40'],    # 401
            '108': ['room30', 'hallway40'],
            '109': ['room30', 'hallway40'],
            '110': ['room30', 'hallway40'],
            '111': ['room30', 'hallway40'],
            '112': ['room30', 'hallway40'],
            '113': ['room30', 'hallway40'],
            '114': ['room31', 'hallway41'],    # 402
            '115': ['room31', 'hallway41'],
            '116': ['room31', 'hallway41'],
            '117': ['room31', 'hallway41'],
            '118': ['room31', 'hallway41'],
            '119': ['room31', 'hallway41'],
            '120': ['hallway42'],
            '121': ['hallway45'],
            '122': ['room32', 'hallway48'],    # 403
            '123': ['room32', 'hallway48'],
            '124': ['room32', 'hallway48'],
            '125': ['room32', 'hallway48'],
            '126': ['room32', 'hallway48'],
            '127': ['room32', 'hallway48'],
            '128': ['hallway47'],
            '129': ['stair3'],
            '130': ['room33', 'hallway50'],    # 404
            '131': ['room33', 'hallway50'],
            '132': ['room33', 'hallway50'],
            '133': ['room33', 'hallway50'],
            '134': ['room33', 'hallway50'],
            '135': ['room33', 'hallway50'],
            '136': ['room34', 'hallway52'],    # 405
            '137': ['room34', 'hallway52'],
            '138': ['room34', 'hallway52'],
            '139': ['room34', 'hallway52'],
            '140': ['room34', 'hallway52'],
            '141': ['room34', 'hallway52'],
            '142': ['hallway52'],
            '143': ['room35', 'hallway54'],    # 406
            '144': ['room35', 'hallway54'],
            '145': ['room35', 'hallway54'],
            '146': ['room35', 'hallway54'],
            '147': ['room35', 'hallway54'],
            '148': ['room35', 'hallway54'],
            '149': ['room36', 'hallway55'],    # 407
            '150': ['room36', 'hallway55'],
            '151': ['room36', 'hallway55'],
            '152': ['room36', 'hallway55'],
            '153': ['room36', 'hallway55'],
            '154': ['room36', 'hallway55'],

            # 5 Floor ###########################################################################
            '155': ['room40', 'hallway60'],    # 501
            '156': ['room40', 'hallway60'],
            '157': ['room40', 'hallway60'],
            '158': ['room40', 'hallway60'],
            '159': ['room40', 'hallway60'],
            '160': ['room40', 'hallway60'],
            '161': ['room40', 'hallway60'],
            '162': ['room41', 'hallway61'],    # 502
            '163': ['room41', 'hallway61'],
            '164': ['room41', 'hallway61'],
            '165': ['room41', 'hallway61'],
            '166': ['room41', 'hallway61'],
            '167': ['room41', 'hallway61'],
            '168': ['hallway62'],
            '169': ['hallway65'],
            '170': ['room42', 'hallway68'],    # 503
            '171': ['room42', 'hallway68'],
            '172': ['room42', 'hallway68'],
            '173': ['room42', 'hallway68'],
            '174': ['room42', 'hallway68'],
            '175': ['room42', 'hallway68'],
            '176': ['hallway67'],
            '177': ['stair4'],
            '178': [],
            '179': ['room43', 'hallway70'],    # 504
            '180': ['room43', 'hallway70'],
            '181': ['room43', 'hallway70'],
            '182': ['room43', 'hallway70'],
            '183': ['room43', 'hallway70'],
            '184': ['room43', 'hallway70'],
            '185': ['room44', 'hallway72'],    # 505
            '186': ['room44', 'hallway72'],
            '187': ['room44', 'hallway72'],
            '188': ['room44', 'hallway72'],
            '189': ['room44', 'hallway72'],
            '190': ['room44', 'hallway72'],
            '191': ['hallway72'],
            '192': ['room45', 'hallway74'],    # 506
            '193': ['room45', 'hallway74'],
            '194': ['room45', 'hallway74'],
            '195': ['room45', 'hallway74'],
            '196': ['room45', 'hallway74'],
            '197': ['room45', 'hallway74'],
            '198': ['room46', 'hallway75'],    # 507
            '199': ['room46', 'hallway75'],
            '200': ['room46', 'hallway75'],
            '201': ['room46', 'hallway75'],
            '202': ['room46', 'hallway75'],
            '203': ['room46', 'hallway75'],
            '204': ['stair5'],
        }
        self.level = [[],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]

    def set_node_weight(self, danger_temp_idx, danger_gas_idx, temp_idx, gas_idx, floor_idx_list):

        danger_node = [[], [], [], [], []]
        for node in danger_temp_idx:
            for floor, floor_nodes in enumerate(floor_idx_list):
                if temp_idx[node] in floor_nodes:
                    danger_node[floor].append(temp_idx[node])

        for node in danger_gas_idx:
            for floor, floor_nodes in enumerate(floor_idx_list):
                if gas_idx[node] in floor_nodes:
                    danger_node[floor].append(gas_idx[node])

        for nodes in danger_node:
            for node in nodes:
                if str(node) in self.map.keys():
                    for sensor_node in self.map[str(node)]:
                        for near_node in self.node[sensor_node]:
                            self.node[near_node][sensor_node] = 100
