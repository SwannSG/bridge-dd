"""
    LIN file reader
"""
import re
import bid
import bidding
import board
import hand


class ReadLinFile:

    dealer_value = {'1': 'S', '2':'W', '3':'N', '4':'E'}
    regex = regex = r"^S([AKQJT98765432]*)H([AKQJT98765432]*)D([AKQJT98765432]*)C([AKQJT98765432]*)"
    pattern = re.compile(regex)

    position_to_declarer = {1: 'S', 2: 'W', 3: 'N', 4: 'E', 5: 'S', 6: 'W', 7: 'N', 8: 'E', 9: 'S', 10: 'W',
     11: 'N', 12: 'E', 13: 'S', 14: 'W', 15: 'N', 16: 'E', 17: 'S', 18: 'W', 19: 'N', 20: 'E',
     21: 'S', 22: 'W', 23: 'N', 24: 'E', 25: 'S', 26: 'W', 27: 'N', 28: 'E', 29: 'S', 30: 'W',
     31: 'N', 32: 'E', 33: 'S', 34: 'W', 35: 'N', 36: 'E', 37: 'S', 38: 'W', 39: 'N', 40: 'E',
     41: 'S', 42: 'W', 43: 'N', 44: 'E', 45: 'S', 46: 'W', 47: 'N', 48: 'E', 49: 'S', 50: 'W',
     51: 'N', 52: 'E', 53: 'S', 54: 'W', 55: 'N', 56: 'E', 57: 'S', 58: 'W', 59: 'N', 60: 'E',
     61: 'S', 62: 'W', 63: 'N', 64: 'E', 65: 'S', 66: 'W', 67: 'N', 68: 'E', 69: 'S', 70: 'W',
     71: 'N', 72: 'E', 73: 'S', 74: 'W', 75: 'N', 76: 'E', 77: 'S', 78: 'W', 79: 'N', 80: 'E',
     81: 'S', 82: 'W', 83: 'N', 84: 'E', 85: 'S', 86: 'W', 87: 'N', 88: 'E', 89: 'S', 90: 'W',
     91: 'N', 92: 'E', 93: 'S', 94: 'W', 95: 'N', 96: 'E', 97: 'S', 98: 'W', 99: 'N', 100: 'E'}

    def __init__(self, fqfn):
        """
            fqfn: fully qualified filename
        """
        fp = open(file, 'r')
        text = fp.read()[:-2]
        fp.close()
        # list of (label, value) pairs
        self.lin = self._create_lable_value_pairs(text)
        self.board = board.Board()
        self.bidding = bidding.Bidding()
        self.read_lin()

    def _create_lable_value_pairs(self, text) -> list:
        l = text.split('|')
        i = 0
        seq = []
        while i < len(l):
            seq.append( (l[i], l[i+1]))
            i = i + 2
        return seq       

    def read_lin(self):
        for (label, value) in self.lin:
            if label=='pn':
                # board players
                self._pn(value)
            elif label=='ah':
                # board name
                self.board.board_name = value
            elif label=='sv':
                # vulnerability
                self.board.vulnerable = value.upper()
            elif label=='md':
                # dealer & hands
                self.board.dealer = ReadLinFile.dealer_value[value[0]]
                self._md(value)
            elif label=='mb':
                # bid
                self.bidding.add_bid(bid.Bid(value))
            elif label=='pg':
                # start or end of playing round i.e 1 trick taken
                # bidding is over
                self.board.declarer = ReadLinFile.position_to_declarer[self.bidding.position]
                self.board.contract = self.bidding.contract
                self.board.penalty = self.bidding.penalty
            elif label=='pc':
                # card played, eg. D3, H9
                value = '%s%s' % (value[1],value[0])
                # self.board.play.append(bo.Card(value))

    def _pn(self, value:str):
        assert type(value)==str
        players = value.split(',')
        self.board.player_south = players[0]
        self.board.player_west = players[1]
        self.board.player_north = players[2]
        self.board.player_east = players[3]
        
    def _md(self, value:str):
        """
            Hand details
        """
        assert type(value)==str
        h1, h2, h3 = value[1:-1].split(',')
        self.board.deal_hand_1 = self._make_hand(h1)
        self.board.deal_hand_2 = self._make_hand(h2)
        self.board.deal_hand_3 = self._make_hand(h3)
        # h4 = cardpack - h1 - h2 - h3 
        self.board.calc_deal_hand_4()

    def _make_hand(self, value:str):
        """
            value = 'S569QKAH35D2467C4'
        """
        assert type(value)==str
        s,h,d,c = ReadLinFile.pattern.search(value).groups()
        hnd = hand.Hand()
        hnd.bulk_append(s, 'S')
        hnd.bulk_append(h, 'H')
        hnd.bulk_append(d, 'D')
        hnd.bulk_append(c, 'C')
        return hnd


if __name__=='__main__':
    print ('__main__ executing')
    file = '/home/steve/development/doubleDummy/data/3399426641.lin'
    a = ReadLinFile(file)
    b = a.board
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
    assert b.declarer=='E'


