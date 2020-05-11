"""
    CHECK DOUBLE OR REDOUBLE IS NOT MADE OVER PARTNERS BID 
"""

import bid
import descriptors
import utility

class Bidding(list):
    """
        Bidding is a container of Bid objects 
    """
    
    def __init__(self):

        # must be read only properties from outside
        # and one shot setting
        self._contract = ''
        self._penalty = ''
        self._declarer_position = -1
        
        # properties used internally
        self._no_suit_bid_count = 0
        self._last_suit_bid = ''
        self._last_penalty = ''
        self._debug_bid_value = ''

    def get_contract(self): return self._contract
    def get_penalty(self): return self._penalty
    def get_declarer_position(self): return self._declarer_position

    def set_contract(self, value):
        if not self.get_contract():
            self._contract = value

    def set_penalty(self, value):
        if not self.get_penalty():
            self._penalty = value

    def set_declarer_position(self, value):
        if self.get_declarer_position() == -1:
            self._declarer_position = value

    def debug_state(self):
        # method for debug
        print ('value bid: %s' % self._debug_bid_value)
        print ('contract:%s, penalty:%s, declarer_position:%s' % 
                (self.get_contract(), self.get_penalty(), self.get_declarer_position()))
        print ('_no_suit_bid_count:%s, _last_suit_bid:%s, _last_penalty:%s' % (self._no_suit_bid_count, self._last_suit_bid, self._last_penalty)  )        
        print ()
        
    def append(self, value:'Bid'):
        if self.get_contract():
            raise ValueError('Bidding is closed')
        if (isinstance(value, bid.Bid)):
            self._add_bid_if_valid(value)
        else:
            raise TypeError('object must be type Bid: %s' % value)

    def _last_suit_bid_rank(self) -> int:
        """
            returns rank of suit as a string eg. '1c'
                and
            return 0 if _last_suit_bid is an empty string 
        """
        if not self._last_suit_bid:
            return 0
        else:
            return utility.Constants.bid_rank[self._last_suit_bid]

    def _add_bid_if_valid(self, value:'Bid') -> bool:
        self._debug_bid_value = value.bid
        if self._is_suit_bid(value.bid):
            # suit bid e.g '1c', '1n'
            if value.rank() > self._last_suit_bid_rank(): 
                self._last_suit_bid = value.bid
                self._no_suit_bid_count = 0
                super().append(value)
            else:
                raise ValueError('bid, must be at a level above %s, bid is %s' % (self._last_suit_bid, value))
        elif value.bid==utility.Constants.double:
            # dbl
            if not self._last_suit_bid:
                # no suit bid
                raise ValueError('bid, cannot double when no suit yet bid') 
            if not self._last_penalty:
                self._last_penalty = utility.Constants.double
                self._no_suit_bid_count = self._no_suit_bid_count + 1
                super().append(value)
            else:
                raise ValueError('bid, cannot double when previous penalty is: %s' % self._last_penalty)
        elif value.bid==utility.Constants.redouble:
            # rdbl
            if self._last_penalty==utility.Constants.double:
                self._last_penalty = utility.Constants.redouble
                self._no_suit_bid_count = self._no_suit_bid_count + 1
                super().append(value)
            else:
                raise ValueError('bid, cannot redouble when previous penalty is: %s' % self._last_penalty)
        elif value.bid==utility.Constants.pass_:
            # pass
            if self._last_suit_bid:
                # suit has been bid
                if self._no_suit_bid_count < 3:
                    self._no_suit_bid_count = self._no_suit_bid_count + 1
                    super().append(value)
                    if self._no_suit_bid_count == 3:
                        self._end_of_bidding()
            else:
                # no suit has been bid, p-p-p-p edge case
                if self._no_suit_bid_count < 4:
                    self._no_suit_bid_count = self._no_suit_bid_count + 1
                    super().append(value)
                    if self._no_suit_bid_count==4:
                        # Bidding is at an end
                        self.set_contract('none')
        else:
            raise ValueError('unkown bid: %s' % value.bid)

    def _end_of_bidding(self):
        """
            does updates at end of bidding
        """
        self.set_contract(self._last_suit_bid)
        self.set_penalty(self._last_penalty)
        self.set_declarer_position(len(self)%4) 
    

    def _declarer(self, position, dealer):
        """
            E,3     E,S,W,N
        """
        pass

    def _is_suit_bid(self, value:'str') -> bool:
        """
            for any bids not 'p'ass, 'd'bl, 'r'db
        """
        if value in utility.Constants.is_not_suit_bid:
            return False
        else:
            return True

if __name__=='__main__':
    g = Bidding()
    b1 = bid.Bid('1h')
    g.append(b1)
    assert g==[b1]
    temp = 0
    try:
        g.append(b1)
        g.debug_state()
        temp = temp + 1
    except ValueError:
        pass
    assert temp==0

    g = Bidding()
    b1 = bid.Bid('1h')
    g.append(b1)
    temp = 0
    try:
        g.append(bid.Bid('1c'))
        temp = temp + 1
    except ValueError:
        pass
    assert temp==0

    g = Bidding()
    b1 = bid.Bid('d')


    

"""

    # 4 passes
    g = Bidding()
    assert g.get_penalty()==''
    assert g.get_contract()==''
    assert g.get_declarer_position()==-1
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    assert g.get_contract()=='none'; assert g.get_declarer_position()==-1; assert g.get_penalty()==''

    g = Bidding()
    g.append(bid.Bid('1h'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    assert g.get_contract()=='1H'; assert g.get_declarer_position()==0; assert g.get_penalty()==''

    g = Bidding()
    g.append(bid.Bid('1h'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('1s'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    temp = 0
    try:
        g.append(bid.Bid('1c'))
        temp = temp + 1
    except ValueError:
        pass
    assert temp==0
    assert g.get_contract()=='1S'; assert g.get_declarer_position()==3; assert g.get_penalty()==''

    g = Bidding()
    g.append(bid.Bid('1h'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('p'))
    g.append(bid.Bid('1c'))

    temp = 0
    try:
        g.append(bid.Bid('1c'))
        temp = temp + 1
    except ValueError:
        pass
    assert temp==0

    temp = 0
    try:
        g.append(bid.Bid('d'))
        temp = temp + 1
    except ValueError:
        pass
    assert temp==0
"""