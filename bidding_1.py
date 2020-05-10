import bid
import utility

class Bidding:

    def __init__(self):
        self.contract = ''
        self.position = -1
        self.penalty = ''

        self.bids = [] # takes bid objects 
        self.bidding_closed = False
        self._no_suit_bid_count = 0
        self._last_suit_bid = bid.Bid(None) 
        self._bid_position = 1
        self._last_penalty = bid.Bid(None)

    def bid_ok(self, value:'Bid') -> bool:
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
        self._no_suit_bid_count += 1
        self.bids.append(value)

    def add_double(self,value:'Bid'):
        self._no_suit_bid_count = 0
        self._last_penalty = value
        self.bids.append(value)

    def add_redouble(self,value:'Bid'):
        self._no_suit_bid_count = 0
        self._last_penalty = value
        self.bids.append(value)

    def add_suit(self, value:'Bid'):
        self._no_suit_bid_count = 0
        self._last_suit_bid = value
        self._last_penalty = None
        self.bids.append(value)

    def _set_bid_position(self, value:'Bid'):
        """
            set the position from which the bid was made 1,2,3,4 
        """
        value.position = self._bid_position
        self._bid_position += 1

    def end_of_bidding(self):
        self.bidding_closed = True
        self._set_contract()

    def _set_contract(self):
        self.contract = self._last_suit_bid.bid if self._last_suit_bid else 'all passed' 
        self.position = self._last_suit_bid.position if self._last_suit_bid else -1
        self.penalty = self._last_penalty.bid if self._last_penalty else ''

    def is_end_of_bidding(self) -> bool:
        if self._last_suit_bid and self._no_suit_bid_count==3:
            return True
        if not self._last_suit_bid and self._no_suit_bid_count==4:
            return True
        return False





if __name__=='__main__':

    """
    # test
    b = Bidding()
    b1 = bid.Bid('p')
    assert b.bid_ok(b1)==True
    b.add_bid(b1)
    assert b1.position==1
    # end

    # test with 4 pass bids
    b = Bidding()
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
    # end 

    b = Bidding()
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    assert b.contract=='1C'
    assert b.penalty==''
    assert b.position==2
    # end

    b = Bidding()
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
    # end


    # good dbl
    b = Bidding()
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
    # end
    """
    # bad dbl
    b = Bidding()
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1S'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('D'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('P'))
    # end

    """
    # bad rdbl
    b = Bidding()
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1C'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('1S'))
    b.add_bid(bid.Bid('D'))
    b.add_bid(bid.Bid('P'))
    b.add_bid(bid.Bid('R'))
    assert b.position==4
    # end
    """
