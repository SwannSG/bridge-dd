"""
    Bridge Board Representation (bbr.py)
"""

import re

class Board:
    """
        Board object represents a board of bridge
            players, vulnerability, bidding, play
    """
    def __init__(self):
        self.player_south = ''
        self.player_west = ''
        self.player_north = ''
        self.player_east = ''
        self.board_name = ''
        self.vulnerablity = 'NULL'
        self.dealer = ''
        self.hand_1 = []
        self.hand_2 = []
        self.hand_3 = []
        self.bidding = []
        self.declarer = ''  # S,W,N,E
        self.contract = ''
        self.penalty = ''

    def methodA(self, bidding):
        self.bidding = bidding
        l4b = self._get_last_4_bids()
        self.penalty = self._get_penalty(l4b)
        self.contract = self._get_contract(l4b)
        self.declarer = self._get_declarer()

    def _get_declarer(self):
        l = ['S','W','N','E','S','W','N','E']
        index = l.index(self.dealer[0].upper())
        index = self._get_contract_bid_position() + index
        return l[index]

    def _get_contract_bid_position(self):
        # what about if passed out and no contract ?
        for bid_round in self.bidding.bid_rounds:
            print (bid_round.bid_1._suit())
            if bid_round.bid_1._suit()==self.contract[1]:
                return 0
            if bid_round.bid_2._suit()==self.contract[1]:
                return 1
            if bid_round.bid_3._suit()==self.contract[1]:
                return 2
            if bid_round.bid_4._suit()==self.contract[1]:
                return 3
    
    def _get_penalty(self, l4b):
        i = 0
        while i <= 3:
            if i == 3:
                return 'None'
            if l4b[3-i].bid != 'p':
                return l4b[3-i].bid
            i = i + 1

    def _get_contract(self, l4b):
        return l4b[0].bid

            
    def _get_last_4_bids(self):
        result = []
        if self.bidding.bid_rounds[-1].bid_4.bid:
            result.append(self.bidding.bid_rounds[-1].bid_4)
        if self.bidding.bid_rounds[-1].bid_3.bid:
            result.append(self.bidding.bid_rounds[-1].bid_3)
        if self.bidding.bid_rounds[-1].bid_2.bid:
            result.append(self.bidding.bid_rounds[-1].bid_2)
        if self.bidding.bid_rounds[-1].bid_1.bid:
            result.append(self.bidding.bid_rounds[-1].bid_1)
        if len(result) == 4:
            result.reverse()
            return result
        if self.bidding.bid_rounds[-2].bid_4.bid:
            result.append(self.bidding.bid_rounds[-2].bid_4)
            if len(result) == 4:
                result.reverse()
                return result
        if self.bidding.bid_rounds[-2].bid_3.bid:
            result.append(self.bidding.bid_rounds[-2].bid_3)
            if len(result) == 4:
                result.reverse()
                return result
        if self.bidding.bid_rounds[-2].bid_2.bid:
            result.append(self.bidding.bid_rounds[-2].bid_2)
            if len(result) == 4:
                result.reverse()
                return result

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
    def dealer(self):
        return self.__dealer

    @dealer.setter
    def dealer(self, value):
        lookup = {
            '1': 'South',
            '2':'West', 
            '3':'North',
            '4':'East'
        }
        if value in lookup:
            self.__dealer = lookup[value]    

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
        if len(self.bids) % 4 !=0:
            # incomplete bid round
            lb_index = (bid_round_counter-1)*4
            ub_index = lb_index + 4
            i = 0
            while i <= len(self.bids) % 4:
                self.bids.append(None)
                self.alerts.append(None)
                self.comments.append(None)
                i = i + 1
            print (self.bids)
            bid_rounds.append(BidRound(bid_round_counter,
                                       self.bids[lb_index:ub_index],
                                       self.alerts[lb_index:ub_index],
                                       self.comments[lb_index:ub_index]))
            
        return bid_rounds

    
class BidRound:
    """
        A BidRound object represents 1 round of bidding i.e. 4 bids
            Contains 4 Bid objects
    """
    def __init__(self, bid_round_counter, bids, alerts, comments, complete=True):
        if complete:
            self.bid_round_counter = bid_round_counter
            self.bid_1 = Bid(bids[0], alerts[0], comments[0])
            self.bid_2 = Bid(bids[1], alerts[1], comments[1])
            self.bid_3 = Bid(bids[2], alerts[2], comments[2])
            self.bid_4 = Bid(bids[3], alerts[3], comments[3])
        else:
            # incomplete bid round
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

    def _suit(self):
        if len(self.bid)==1:
            return self.bid
        return self.bid[1]

    def __repr__(self):
        return str(self.bid)

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

    def update(self):
        """
            pg label encountered
            update state
       """
        if self.pg_counter==0:
           self.pg_first_ever = True
           self.pg_state = 'start'
        else:
            self.pg_first_ever = False 
            self.pg_state = self._toggle_pg_state() 
        self.pg_counter = self.pg_counter + 1

    def _toggle_pg_state(self):
        if self.pg_state == 'start':
            return 'end'
        return 'start'
