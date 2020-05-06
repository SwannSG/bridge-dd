import re
import pprint

END_OF_LINE_CHAR = '\n'

# B1
file = '/home/steve/development/doubleDummy/data/3399426367.lin'
# B4
file = '/home/steve/development/doubleDummy/data/3399426420.lin'


labels = {
    'ah':   'Board Name',
    'an':   'Alert',
    'pc':   'Played Card',
    'pg':   "Don't know",
    'pn':   'Players Names',    # value S, W, N, E
    'mb':   'Bid',
    'md':   'Hands',
    'rh':   "Don't know",
    'st':   "Don't know",
    'sv':   'Vulnerability',
}

def parseHand(value):
    # values has form 'S4TJQH246JKD6C459','SKAH7QD3459TAC28T',
    # 'S359HTAD78JKC67QK'
    hand = {
        's': [],
        'h': [],
        'd': [],
        'c': []
    }
    for char in value:    
        if char=='S':
            suit = 's'
        elif char=='H':
            suit = 'h'
        elif char=='D':
            suit = 'd'
        elif char=='C':
            suit = 'c'
        else:
            hand[suit].append(char)            
    return hand

def parseHands(value):
    # this is the value for label 'md'
    handUnknown = value[0]
    value = value[1:-1]
    print (handUnknown)
    print (value)

def longLabel(seq):
    l = []
    for each in seq:
        l.append( (labels[each[0]], each[1]) )
    return l

class Board:

    def __init__(self):
        self.player_south = ''
        self.player_west = ''
        self.player_north = ''
        self.player_east = ''
        self.board_name = ''
        self.vulnerablity = 'NULL'
        self.opening_bidder = ''
        self.hand_1 = []
        self.hand_2 = []
        self.hand_3 = []
        self.bidding = []

    def set_players_from_LIN(self, value):
        value = value.split(',')
        self.player_south = value[0]
        self.player_west = value[1]
        self.player_north = value[2]
        self.player_east = value[3]

    @property
    def vulnerablity(self):
        return self.__vulnerablity

    @vulnerablity.setter
    def vulnerablity(self, value):
        print (value)
        if value=='o':
            self.__vulnerablity = 'None'
        elif value=='b':
            self.__vulnerablity = 'Both'
        elif value=='e':
            self.__vulnerablity = 'EW'
        elif value=='n':
            self.__vulnerablity = 'NS'

    @property
    def opening_bidder(self):
        return self.__opening_bidder

    @opening_bidder.setter
    def opening_bidder(self, value):
        lookup = {
            '1': 'South',
            '2':'West', 
            '3':'North',
            '4':'East'
        }
        if value in lookup:
            self.__opening_bidder = lookup[value]    

    def hands_from_LIN(self, value):
        value = value[1:-1]
        h1, h2, h3 = value.split(',')
        self.hand_1 = Hand(h1)
        self.hand_2 = Hand(h2)
        self.hand_3 = Hand(h3)
        # 4th hand has to be generated
        # Pack - (hand1 + hand2 + hand3)
        self.hand_4 = Hand([])
        self.hand_4.get_4th_hand_LIN(self.hand_1, self.hand_2, self.hand_3)

class Hand:

    regex = regex = r"^S([AKQJT98765432]*)H([AKQJT98765432]*)D([AKQJT98765432]*)C([AKQJT98765432]*)"
    pattern = re.compile(regex)

    suitSet = set([2,3,4,5,6,7,8,9,10,11,12,13,14])

    cardToInt = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }

    intToCard = {1: '2',
                 2: '3',
                 3: '4',
                 4: '5',
                 5: '6',
                 6: '7',
                 7: '8',
                 8: '9',
                 9: 'T',
                 10: 'J',
                 11: 'Q',
                 12: 'K',
                 13: 'A'
    }

    def __init__(self, value):
        self.spades = []
        self.hearts = []
        self.diamonds = []
        self.clubs = []
        # 4th hand LIN test
        if len(value)!=0:
            self.get_hand_from_LIN_string(value)        

    def get_hand_from_LIN_string(self, value):
        # value 'S4TJQH246JKD6C459'
        s, h, d, c = Hand.pattern.search(value).groups()
        self.spades = self._mapSuitToInt(s)
        self.hearts = self._mapSuitToInt(h)
        self.diamonds = self._mapSuitToInt(d)
        self.clubs = self._mapSuitToInt(c)

    def _mapSuitToInt(self, value):
        # value '4TJQ'
        intSuit = []
        for char in value:
            intSuit.append(Hand.cardToInt[char])    
        return intSuit

    def get_4th_hand_LIN(self, hand1, hand2, hand3):
        self.spades = sorted(list(Hand.suitSet.difference(set(hand1.spades + hand2.spades + hand3.spades))))
        self.hearts = sorted(list(Hand.suitSet.difference(set(hand1.hearts + hand2.hearts + hand3.hearts))))
        self.diamonds = sorted(list(Hand.suitSet.difference(set(hand1.diamonds + hand2.diamonds + hand3.diamonds))))
        self.clubs = sorted(list(Hand.suitSet.difference(set(hand1.clubs + hand2.clubs + hand3.clubs))))

    def __repr__(self):
        return '%s %s %s %s' % (self.dsp_spades(), self.dsp_hearts(), self.dsp_diamonds(), self.dsp_clubs() )

    def dsp_spades(self):
        r = ''
        for each in self.spades:
            r = r + Hand.intToCard[each]
        return r

    def dsp_hearts(self):
        r = ''
        for each in self.hearts:
            r = r + Hand.intToCard[each]
        return r

    def dsp_diamonds(self):
        r = ''
        for each in self.diamonds:
            r = r + Hand.intToCard[each]
        return r

    def dsp_clubs(self):
        r = ''
        for each in self.clubs:
            r = r + Hand.intToCard[each]
        return r


