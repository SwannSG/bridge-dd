import bid
import utility

class Bidding:

    def __init__(self):
        self.contract = ''
        self.position = -1  # is this position of declarer
        self.penalty = ''
        self.dealer = ''

        self.bids = [] # takes bid objects 
        self.bidding_closed = False
        self._no_suit_bid_count = 0
        self._last_suit_bid = bid.Bid(None) 
        self._bid_position = 1
        self._last_penalty = bid.Bid(None)

    def bid_ok(self, value:'Bid') -> bool:
        """
            Checks if a Bid is ok in the context of the bid stream
        """
        assert type(value)==bid.Bid
        if self.bidding_closed:
            return False
        if not self._last_suit_bid and self._no_suit_bid_count < 4:
            # no suit yet bid, 'pass' or any suit is ok 
            if value.bid=='P': return True
            if value.has_rank: return True
            return False
        if self._last_suit_bid and self._no_suit_bid_count < 3 and not value.has_rank:
            # bid = (P)ass || (D)bl || (R)dbl (and a suit has already been bid)
            if value.bid=='P': return True
            if value.bid=='D' and self._last_suit_bid.team() != value.team() and self._last_penalty != 'D' and self._last_penalty != 'R': return True
            if value.bid=='R' and value.team() != self._last_penalty.team() and self._last_penalty.bid == 'D': return True
            return False 
        if self._last_suit_bid and self._no_suit_bid_count < 3 and value.has_rank:
            # bid = suit
            if value.rank > self._last_suit_bid.rank: return True
            return False



    def add_bid(self, value:'Bid') -> None:
        assert type(value)==bid.Bid
        self._set_bid_position(value)     
        if self.bid_ok(value):
            if value.bid=='P':
                # bid = pass 'P'
                self.add_pass(value)
                if self.is_end_of_bidding():
                    self.end_of_bidding()
            elif value.has_rank:
                # bid = suit incl. no trumps
                self.add_suit(value)
            elif value.bid=='D':
                # bid = double 'D'
                self.add_double(value)
                if self.is_end_of_bidding():
                    self.end_of_bidding()
            elif value.bid=='R':
                # bid = redouble 'R'
                self.add_redouble(value)
                if self.is_end_of_bidding():
                    self.end_of_bidding()
        else:
            # NEED TO HANDLE DIFFENRENTLY
            raise ValueError('Bid not ok %s position %s' % (value.bid, value.position))

    def add_pass(self, value:'Bid'):
        assert type(value)==bid.Bid
        self._no_suit_bid_count += 1
        self.bids.append(value)

    def add_double(self,value:'Bid'):
        assert type(value)==bid.Bid
        self._no_suit_bid_count = 0
        self._last_penalty = value
        self.bids.append(value)

    def add_redouble(self,value:'Bid'):
        assert type(value)==bid.Bid
        self._no_suit_bid_count = 0
        self._last_penalty = value
        self.bids.append(value)

    def add_suit(self, value:'Bid'):
        assert type(value)==bid.Bid
        self._no_suit_bid_count = 0
        self._last_suit_bid = value
        self._last_penalty = None
        self.bids.append(value)

    def _set_bid_position(self, value:'Bid'):
        """
            set the position from which the bid was made 1,2,3,4 
        """
        assert type(value)==bid.Bid
        value.position = self._bid_position
        self._bid_position += 1

    def end_of_bidding(self):
        self.bidding_closed = True
        self._add_player_to_bids()
        self._set_contract()

    def _set_contract(self):
        self.contract = self._last_suit_bid.bid if self._last_suit_bid else 'all passed' 
        self.penalty = self._last_penalty.bid if self._last_penalty else ''
        if self.contract != 'all passed':
            declarer_position = self._first_time_suit_bid_position(self.contract[1])
            self.declarer = self.bids[declarer_position-1].player
            self.position = declarer_position
            pass
        else:
            self.declarer = ''

    def _first_time_suit_bid_position(self, suit:str):
        assert type(suit)==str and suit in utility.Constants.suits
        for value in self.bids:
            if len(value.bid)==2:
                if value.bid[1] ==suit:
                    return value.position
        return -1

    def is_end_of_bidding(self) -> bool:
        if self._last_suit_bid and self._no_suit_bid_count==3:
            return True
        if not self._last_suit_bid and self._no_suit_bid_count==4:
            return True
        return False

    def __repr__(self):
        d  = {1:['-','-','-'], 2:[], 3:['-'],4:['-','-']}
        l1 = []
        l2 = d[utility.Constants.dealer_value_inverse[self.dealer]]  
        for each in self.bids:
            if len(l2)==4:
                l1.append(l2)
                l2 = []
                l2.append(each.bid)
            else:
                l2.append(each.bid)
        r = 'W\tN\tE\tS\n'
        for each in l1:
            r  = r + '%s\t%s\t%s\t%s\n' % (each[0],each[1],each[2],each[3])
        if len(l2)==0:
            return r
        elif len(l2)==1:
            r = r + '%s\n' % l2[0]
        elif len(l2)==2:
            r = r + '%s\t%s\n' % (l2[0], l2[1])
        elif len(l2)==3:
            r = r + '%s\t%s\t%s\n' % (l2[0], l2[1], l2[3])
        return r

    def to_serial(self):
        l = []
        for v in self.bids:
            l.append(v.to_serial())
        return l

    def _add_player_to_bids(self):
        assert self.dealer
        for each in self.bids:
            each._set_player_from_position(self.dealer)


