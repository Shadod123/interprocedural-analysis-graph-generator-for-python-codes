class test ():
    x = 0
    
    def __init__(self):
        print('test')

    def bar(self, value):
        x = value
        print('bar')

t = test()
t.bar(5)