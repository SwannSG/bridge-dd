class EvenNumber:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, type=None) -> object:
        return obj.__dict__.get(self.name) or 0

    def __set__(self, obj, value) -> None:
        if self.name in obj.__dict__:
            # has already been set
            if not obj.__dict__[self.name]:
                obj.__dict__[self.name] = value
        else:
            # initialise
            obj.__dict__[self.name] = 0

class OneShotString:
    def __set_name__(self, owner, name):    
        self.name = name

    def __get__(self, obj, type=None) -> object:
        return obj.__dict__.get(self.name) or ''

    def __set__(self, obj, value) -> None:
        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = value




class Values:
    _value1 = OneShotString()

    def method(self):
         self._value1 = 'DOG'   

class T:

    def __init__(self):
        self.x = ''

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        print ('value: %s, type: %s' % (value, type(value)) )
        print (self.__dict__)
        print (dir(self))
        if '_x' in self.__dict__:
            print ('_x is in')
            if not self._x:
                self._x = value
        else:
            print ('_x is out')
            self._x = value

#x = Values()
#x.method()
a = T()






