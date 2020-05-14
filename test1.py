class A:
    def __init__(self):
        self.x = 'zx'
        self.v = 0

    def __lt__(self, other:'CardForRound') -> bool:
        if self.v < other.v:
            return True
        return False

    def __repr__(self):
        return '%s%s'% (self.x, self.v)

a = A()
a.v = 10
b = A()
b.v = 11
c = A()
c.v = 12
d = A()
d.v = 13

l = [a,b,c,d]
