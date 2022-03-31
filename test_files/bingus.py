from test_files.bungus import Bungus

class Bingus(Bungus):
    
    def __init__(self, name):
        self.name = name

    def eat_chicken(self, cut):
        if cut == "breast":
            print("I'm eating chicken breast")
        elif cut == "wing":
            print("yeehaw")
