class Constants:
    """
        A place to house generally useful stuff
        with no specific home
    """

    cardIntToStr = {  1: '2C', 2: '3C', 3: '4C', 4: '5C', 5: '6C', 6: '7C', 7: '8C', 8: '9C', 9: 'TC', 10: 'JC',
                     11: 'QC', 12: 'KC', 13: 'AC', 14: '2D', 15: '3D', 16: '4D', 17: '5D', 18: '6D', 19: '7D',
                     20: '8D', 21: '9D', 22: 'TD', 23: 'JD', 24: 'QD', 25: 'KD', 26: 'AD', 27: '2H', 28: '3H',
                     29: '4H', 30: '5H', 31: '6H', 32: '7H', 33: '8H', 34: '9H', 35: 'TH', 36: 'JH', 37: 'QH',
                     38: 'KH', 39: 'AH', 40: '2S', 41: '3S', 42: '4S', 43: '5S', 44: '6S', 45: '7S', 46: '8S',
                     47: '9S', 48: 'TS', 49: 'JS', 50: 'QS', 51: 'KS', 52: 'AS'}

    cardStrToInt = {'2C': 1, '3C': 2, '4C': 3, '5C': 4, '6C': 5, '7C': 6, '8C': 7, '9C': 8, 'TC': 9, 'JC': 10,
                    'QC': 11, 'KC': 12, 'AC': 13, '2D': 14, '3D': 15, '4D': 16, '5D': 17, '6D': 18, '7D': 19,
                    '8D': 20, '9D': 21, 'TD': 22, 'JD': 23, 'QD': 24, 'KD': 25, 'AD': 26, '2H': 27, '3H': 28,
                    '4H': 29, '5H': 30, '6H': 31, '7H': 32, '8H': 33, '9H': 34, 'TH': 35, 'JH': 36, 'QH': 37,
                    'KH': 38, 'AH': 39, '2S': 40, '3S': 41, '4S': 42, '5S': 43, '6S': 44, '7S': 45, '8S': 46,
                    '9S': 47, 'TS': 48, 'JS': 49, 'QS': 50, 'KS': 51, 'AS': 52}

    cardIntToSuit = {1: 'C', 2: 'C', 3: 'C', 4: 'C', 5: 'C', 6: 'C', 7: 'C', 8: 'C', 9: 'C', 10: 'C', 11: 'C',
                     12: 'C', 13: 'C', 14: 'D', 15: 'D', 16: 'D', 17: 'D', 18: 'D', 19: 'D', 20: 'D', 21: 'D',
                     22: 'D', 23: 'D', 24: 'D', 25: 'D', 26: 'D', 27: 'H', 28: 'H', 29: 'H', 30: 'H', 31: 'H',
                     32: 'H', 33: 'H', 34: 'H', 35: 'H', 36: 'H', 37: 'H', 38: 'H', 39: 'H', 40: 'S', 41: 'S',
                     42: 'S', 43: 'S', 44: 'S', 45: 'S', 46: 'S', 47: 'S', 48: 'S', 49: 'S', 50: 'S', 51: 'S', 52: 'S'}

    facevalues = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
    suits = ['C','D','H','S']
    all_cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
                 45, 46, 47, 48, 49, 50, 51, 52]

    bid_rank = {'1C': 1, '1D': 2, '1H': 3, '1S': 4, '1N': 5, '2C': 6, '2D': 7, '2H': 8, '2S': 9, '2N': 10,
                '3C': 11, '3D': 12, '3H': 13, '3S': 14, '3N': 15, '4C': 16, '4D': 17, '4H': 18, '4S': 19,
                '4N': 20, '5C': 21, '5D': 22, '5H': 23, '5S': 24, '5N': 25, '6C': 26, '6D': 27, '6H': 28,
                '6S': 29, '6N': 30, '7C': 31, '7D': 32, '7H': 33, '7S': 34, '7N': 35}

    double  = 'D'
    redouble = 'R'
    pass_ = 'P'
    is_not_suit_bid = [double, redouble, pass_,]    
    

  
