import utility

class Board:
    """
        Board object represents a board of bridge
    """
    # O=None, B=Both, N=NorthSouth, E=EastWest
    vulnerable_values = ['O', 'B', 'N', 'E']
    dealer_values = ['N', 'S', 'W', 'E']
    
    def __init__(self):
        self.player_south = ''
        self.player_west = ''
        self.player_north = ''
        self.player_east = ''
        self.board_name = ''
        self.vulnerable = 'B'
        self.dealer = 'W'
        self.deal_hand_1 = Hand()
        self.deal_hand_2 = Hand()
        self.deal_hand_3 = Hand()
        self.deal_hand_4 = Hand()
        self.bidding = Bidding()
        self.declarer = ''  
        self.contract = ''
        self.penalty = ''

    @property
    def vulnerable(self):
        return self.__vulnerable

    @vulnerable.setter
    def vulnerable(self,value):
        if value in Board.vulnerable_values:
            self.__vulnerable = value
        else:
            raise ValueError('invalid vulnerable value: %s' % value)

    @property
    def dealer(self):
        return self.__dealer

    @dealer.setter
    def dealer(self,value):
        if value in Board.dealer_values:
            self.__dealer = value
        else:
            raise ValueError('invalid dealer value: %s' % value)
        
    def calc_deal_hand_4(self):
        """
            cardpack - h1 - h2 - h3
            special method used by LIN files
        """
        h1 = self.deal_hand_1.as_int()
        h2 = self.deal_hand_2.as_int()
        h3 = self.deal_hand_3.as_int()
        h4 = list(set(utility.Constants.all_cards).difference(set(h1+h2+h3)))
        self.deal_hand_4.bulk_append_int(h4)
        self.deal_hand_4.arrange_LIN_cards()

class Hand(list):
    """
        Hand is a container of Card objects
    """
    def __init__(self):
        pass

    def append(self, value):
        if (isinstance(value, Card)):
            super().append(value)
        else:
            raise TypeError('object must be type Card')

    def bulk_append(self, facevalues:str, suit:str):
        """
            bulk_append('s', 'AT9543')
        """
        suit = suit.upper()
        facevalues = facevalues.upper()
        for facevalue in facevalues:
            self.append(Card(facevalue, suit))

    def bulk_append_int(self, cards:list):
        """
            bulk_append_int([10, 15, 25])
                integers as card representation
        """
        for each in cards:
            self.append(Card(each))

    def bulk_append_card(self, cards:list):
        """
            cards = [Card(), Card()]
        """
        for each in cards:
            self.append(each)


    def as_int(self):
        """
            Hand as card ints
        """
        r = []
        for card in self:
            r.append(card.as_int())
        return r

    def find(self, value):
        """
            find a card in the Hand
            value: '6c' or int
            returns: index or -1
        """
        if isinstance(value, str):
            value = value.upper()
            value =  utility.Constants.cardStrToInt[value]
        elif isinstance(value, int):   
            pass
        else:
            raise TypeError('value must be int 2 char string')
        try:
            return self.index(value)
        except:
            return -1

    def suit_split(self) -> tuple:
        """
            (spades, hearts, diamonds, clubs)
        """
        d = {'S':[], 'H':[], 'D':[], 'C':[]}
        for each in self:
            suit = each.suit()
            d[suit].append(each)
        return (d['S'],d['H'],d['D'],d['C'])

    def arrange_LIN_cards(self):
        """
            arranges cards in LIN order
        """
        s,h,d,c = self.suit_split()
        s.sort()
        h.sort()
        d.sort()
        c.sort()
        self.clear()
        self.bulk_append_card(s + h + d + c)

class Card:
    """
        Card object
    """
    def __init__(self, value, suit=''):
        suit = suit.upper()
        if isinstance(value, str):
            value = value.upper()
            if len(value)==2:
                # e.g. 2S
                self._validate_face_value(value[0])
                self._validate_suit(value[1])
                self._card = utility.Constants.cardStrToInt[value]
            elif len(value)==1:
                self._validate_face_value(value)
                self._validate_suit(suit)
                self._card = utility.Constants.cardStrToInt[value + suit ]
        elif isinstance(value, int):
            if suit:
                self._validate_face_value(str(value))
                self._validate_suit(suit)
                self._card = utility.Constants.cardStrToInt[str(value) + suit ]
            else:
                if self.__validate_card_as_int(value):
                    self._card = value 
        else:
            raise TypeError('value must be int or 1 or 2char e.g. 2s, 2')

    def _validate_face_value(self, value):
        if value in utility.Constants.facevalues:
            return True
        else:
            raise ValueError('invalid card facevalue: %s' % value)

    def _validate_suit(self, value):
        if value in utility.Constants.suits:
            return True
        else:
            raise ValueError('invalid card suit: %s' % value)

    def __validate_card_as_int(self, value):
        if value in utility.Constants.all_cards:
            return True
        else:
            raise ValueError('invalid card integer: %s' % value)

    def __str__(self):
        return '%s%s' % (self.facevalue(), self.suit())

    def __repr__(self):
        return '%s%s' % (self.facevalue(), self.suit())

    def suit(self):
        # return card as suit eg.'S'
        return utility.Constants.cardIntToSuit[self._card]


    def facevalue(self):
        # return card facevalue as string eg.'A'
        return utility.Constants.cardIntToStr[self._card][0]

    def as_int(self):
        # returns cards as int
        return self._card

    def __eq__(self, other):
        if self.as_int()==other.as_int():
            return True
        return False

    def __lt__(self, other):
        if self.as_int() < other.as_int():
            return True
        return False

