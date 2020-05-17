import card
import utility

class Hand(list):
    """
        Hand is a container of Card objects
    """
    def __init__(self):
        pass

    def append(self, value: 'Card'):
        if (isinstance(value, card.Card)):
            super().append(value)
        else:
            raise TypeError('object must be type Card')

    def bulk_append(self, facevalues:'str', suit:'str'):
        """
            bulk_append('569QKA', 's')
        """
        assert type(facevalues)==str
        assert type(suit)==str 
        suit = suit.upper()
        assert suit in utility.Constants.suits
        facevalues = facevalues.upper()
        for facevalue in facevalues:
            self.append(card.Card(facevalue, suit))

    def bulk_append_int(self, cards: 'list[int, ...]'):
        """
            bulk_append_int([10, 15, 25])
                integers as card representation
        """
        assert type(cards)==list
        for each in cards:
            self.append(card.Card(each))

    def bulk_append_card(self, cards: 'list[Card, ...]'):
        """
            cards = [Card(), Card()]
        """
        assert type(cards)==list
        for each in cards:
            self.append(each)


    def as_int(self) -> 'list[int, ...]':
        """
            Hand as card ints
        """
        r = []
        for card in self:
            r.append(card.as_int())
        return r

    def find(self, value:'str or int') -> int:
        """
            find a card in the Hand
            value: '6c' or int
            returns: index or -1
        """
        assert type(value)==str or type(value)==int 
        if isinstance(value, str):
            value = value.upper()
            try:
                value =  utility.Constants.cardStrToInt[value]
            except KeyError:
                return -1
        elif isinstance(value, int):   
            pass
        else:
            raise TypeError('value must be int 2 char string')
        try:
            return self.as_int().index(value)
        except:
            return -1

    def suit_split(self) -> 'tuple([spade, ...], [heart, ...], [diamond, ...], [club, ...])':
        """
            splits hand of card object into 4 suits 
        """
        d = {'S':[], 'H':[], 'D':[], 'C':[]}
        for each in self:
            suit = each.suit()
            d[suit].append(each)
        return (d['S'],d['H'],d['D'],d['C'])

    def arrange_LIN_cards(self):
        """
            arranges cards in LIN order
        """
        s,h,d,c = self.suit_split()
        s.sort()
        h.sort()
        d.sort()
        c.sort()
        self.clear()
        self.bulk_append_card(s + h + d + c)

    def to_serial(self):
        l = []
        for v in self:
            l.append(str(v))
        return l

if __name__ == '__main__':
    import card
    h = Hand()
    h.append( card.Card('JD') )
    h.append( card.Card('QS') )
    assert h==[card.Card('JD'), card.Card('QS')]
    assert h.as_int()==[23,50]
    assert h.find('QS')==1
    assert h.find(23)==0
    assert h.find('SS')==-1
    
    h = Hand()
    h.bulk_append('AT9543', 's')
    assert h==[card.Card('AS'), card.Card('TS'), card.Card('9S'),
    card.Card('5S'),card.Card('4S'),card.Card('3S')]

    h = Hand()
    h.bulk_append_card([card.Card('AS'), card.Card('TS'), card.Card('9S'),
    card.Card('5S'),card.Card('4S'),card.Card('3S')])
    assert h==[card.Card('AS'), card.Card('TS'), card.Card('9S'),
    card.Card('5S'),card.Card('4S'),card.Card('3S')]

    h = Hand()
    h.bulk_append_int([52,48,47,43,42,41])
    assert h==[card.Card('AS'), card.Card('TS'), card.Card('9S'),
    card.Card('5S'),card.Card('4S'),card.Card('3S')]

    h = Hand()
    h.bulk_append('AT9543', 's')
    h.bulk_append('AT9543', 'h')
    h.bulk_append('AT9543', 'd')
    h.bulk_append('AT9543', 'c')
    a,b,c,d = h.suit_split()
    assert a==[card.Card('AS'), card.Card('TS'), card.Card('9S'),
    card.Card('5S'),card.Card('4S'),card.Card('3S')]
    assert b==[card.Card('AH'), card.Card('TH'), card.Card('9H'),
    card.Card('5H'),card.Card('4H'),card.Card('3H')]
    assert c==[card.Card('AD'), card.Card('TD'), card.Card('9D'),
    card.Card('5D'),card.Card('4D'),card.Card('3D')]
    assert d==[card.Card('AC'), card.Card('TC'), card.Card('9C'),
    card.Card('5C'),card.Card('4C'),card.Card('3C')]
    
    'S569QKAH35D2467C4'
    h = Hand()
    h.bulk_append_card([card.Card('AS'), card.Card('2S'),
        card.Card('KH'), card.Card('2H'), card.Card('TH'),
        card.Card('AD'), card.Card('2D'),
        card.Card('KC'), card.Card('2C'), card.Card('TC')])
    h.arrange_LIN_cards()
    assert h==[ card.Card('2S'), card.Card('AS'), card.Card('2H'),
                card.Card('TH'), card.Card('KH'), card.Card('2D'),
                card.Card('AD'), card.Card('2C'), card.Card('TC'), card.Card('KC')]

    print (h.to_serial())