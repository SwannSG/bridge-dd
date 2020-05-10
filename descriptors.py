"""
    OneShotDescriptor is not used.
    Proving to be unreliable and needs more work.
"""
class OneShotDesciptor:
    """
        Allows a property of a class to be set only once.
        Once-set the property becomes effectively read only
        usage:
            class Abc
                value1 = OneShotDescriptor()
            a = Abc()
            a.value1 = 'cat'
            a.value1  # cat
    """
    def __set_name__(self, owner, name):
        # sets the name of the property on the object
        self.name = name

    def __get__(self, obj, type=None) -> object:
        return obj.__dict__.get(self.name) or ''

    def __set__(self, obj, value) -> None:
        if self.name in obj.__dict__:
            # has already been set
            if not obj.__dict__[self.name]:
                obj.__dict__[self.name] = value
            else:
                raise AttributeError('Once %s is set, it becomes read-only' % self.name)
        else:
            # initialise
            obj.__dict__[self.name] = ''


if __name__  == '__main__':
    class Abc:
        value1 = OneShotDesciptor()

    a = Abc()


    assert a.value1 == ''
    a.value1 = 'cat'
    assert a.value1 == 'cat', 'a.value1 should be "cat"'
    try:
        a.value1 = 'dog'    # should throw an error
    except AttributeError:
        print ('test passed - descriptors.OneShotDescriptor')
    except:
        print ('test failed - descriptors.OneShotDescriptor')