class Bidding(list):
    """
        Bidding is a container of Bid objects 
    """

    
    def __init__(self):

        # must be read only properties from outside
        self.contract = ''
        self.penalty = ''
        self.declarer_position = -1
        # end must be read only properties from outside

        self._no_suit_bid_count = 0
        self._last_suit_bid = ''
        self._last_penalty = ''
        self._debug_bid_value = ''

    def debug_state(self):
        # temp method for debug
        print ('value bid: %s' % self._debug_bid_value)
        print ('contract:%s, penalty:%s, declarer_position:%s' % (self.contract, self.penalty, self.declarer_position))
        print ('_no_suit_bid_count:%s, _last_suit_bid:%s, _last_penalty:%s' % (self._no_suit_bid_count, self._last_suit_bid, self._last_penalty)  )        
        print ()
        
    def append(self, value):
        if self.contract:
            raise ValueError('Bidding is closed')
        if (isinstance(value, Bid)):
            self._is_bid_valid(value)
        else:
            raise TypeError('object must be type Bid: %s' % value)

    def _is_bid_valid(self, value) -> bool:
        self._debug_bid_value = value.bid
        if self._is_suit_bid(value.bid):
            # suit bid e.g '1c', '1n'
            self._last_suit_bid = value.bid
            self._no_suit_bid_count = 0
            super().append(value)
        elif value.bid==utility.Constants.double:
            # dbl
            if not self._last_penalty:
                self._last_penalty = utility.Constants.double
                self._no_suit_bid_count = self._no_suit_bid_count + 1
                super().append(value)
                self._end_of_bidding()
            else:
                raise ValueError('bid, cannot double when previous penalty is: %s' % self._last_penalty)
        elif value.bid==utility.Constants.redouble:
            # rdbl
            if self._last_penalty==utility.Constants.double:
                self._last_penalty = utility.Constants.redouble
                self._no_suit_bid_count = self._no_suit_bid_count + 1
                super().append(value)
                self._end_of_bidding()
            else:
                raise ValueError('bid, cannot redouble when previous penalty is: %s' % self._last_penalty)
        elif value.bid==utility.Constants.pass_:
            # pass
            if self._last_suit_bid:
                # suit has been bid
                if self._no_suit_bid_count < 3:
                    self._no_suit_bid_count = self._no_suit_bid_count + 1
                    super().append(value)
                    self._end_of_bidding()
            else:
                # no suit has been bid, p-p-p-p edge case
                if self._no_suit_bid_count < 4:
                    self._no_suit_bid_count = self._no_suit_bid_count + 1
                    super().append(value)
                    if self._no_suit_bid_count==4:
                        # Bidding is at an end
                        self.contract = 'none'
        else:
            raise ValueError('unkown bid: %s' % value.bid)

    def _end_of_bidding(self):
        """
            checks if bidding is at an end
            and updates necessary
        """
        if self._no_suit_bid_count==3:
            # Bidding is at an end
            self.contract = self._last_suit_bid
            self.penalty = self._last_penalty
            # Update declarer position
            self.declarer_position = len(self)%4 

    def _is_suit_bid(self, value) -> bool:
        """
            for any bids not pass, dbl, rdb
        """
        if value in utility.Constants.is_not_suit_bid:
            return False
        else:
            return True

class Bid:
    """
        Bid object
    """
    def __init__(self, bid, alert='', comment=''):
        self.bid = bid.upper()
        self.alert = alert
        self.comment = comment

    def rank(self) -> int:
        """
            2c has rank 1, 3c has rank 2
        """
        return utility.Constants.bid_rank[self.bid]

    def __repr__(self):
        return '%s %s %s' % (self.bid, self.alert, self.comment)

    def __str__(self):
        return '%s' % self.bid


if __name__  == '__main__':
    # show usage & simple tests
    c1 = Card('2c')
    c2 = Card(3, 'c')
    c3 = Card('J', 'c')
    c4 = Card(28)
    hand = Hand()
    hand.append(c1)
    hand.append(c2)
    hand.append(c3)
    hand.append(c4)
    print (hand)

    h = Hand()
    h.bulk_append('KJ642', 'c')
    print (hand)





    #Bid seq1
    b1 = Bid('1c')
    b2 = Bid('p')
    b3 = Bid('1s')
    b4 = Bid('p')
    b5 = Bid('d')
    b6 = Bid('r')
    bidding = Bidding()
    bidding.debug_state()
    bidding.append(b1)
    bidding.debug_state()
    bidding.append(b2)
    bidding.debug_state()
    bidding.append(b3)
    bidding.debug_state()
    bidding.append(b4)
    bidding.debug_state()
    bidding.append(b5)
    bidding.debug_state()
    bidding.append(b6)
    bidding.debug_state()

    #Bid seq2
    b1 = Bid('1c')
    b2 = Bid('p')
    b3 = Bid('1s')
    b4 = Bid('1h')
    b5 = Bid('p')
    b6 = Bid('p')
    b7 = Bid('p')
    bidding = Bidding()
    bidding.debug_state()
    bidding.append(b1)
    bidding.debug_state()
    bidding.append(b2)
    bidding.debug_state()
    bidding.append(b3)
    bidding.debug_state()
    bidding.append(b4)
    bidding.debug_state()
    bidding.append(b5)
    bidding.debug_state()
    bidding.append(b6)
    bidding.debug_state()
    bidding.append(b7)
    bidding.debug_state()


    #Bid seq3
    b1 = Bid('p')
    b2 = Bid('p')
    b3 = Bid('p')
    b4 = Bid('p')
    bidding = Bidding()
    bidding.debug_state()
    bidding.append(b1)
    bidding.debug_state()
    bidding.append(b2)
    bidding.debug_state()
    bidding.append(b3)
    bidding.debug_state()
    bidding.append(b4)
    bidding.debug_state()


