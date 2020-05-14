class CardForRound:

    def __init__(self, card:str, value:int, player:str):
        # card "2C"
        self.card = card
        self.value = value
        self.player = player # S,W,N,E
        self.winner = False

    def __repr__(self):
        return '%s:%s%s' % (self.card, self.player, '*' if self.winner else '')

    def __lt__(self, other:'CardForRound') -> bool:
        if self.value < other.value:
            return True
        return False

