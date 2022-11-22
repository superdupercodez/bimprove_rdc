
import sys

class Clunki():
    def __init__(self, **kwargs):
        print(kwargs['test'])
        
if __name__ == "__main__":
    clunk = Clunki(test=sys.argv[1])