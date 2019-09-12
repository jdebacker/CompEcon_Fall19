class Backpack(object):
    '''
    A Backpack object class.
    Attributes and details in problem 1
    '''
    def __init__(self, name, color, max_size = 5):
        self.name = name
        self.color = color
        self.max_size = max_size
        self.contents = []

    def put(self, item):    #modification of put() method
        if len(self.contents) >= self.max_size:
            print("No Room!")
        else:
            self.contents.append(item)

    def dump(self):    #reset contents to an empty list
        self.contents = []
#-----------------------------------------------------------------
#-----------------------------------------------------------------
class Jetpack(Backpack):
    """
    A Jetpack object class. Inherited from Backpack class.
    A Jetpack is smaller than a Backpackself.

    Attributes:
        name (str): the name of the Jetpack's owner.
        color (str): color of Jetpack
        max_size (int): maximum number of items that can be fit inside the Jetpack
        fuel (int):
        contents (list): the contents of the Jetpack
    """
    def __init__(self, name, color, max_size = 2, fuel =10):
        Backpack.__init__(self, name, color, max_size)
        self.fuel = fuel

    def fly(self, burned_fuel):
        self.burned_fuel = burned_fuel
        if self.burned_fuel <= self.fuel:
            self.fuel = self.fuel - self.burned_fuel
        if self.burned_fuel > self.fuel:
            self.fuel = self.fuel
            print("Not Enough Fuel!")
    def dump(self):
        Backpack.dump(self)
        self.fuel = 0

#-----------------------------------------------------------------
#-----------------------------------------------------------------
test = Jetpack("Saharnaz", "White")
test.put("calculator")
print(test.contents, test.fuel)
test.dump()
print(test.contents, test.fuel)
