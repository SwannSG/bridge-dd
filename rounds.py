import card_for_round
import utility

class Rounds():
    """
        Collection of round objects
    """
    @staticmethod
    def get_lead_player_from_declarer(declarer):
        assert (declarer=='S' or declarer=='W' or declarer=='N' or declarer=='E')
        d = {'E':'S', 'S':'W', 'W':'N', 'N':'E'}
        return d[declarer]

    @staticmethod
    def get_player_from_position(position:'int 0,1,2,3', who_led:'str S,W,N,E') ->'str:S,W,N,E' :
        assert (position==0 or position==1 or position==2 or position==3)  
        assert (who_led=='S' or who_led=='W' or who_led=='N' or who_led=='E')
        if who_led=='S':
            d = {0:'S',1:'W',2:'N',3:'E'}
        elif who_led=='W':
            d = {0:'W',1:'N',2:'E',3:'S'}
        elif who_led=='N':
            d = {0:'N',1:'E',2:'S',3:'W'}
        elif who_led=='E':
            d = {0:'E',1:'S',2:'W',3:'N'}
        return d[position]

    def __init__(self):
        self.rounds = []
        self.contract = ''  # 1N, 3S
        self.declarer = ''  # S,W,N,E
        self._current_suit = ''
        self._current_round = []
        self._count = 0
        self._player_of_lead = '' 
        

    def new_round_card(self, card:str, is_first_round=False):
        """
            card: "2C", player: N,S,W,E
        """
        self._current_suit = card[1]
        if self._is_trump(card):
            # trump
            value = utility.Constants.cardStrToInt[card] + 100
        else:
            # not a trump
            value = utility.Constants.cardStrToInt[card]
        if is_first_round:
            self._player_of_lead = Rounds.get_lead_player_from_declarer(self.declarer)
            self._current_round.append(card_for_round.CardForRound(card, value, self._player_of_lead))
        else:
            self._current_round.append(card_for_round.CardForRound(card, value, self._player_of_lead))
        self._count += 1

    def next_card(self, card:str):
        """
            next card in current round
        """
        assert self._count!=0
        assert self._count<=3
        if self._is_trump(card):
            # trump
            value = utility.Constants.cardStrToInt[card] + 100
        else:
            # not a trump
            if self._current_suit==card[1]:
                # following suit
                value = utility.Constants.cardStrToInt[card]
            else:
                # not following suit & not a trump
                value = 0
        # self._player_of_lead
        self._current_round.append(card_for_round.CardForRound(
            card,
            value,
            Rounds.get_player_from_position(self._count, self._player_of_lead)))
        self._count += 1
        if self._count==4:
            # end of current round
            self._count = 0
            self.rounds.append(self._current_round)
            winning_card = max(self._current_round) # CardForRound obj
            winning_card.winner = True
            winning_position = self._current_round.index(winning_card)
            self._player_of_lead = Rounds.get_player_from_position(winning_position, who_led=self._player_of_lead)
            self._current_round = []

    def _is_trump(self, card:str):
        if self.contract[1]=='N':
            return False
        if self.contract[1]==card[1]:
            return True
        return False

