def foo():
    print('foo')

def woo():
    print('woo')
    
class test ():
    x = 0
    
    def __init__(self):
        print('test')

    def bar(self, value):
        x = value
        print('bar')
        
    def baz(self):
        print('baz')
    
t = test()
array = [t.baz(), t.bar(5), foo(), woo()]
