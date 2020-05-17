import utility
import bidding
import card
import hand

class Board:
    """
        Board object represents a board of bridge
    """
    # O=None, B=Both, N=NorthSouth, E=EastWest
    _vulnerable_values = ['O', 'B', 'N', 'E']
    _dealer_values = ['N', 'S', 'W', 'E']

    @staticmethod
    def meaning_of_vulnerable_values():
        print ("'O'=None, 'B'=Both, 'N'=NorthSouth, 'E'=EastWest")

    @staticmethod
    def meaning_of_dealer_values():
        print ('"N"=North, "S"=South, "W"=West, "E"=East')

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
        self.bidding = None # Bidding obj
        self.declarer = ''  
        self.contract = ''
        self.penalty = ''
        self.play = None    # Rounds obj
        self.tricks_made = -1

    @property
    def vulnerable(self):
        return self.__vulnerable

    @vulnerable.setter
    def vulnerable(self,value:str):
        assert value in Board._vulnerable_values
        self.__vulnerable = value 

    @property
    def dealer(self):
        return self.__dealer

    @dealer.setter
    def dealer(self,value:str):
        assert value in Board._dealer_values
        self.__dealer = value
        
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

    def to_serial(self):
        d = {}
        d['player_south'] = self.player_south
        d['player_west'] = self.player_west
        d['player_north'] = self.player_north
        d['player_east'] = self.player_east
        d['board_name'] = self.board_name
        d['vulnerable'] = self.vulnerable
        d['dealer'] = self.dealer
        d['deal_hand_1'] = self.deal_hand_1.to_serial()
        d['deal_hand_2'] = self.deal_hand_2.to_serial()
        d['deal_hand_3'] = self.deal_hand_3.to_serial()
        d['deal_hand_4'] = self.deal_hand_4.to_serial()
        d['bidding'] = self.bidding.to_serial()
        d['declarer'] = self.declarer  
        d['contract'] = self.contract
        d['penalty'] = self.penalty
        # self.play = None    # Play obj
        return d

if __name__  == '__main__':
    Board.meaning_of_dealer_values()
    Board.meaning_of_vulnerable_values()
