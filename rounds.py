import card_for_round
import utility

class Rounds(list):
    """
        Collection of round objects
    """
    @staticmethod
    def get_player_of_lead(declarer):
        d = {'E':'S', 'S':'W', 'W':'N', 'N':'E'}
        return d[declarer]

    def __init__(self):
        self.contract = ''  # 1N, 3S
        self.declarer = ''  # S,W,N,E
        self._current_suit = ''
        self._current_round = []
        self._count = 0
        

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
            self._current_round.append(card_for_round.CardForRound(card, value, Rounds.get_player_of_lead(self.declarer)))
        else:
            # !!! MUST ADD WINNER OF LAST TRICK
            self._current_round.append(card_for_round.CardForRound(card, value, ''))
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
        self._current_round.append(card_for_round.CardForRound(card, value, ''))
        self._count += 1
        if self._count==4:
            # end of current round
            self._count = 0
            self.append(self._current_round)

    def _is_trump(self, card:str):
        if self.contract[1]=='N':
            return False
        if self.contract[1]==card[1]:
            return True
        return False
