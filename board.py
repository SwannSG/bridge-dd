import utility
import bidding
import card
import hand
import play

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
        self.deal_hand_1 = hand.Hand()
        self.deal_hand_2 = hand.Hand()
        self.deal_hand_3 = hand.Hand()
        self.deal_hand_4 = hand.Hand()
        self.bidding = bidding.Bidding()
        self.declarer = ''  
        self.contract = ''
        self.penalty = ''
        self.play = play.Play()

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
            special method used by LIN files for 4th hand
        """
        h1 = self.deal_hand_1.as_int()
        h2 = self.deal_hand_2.as_int()
        h3 = self.deal_hand_3.as_int()
        h4 = list(set(utility.Constants.all_cards).difference(set(h1+h2+h3)))
        self.deal_hand_4.bulk_append_int(h4)
        self.deal_hand_4.arrange_LIN_cards()








if __name__  == '__main__':

"""
    #Bid seq1
    # b1 = Bid('1c')
    # b2 = Bid('p')
    # b3 = Bid('1s')
    # b4 = Bid('p')
    # b5 = Bid('d')
    # b6 = Bid('r')
    # bidding = Bidding()
    # bidding.debug_state()
    # bidding.append(b1)
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
    print (bidding)

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
"""

