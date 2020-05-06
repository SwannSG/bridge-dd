"""
    LIN file reader
"""
import Board as bo

class ReadLinFile:

    dealer_value = {'1': 'S', '2':'W', '3':'N', '4':'E'}

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
            print (l[i], l[i+1])
            print (i + 1)
            seq.append( (l[i], l[i+1]))
            i = i + 2
        return seq       

    def read_lin(self):
        for (label, value) in self.lin:
            if label=='pn':
                self._pn(value)
            elif label=='ah':
                self.board.board_name = value
            elif label=='sv':
                self.board.vulnerable = value.upper()
            elif label=='md':
                self.board.dealer = ReadLinFile.dealer_value[value[0]]
                
    def _pn(self, value):
        players = value.split(',')
        print (players)
        self.board.player_south = players[0]
        self.board.player_west = players[1]
        self.board.player_north = players[2]
        self.board.player_east = players[3]
        




file = '/home/steve/development/doubleDummy/data/3399426641.lin'
a = ReadLinFile(file)
b = a.board




    
