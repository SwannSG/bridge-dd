import utility

class Card:
    """
        Card object
    """
    def __init__(self, value, suit=''):
        suit = suit.upper()
        if isinstance(value, str):
            value = value.upper()
            if len(value)==2:
                # e.g. 2S
                self._validate_face_value(value[0])
                self._validate_suit(value[1])
                self._card = utility.Constants.cardStrToInt[value]
            elif len(value)==1:
                self._validate_face_value(value)
                self._validate_suit(suit)
                self._card = utility.Constants.cardStrToInt[value + suit ]
        elif isinstance(value, int):
            if suit:
                self._validate_face_value(str(value))
                self._validate_suit(suit)
                self._card = utility.Constants.cardStrToInt[str(value) + suit ]
            else:
                if self._validate_card_as_int(value):
                    self._card = value 
        else:
            raise TypeError('value must be int or 1 or 2char e.g. 2s, 2')

    def _validate_face_value(self, value:str) -> bool:
        if value in utility.Constants.facevalues:
            return True
        else:
            raise ValueError('invalid card facevalue: %s' % value)

    def _validate_suit(self, value:str) -> bool:
        if value in utility.Constants.suits:
            return True
        else:
            raise ValueError('invalid card suit: %s' % value)

    def _validate_card_as_int(self, value:int) -> bool:
        if value in utility.Constants.all_cards:
            return True
        else:
            raise ValueError('invalid card integer: %s' % value)

    def __str__(self) -> str:
        return str(self.__repr__())

    def __repr__(self):
        return '%s%s' % (self.facevalue(), self.suit())

    def suit(self) -> str:
        # return card as suit eg.'S'
        return utility.Constants.cardIntToSuit[self._card]


    def facevalue(self) -> str:
        # return card facevalue as string eg.'A'
        return utility.Constants.cardIntToStr[self._card][0]

    def as_int(self) -> int:
        # returns cards as int
        return self._card

    def __eq__(self, other:'Card') -> bool:
        if self.as_int()==other.as_int():
            return True
        return False

    def __lt__(self, other:'Card') -> bool:
        if self.as_int() < other.as_int():
            return True
        return False

if __name__  == '__main__':
    c1 = Card(23)   #'JD'
    assert c1.facevalue() == 'J'
    assert c1.suit() == 'D'
    assert c1.as_int() == 23
    assert str(c1) == 'JD'

    # __eq__
    assert c1==Card('JD')
    #__lt__
    assert c1<Card('AS')

    #_validate_face_value
    assert c1._validate_face_value('T')==True
    try:
        assert c1._validate_face_value('Z')==False
    except ValueError:
        pass
    except:
        print ('Card._validate_face_value(Z) failed')

    #_validate_suit
    assert c1._validate_suit('S')==True
    try:
        assert c1._validate_face_value('Z')==False
    except ValueError:
        pass
    except:
        print ('Card._validate_face_value(Z) failed')

    #__validate_card_as_int
    c1._validate_card_as_int(18)==True
    try:
        assert c1._validate_card_as_int(118)==False
    except ValueError:
        pass
    except:
        print ('Card._validate_card_as_int(118) failed')

    c1 = Card('QS')
    assert str(c1)=='QS'
    c1 = Card('Q', 'S')
    assert str(c1)=='QS'
    c1 = Card('qs')
    assert str(c1)=='QS'
    c1 = Card('q', 's')
    assert str(c1)=='QS'