class BidRecorder:
    """
        keeps a record of the sequence of:
            all bid strings e.g 1D
            all alerts
            all comments

        bid_round_chunks() creates the necessary BidRound objects
        and returns a list of BidRound objects
    """

    
    def __init__(self):
        self.bid_count = 0
        self.bids = []
        self.alerts = []
        self.comments = []
        
    def add_bid(self, bid:str):
        """
            bid eg. 1H, 1N
        """
        self.bids.append(bid)
        self.alerts.append(''),
        self.comments.append(''),
        self.bid_count = self.bid_count + 1 

    def add_alert(self, alert:str):
        """
            alert eg. 5+ D
        """
        self.alerts[self.bid_count - 1] = alert

    def add_comment(self, comment:str):
        """
            comment eg. free format text
        """
        self.comments[self.bid_count - 1] = comment

    def bid_round_chunks(self) -> list:
        """
            returns [BidRound obj, BidRound obj, ...]
        """
        bid_round_total = self.bid_count/4
        bid_round_counter = 1
        bid_rounds = []
        while bid_round_counter <= bid_round_total:
            lb_index = (bid_round_counter-1)*4
            ub_index = lb_index + 4
            bid_rounds.append(BidRound(bid_round_counter,
                                       self.bids[lb_index:ub_index],
                                       self.alerts[lb_index:ub_index],
                                       self.comments[lb_index:ub_index]))
            bid_round_counter = bid_round_counter + 1
        return bid_rounds

    
class BidRound:
    """
        A BidRound object represents 1 round of bidding i.e. 4 bids
            Contains 4 Bid objects
    """
    def __init__(self, bid_round_counter, bids, alerts, comments):
        self.bid_round_counter = bid_round_counter
        self.bid_1 = Bid(bids[0], alerts[0], comments[0])
        self.bid_2 = Bid(bids[1], alerts[1], comments[1])
        self.bid_3 = Bid(bids[2], alerts[2], comments[2])
        self.bid_4 = Bid(bids[3], alerts[3], comments[3])

    def __repr__(self):
        return '%s: %s | %s | %s | %s' % (self.bid_round_counter,
                                          self.bid_1.bid,
                                          self.bid_2.bid,
                                          self.bid_3.bid,
                                          self.bid_4.bid)

class Bid:
    """
        A Bid object represents a single bid eg. 1D
    """
    def __init__(self, bid, alert, comment):
        self.bid = bid
        self.bid_alert = alert
        self.bid_comment = comment

    def __repr__(self):
        return self.bid

class Bidding:
    """
        A Bidding object represents the sequence of all bids
            Contains BidRound objects
    """

    def __init__(self, bid_rounds: '[BidRound obj, BidRound obj, ...]'):
        self.bid_rounds = bid_rounds

    def __repr__(self):
        result = ''
        for each in self.bid_rounds:
            result = result + str(each) + '\n'
        return result

class PgState:
    """
        'pg' label state
    """

    def __init__(self):
        self.pg_counter = 0
        self.pg_first_ever = False
        self.pg_state = ''

    def update():
        """
            pg label encountered
            update state
       """
        if self.pg_counter==0:
           self.pg_first_ever = True
           self.pg_state = 'start'
        else:
            self.first_ever_pg = False 
            self.pg_state = _toggle_pg_state() 
        self.pg_counter = self.pg_counter

    def _togggle_pg_state(self):
        if self.pg_state == 'start':
            return 'end'
        return 'start'


fp = open(file, 'r')
for lin in fp:
    pass
# 'lin' contains the entire LIN string representation
l = lin.split('|')
if l[-1]==END_OF_LINE_CHAR:
    # remove it
    l = l[:len(l)-1]
# create (label,value) tuples in an ordered seqence (list)
i = 0
seq = []
while i < len(l):
    seq.append( (l[i], l[i+1]))
    i = i+ 2
#pprint.pprint(longLabel(seq))

# create Board object from BBO LIN
board = Board()
bid_rec = BidRecorder()
play_rec = PlayRecorder()
pg = PgState()
for (label, value) in seq:
    if label=='pn':
        board.set_players_from_LIN(value)
    if label=='ah':
        board.board_name = value
    if label=='sv':
        board.vulnerablity = value
    if label=='md':
        board.opening_bidder = value[0]
        board.hands_from_LIN(value)
    if label=='mb':
        bid_rec.add_bid(value)
    if label=='an':
        bid_rec.add_alert(value)
    if label=='pg':
        pg.update()
        if pg.pg_first_ever:
            # get contract
            pass
    
    if label=='pc':
        # card played

board.bidding = Bidding(bid_rec.bid_round_chunks())    