if __name__=='__main__':

    # test
    b = Bidding()
    b1 = bid.Bid('p')
    assert b.bid_ok(b1)==True
    b.add_bid(b1)
    assert b1.position==1
    # end

    # test with 4 pass bids
    b = Bidding()
    b.dealer = 'W'
    b.add_bid(bid.Bid('p'))
    assert b.bidding_closed==False
    b.add_bid(bid.Bid('p'))
    assert b.bidding_closed==False
    b.add_bid(bid.Bid('p'))
    assert b.bidding_closed==False
    b.add_bid(bid.Bid('p'))
    assert b.bidding_closed==True
    assert b.bids[0].position==1
    assert b.bids[1].position==2
    assert b.bids[2].position==3
    assert b.bids[3].position==4
    assert b.contract=='all passed'
    assert b.penalty==''
    assert b.position==-1
    assert b.declarer==''
    # end 

    b = Bidding()
    b.dealer = 'E'
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    assert b.contract=='1C'
    assert b.penalty==''
    assert b.position==2
    assert b.declarer=='S'
    # end

    b = Bidding()
    b.dealer = 'W'
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1S'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    assert b.contract=='1S'
    assert b.penalty==''
    assert b.position==4
    assert b.declarer=='S'
    # end


    # good dbl
    b = Bidding()
    b.dealer = 'N'
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1S'))
    b.add_bid(bid.Bid('D'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    assert b.contract=='1S'
    assert b.penalty=='D'
    assert b.position==4
    assert b.declarer=='W'
    # end

    # bad dbl
    b = Bidding()
    b.dealer = 'W'
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1S'))
    b.add_bid(bid.Bid('P'))
    r = 0
    try:
        b.add_bid(bid.Bid('D'))
        r = 1
    except:
        pass
    assert r==0
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    # end

    # bad rdbl
    b = Bidding()
    b.dealer = 'W'
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1S'))
    b.add_bid(bid.Bid('D'))
    b.add_bid(bid.Bid('P'))
    r = 0
    try:
        b.add_bid(bid.Bid('R'))
        r = 1
    except:
        pass
    assert r==0
    # end

    # good rdbl
    b = Bidding()
    b.dealer = 'W'
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('1d'))
    b.add_bid(bid.Bid('1h'))
    b.add_bid(bid.Bid('1s'))
    b.add_bid(bid.Bid('1n'))
    b.add_bid(bid.Bid('2c'))
    b.add_bid(bid.Bid('2d'))
    b.add_bid(bid.Bid('2h'))
    b.add_bid(bid.Bid('2s'))
    b.add_bid(bid.Bid('2n'))
    b.add_bid(bid.Bid('d'))
    b.add_bid(bid.Bid('r'))
    b.add_bid(bid.Bid('p'))
    b.add_bid(bid.Bid('p'))
    b.add_bid(bid.Bid('p'))
    assert b.contract=='2N'
    assert b.position==6
    assert b.penalty=='R'

