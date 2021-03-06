import utility

class Bid:
    """
        Bid object
            bid '2c', alert, comment
            position    (added later, position in bidding stream, allows team to be determined) 
    """


    def __init__(self, bid, player:'str:S,W,N,E'='', alert='', comment=''):
        if bid:
            bid = bid.upper()
            self.bid = bid
            self.alert = alert
            self.comment = comment
            self.player = ''                     # S,W,N.E
            self.position = -1                   # position inside bidding stream 1,2,...
            self.has_rank = self._is_suit(bid)   # bool
            self.rank = self._get_rank(bid)      # -1 if no rank 
        else:
            # None of empty bid Bid(None), Bid('')
            self.bid = ''
            self.alert = ''
            self.comment = ''
            self.position = -1                   # position inside bidding stream
            self.has_rank = False                # bool
            self.rank = -1                       # -1 if no rank 

    def _get_rank(self, value:'str') -> int:
        """
            2c has rank 1, 3c has rank 2
            include no trumps as well
            excludes pass, double and redouble
        """
        assert type(value)==str
        if value in utility.Constants.bid_rank: 
            return utility.Constants.bid_rank[value]
        return -1

    def _is_suit(self, value:'str') -> bool:
        """
            for any bids not 'p'ass, 'd'bl, 'r'db
            includes no trumps
        """
        assert type(value)==str
        if value in utility.Constants.is_not_suit_bid: return False
        return True

    def __repr__(self):
        return '%s:%s:%s:%s:%s:%s' % (self.bid, self.alert, self.comment, self.team(), self.player, self.position)

    def __str__(self):
        return '%s' % self.bid

    def __bool__(self):
        return False if self.bid=='' else True

    def team(self):
        """
            Associates bid with team A or team B
            odd number = A, even number = B
        """
        return 'B' if self.position % 2==0 else 'A'

    def to_serial(self, properties = ['bid', 'alert', 'comment']):
        """
            returns dictionary represenstation of the object
            which can be used for json conversion 
        """
        d = {}
        for each in properties:
            d[each] = self.__dict__[each]
        return d

    def _set_player_from_position(self, dealer:'str S,W,N,E'):
        """
            Determines whether bid is from player S,W,N,E
            from position in bid stream and who dealer is
        """
        assert type(dealer)==str and dealer in utility.Constants.dealer_value_inverse
        d = {   'S': {1:'S', 2:'W', 3:'N', 0:'E'},
                'W': {1:'W', 2:'N', 3:'E', 0:'S'},
                'N': {1:'N', 2:'E', 3:'S', 0:'W'},
                'E': {1:'E', 2:'S', 3:'W', 0:'N'}}
        result = ''
        if self.position<4:
            result = d[dealer][self.position]
        elif self.position==4:
            result = d[dealer][0]
        else:
            result = d[dealer][self.position % 4]    
        self.player = result
        return self.player

if __name__=='__main__':
    b = Bid('3s', alert='alert', comment='comment')
    assert b.bid=='3S'
    assert b.alert=='alert'
    assert b.comment=='comment'
    assert str(b)=='3S'
    assert b.has_rank==True
    assert b.rank==14
    r = True if b else False
    assert r==True

    b = Bid('3s', alert='alert', comment='comment')
    b.position = 5
    assert b.team()=='A'
    b.position = 6
    assert b.team()=='B'
    r = True if b else False
    assert r==True

    b = Bid('p')
    assert b.bid=='P'
    assert b.alert==''
    assert b.comment==''
    assert str(b)=='P'
    assert b.has_rank==False
    assert b.rank==-1 
    r = True if b else False
    assert r==True

    b = Bid('d')
    assert b.bid=='D'
    assert b.alert==''
    assert b.comment==''
    assert str(b)=='D'
    assert b.has_rank==False
    assert b.rank==-1 
    r = True if b else False
    assert r==True

    b = Bid('r')
    assert b.bid=='R'
    assert b.alert==''
    assert b.comment==''
    assert str(b)=='R'
    assert b.has_rank==False
    assert b.rank==-1 
    r = True if b else False
    assert r==True


    b = Bid('2n')
    assert b.bid=='2N'
    assert b.alert==''
    assert b.comment==''
    assert str(b)=='2N'
    assert b.has_rank==True
    assert b.rank==10
    r = True if b else False
    assert r==True


    b = Bid(None)
    assert b.bid==''
    assert b.alert==''
    assert b.comment==''
    assert str(b)==''
    assert b.has_rank==False
    assert b.rank==-1
    r = True if b else False
    assert r==False

    b = Bid('')
    assert b.bid==''
    assert b.alert==''
    assert b.comment==''
    assert str(b)==''
    assert b.has_rank==False
    assert b.rank==-1
    r = True if b else False
    assert r==False

    # test teams
    a = Bid('p')
    a.position = 1
    assert a.team()=='A'
    a.position = 2
    assert a.team()=='B'
    a.position = 3
    assert a.team()=='A'
    a.position = 4
    assert a.team()=='B'

    a.position = 5
    assert a.team()=='A'
    a.position = 6
    assert a.team()=='B'
    a.position = 7
    assert a.team()=='A'
    a.position = 8
    assert a.team()=='B'

    a.position = 9
    assert a.team()=='A'
    a.position = 10
    assert a.team()=='B'
    a.position = 11
    assert a.team()=='A'
    a.position = 12
    assert a.team()=='B'

    a.position = 13
    assert a.team()=='A'
    a.position = 14
    assert a.team()=='B'
    a.position = 15
    assert a.team()=='A'
    a.position = 16
    assert a.team()=='B'
