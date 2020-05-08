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

    def bulk_append(self, facevalues:str, suit:str):
        """
            bulk_append('s', 'AT9543')
        """
        suit = suit.upper()
        facevalues = facevalues.upper()
        for facevalue in facevalues:
            self.append(card.Card(facevalue, suit))

    def bulk_append_int(self, cards: 'list[int, ...]'):
        """
            bulk_append_int([10, 15, 25])
                integers as card representation
        """
        for each in cards:
            self.append(card.Card(each))

    def bulk_append_card(self, cards: 'list[Card, ...]'):
        """
            cards = [Card(), Card()]
        """
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

    def suit_split(self) -> 'tuple([spades], [hearts], [diamonds], [clubs])':
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
    