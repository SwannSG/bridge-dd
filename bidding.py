import descriptors
import utility

class Bidding(list):
    """
        Bidding is a container of Bid objects 
    """

    
    def __init__(self):

        # must be read only properties from outside
        # and one shot setting
        self.contract = descriptors.OneShotDesciptor()
        self.penalty = descriptors.OneShotDesciptor()
        self.declarer_position = descriptors.OneShotDesciptor()
        
        # properties used internally
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
                        self.contract = 'none'
        else:
            raise ValueError('unkown bid: %s' % value.bid)

    def _end_of_bidding(self):
        """
            checks if bidding is at an end
            and updates necessary
        """
        self.contract = self._last_suit_bid
        self.penalty = self._last_penalty
        # Update declarer 
        self.declarer = len(self)%4 
        pass

    def _declarer(self, position, dealer):
        """
            E,3     E,S,W,N
        """
        pass

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

