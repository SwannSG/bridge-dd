"""
    BBO LIN file reader
"""
import re
import bid
import bidding
import board
import hand
import rounds
import utility


class ReadLinFile:
    """
        BBO LIN file reader
        Creates an internal Board object  
    """
    _dealer_value = utility.Constants.dealer_value
    _regex = regex = r"^S([AKQJT98765432]*)H([AKQJT98765432]*)D([AKQJT98765432]*)C([AKQJT98765432]*)"
    _pattern = re.compile(_regex)

    def __init__(self, fqfn:'str: fully qualified file name'):
        """
            fqfn: fully qualified filename
        """
        assert type(fqfn)==str
        fp = open(file, 'r')
        text = fp.read()[:-2]
        fp.close()
        # list of (label, value) pairs
        self._lin = self._create_lable_value_pairs(text)
        
        self._board = board.Board()
        self._bidding = bidding.Bidding()
        self._rounds = rounds.Rounds()
        
        self._start_playing_round = False
        self._playing_round_count = 0
        self._is_first_pg = True
        self._read_lin()


    def _create_lable_value_pairs(self, text:str) -> list:
        assert type(text)==str
        l = text.split('|')
        i = 0
        seq = []
        while i < len(l):
            seq.append( (l[i], l[i+1]))
            i = i + 2
        return seq       

    def _read_lin(self):
        for (label, value) in self._lin:
            if label=='pn':
                # board players
                self._pn(value)
            elif label=='ah':
                # board name
                self._board.board_name = value
            elif label=='sv':
                # vulnerability
                self._board.vulnerable = value.upper()
            elif label=='md':
                # dealer & hands
                    # dealer set to S,W,N,E                
                self._bidding.dealer = ReadLinFile._dealer_value[value[0]]
                self._board.dealer = self._bidding.dealer
                    # hands
                self._md(value)
            elif label=='mb':
                # each bid
                self._bidding.add_bid(bid.Bid(value))
            elif label=='pg':
                # start or end of playing round i.e 1 trick taken
                self._start_playing_round = True
                if self._is_first_pg:
                    # first time pg tag is encountered
                    # bidding is over
                    self._board.contract = self._bidding.contract
                    self._board.penalty = self._bidding.penalty
                    self._board.declarer = self._bidding.declarer
                    self._rounds.declarer = self._board.declarer
                    self._rounds.contract = self._board.contract
            elif label=='pc':
                # card played, eg. D3, H9
                card = '%s%s' % (value[1],value[0])
                if self._start_playing_round:
                    self._start_playing_round = False
                    self._playing_round_count = 1
                    self._rounds.new_round_card(card, self._is_first_pg)
                    self._is_first_pg = False
                else:
                    self._playing_round_count += 1
                    self._rounds.next_card(card)
                    print (self._rounds._current_round)
                    if self._playing_round_count==4:
                        self._start_playing_round = True
            elif label=='mc':
                # tricks claimed
                self._board.tricks_made = int(value) if value else -1
                        
        # end of file reached
        self._board.bidding = self._bidding
        self._board.play = self._rounds
        if self._board.tricks_made==-1:
            self._board.tricks_made = int(self._rounds._tricks_made(self._board.declarer))

    def _pn(self, value:str):
        """
            value: "barbswill,chriskr,adelemk,SwannSG:
        """
        assert type(value)==str
        players = value.split(',')
        self._board.player_south = players[0]
        self._board.player_west = players[1]
        self._board.player_north = players[2]
        self._board.player_east = players[3]
        
    def _md(self, value:str):
        """
            'S569QKAH35D2467C4,S2H78TQKD39TC367Q,S34TJH46ADQAC89JK,'
        """
        assert type(value)==str
        h1, h2, h3 = value[1:-1].split(',')
        self._board.deal_hand_1 = self._make_hand(h1)
        self._board.deal_hand_2 = self._make_hand(h2)
        self._board.deal_hand_3 = self._make_hand(h3)
        self._board.calc_deal_hand_4()

    def _make_hand(self, value:str):
        """
            value = 'S569QKAH35D2467C4'
        """
        assert type(value)==str
        s,h,d,c = ReadLinFile._pattern.search(value).groups()
        hnd = hand.Hand()
        hnd.bulk_append(s, 'S')
        hnd.bulk_append(h, 'H')
        hnd.bulk_append(d, 'D')
        hnd.bulk_append(c, 'C')
        return hnd

if __name__=='__main__':
    print ('__main__ executing')
    file = '/home/steve/development/doubleDummy/data/3399426641.lin'
    file = '/home/steve/development/doubleDummy/data/3441845996.lin'
    if file=='/home/steve/development/doubleDummy/data/3399426641.lin':
        a = ReadLinFile(file)
        b = a._board
        assert b.board_name=='Board 18'  
        assert b.player_south=='barbswill'
        assert b.player_west=='chriskr'  
        assert b.player_north=='adelemk'
        assert b.player_east=='SwannSG'
        assert str(b.deal_hand_1)=='[5S, 6S, 9S, QS, KS, AS, 3H, 5H, 2D, 4D, 6D, 7D, 4C]'
        assert str(b.deal_hand_2)=='[2S, 7H, 8H, TH, QH, KH, 3D, 9D, TD, 3C, 6C, 7C, QC]'
        assert str(b.deal_hand_3)=='[3S, 4S, TS, JS, 4H, 6H, AH, QD, AD, 8C, 9C, JC, KC]'
        assert str(b.deal_hand_4)=='[7S, 8S, 2H, 9H, JH, 5D, 8D, JD, KD, 2C, 5C, TC, AC]'
        assert b.dealer=='E'
        assert b.vulnerable=='N'
        assert b.contract=='4S'
        assert b.penalty==''
        assert b.declarer=='S'
        assert b.tricks_made==10
        # IMPLEMENT ITER & NEXT
        for each in b.play.rounds:
            print (each)
    if file == '/home/steve/development/doubleDummy/data/3441845996.lin':
        a = ReadLinFile(file)
        b = a._board
        assert b.board_name=='Board 1'  
        assert b.player_south=='omanbik'
        assert b.player_west=='pauleeeee'  
        assert b.player_north=='giubel'
        assert b.player_east=='TimCSF'
        assert str(b.deal_hand_1)=='[6S, 6H, AH, 8D, 9D, KD, AD, 2C, 5C, 7C, 8C, KC, AC]'
        assert str(b.deal_hand_2)=='[9S, QS, KS, AS, 5H, 7H, 9H, JH, 5D, QD, 3C, 6C, 9C]'
        assert str(b.deal_hand_3)=='[2S, 7S, TS, JS, 2H, 4H, 8H, TH, QH, 3D, 4C, TC, JC]'
        assert str(b.deal_hand_4)=='[3S, 4S, 5S, 8S, 3H, KH, 2D, 4D, 6D, 7D, TD, JD, QC]'
        assert b.dealer=='N'
        assert b.vulnerable=='O'
        assert b.contract=='5S'
        assert b.penalty=='D'
        assert b.declarer=='W'
        assert b.tricks_made==5
        # IMPLEMENT ITER & NEXT
        for each in b.play.rounds:
            print (each)
