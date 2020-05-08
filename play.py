class Play():

    def __init__(self):
        self._raw = []
        self.contract = ''
        self.declarer = ''  

    def append(self, value: 'Card'):
        self._raw.append(value)
