class Backpack(object):    #Part 1. constructor modification
    def __init__(self, name, color, max_size = 5):
        '''
        A Backpack object class. includes a name, a list of contents, a color, and maximum size for contents.

        Attributes:
             name (str) : the name of the backpack's owner.
             contents (list) : the contents of the backpack.
             color (str) : color of the backpack.
             max_size (int) : the maximum size of the backpack.
        '''
        self.name = name
        self.contents = []
        self.color = color
        self.max_size = max_size

    def put(self, item):    #modification of put() method
        if len(self.contents) >= self.max_size:
            print("No Room!")
        else:
            self.contents.append(item)

    def dump(self):    #reset contents to an empty list
        self.contents = []

#-----------------------------------------------------------------
#-----------------------------------------------------------------
test = Backpack("Saharnaz", "Gray")
for item in ["laptop", "mouse", "book", "pen", "pencil", "keys"]:
    test.put(item)
print("contents: ", test.contents)
#----------------------------------------------------------------
#----------------------------------------------------------------
test.dump()
print("contents: ", test.contents)
