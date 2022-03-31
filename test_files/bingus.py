from test_files.bungus import Bungus

class Bingus(Bungus):
    
    def __init__(self, name):
        self.name = name

    def eat_chicken(self, cut):
        if cut == "breast":
            print("I'm eating chicken breast")
        elif cut == "wing":
            print("yeehaw")


def bingus_inspect(bingus):
    print("I'm a bingus")
    print("My name is {}".format(bingus.name))
    bingus.eat_chicken("breast")
    bingus.eat_chicken("wing")
    bingus.say_name()
