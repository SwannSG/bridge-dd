"""
    LIN file reader
"""
import re
import Board as bo

class ReadLinFile:

    dealer_value = {'1': 'S', '2':'W', '3':'N', '4':'E'}
    regex = regex = r"^S([AKQJT98765432]*)H([AKQJT98765432]*)D([AKQJT98765432]*)C([AKQJT98765432]*)"
    pattern = re.compile(regex)

    def __init__(self, fqfn):
        """
            fqfn: fully qualified filename
        """
        fp = open(file, 'r')
        text = fp.read()[:-2]
        fp.close()
        # list of (label, value) pairs
        self.lin = self._create_lable_value_pairs(text)
        self.board = bo.Board()
        self.bidding = bo.Bidding()
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
                self.board.bidding.append(bo.Bid(value))
            elif label=='pg':
                # start or end of playing round i.e 1 trick taken
                pass
            elif label=='pc':
                # card played, eg. D3, H9
                value = '%s%s' % (value[1],value[0])
                # self.board.play.append(bo.Card(value))

    def _pn(self, value):
        players = value.split(',')
        self.board.player_south = players[0]
        self.board.player_west = players[1]
        self.board.player_north = players[2]
        self.board.player_east = players[3]
        
    def _md(self, value):
        h1, h2, h3 = value[1:-1].split(',')
        self.board.deal_hand_1 = self._make_hand(h1)
        self.board.deal_hand_2 = self._make_hand(h2)
        self.board.deal_hand_3 = self._make_hand(h3)
        # h4 = cardpack - h1 - h2 - h3 
        self.board.calc_deal_hand_4()

    def _make_hand(self, value):
        """
            value = 'S569QKAH35D2467C4'
        """
        s,h,d,c = ReadLinFile.pattern.search(value).groups()
        hand = bo.Hand()
        hand.bulk_append(s, 'S')
        hand.bulk_append(h, 'H')
        hand.bulk_append(d, 'D')
        hand.bulk_append(c, 'C')
        return hand

file = '/home/steve/development/doubleDummy/data/3399426641.lin'
a = ReadLinFile(file)
b = a.board
print (b.board_name)
print (b.dealer)
print (b.bidding)
print (b.contract)
print (b.declarer)


    
