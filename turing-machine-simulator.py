# Quang Lam

class Tape:
    def __init__(self, inputStr = ''):
        # 100 or so
        self.tape = [' '] * 50 + list(inputStr) + [' '] * 50

        self.location = 50

    def moveLeft(self):
        if self.location == 0:
            self.location = len(self.tape) - 1
            self.tape = [' '] * len(self.tape) + self.tape
        else:
            self.location -= 1
    
    def moveRight(self):
        if self.location == len(self.tape) - 1:
            self.location = len(self.tape)
            self.tape = self.tape + [' '] * len(self.tape)
        else:
            self.location += 1

    def write(self, symbol):
        self.tape[self.location] = symbol
    
    def read(self):
        return self.tape[self.location]

    def __str__(self):
        return '|' + '|'.join([symbol for symbol in self.tape if symbol != ' ']) + '|'

def main():    
    transitions = {
        (0, '$'): (1, '$', 'R'),

        (1, 'r'): (1, 'r', 'R'),
        (1, 'e'): (1, 'e', 'R'),
        (1, 'v'): (1, 'v', 'R'),
        (1, 's'): (1, 's', 'R'),
        (1, 'x'): (2, 'x', 'L'),
        (1, '$'): (2, '$', 'L'),

        # get right most character
        (2, 'r'): (3, 'x', 'R'), # Mark x as done
        (2, 'e'): (4, 'x', 'R'), 
        (2, 'v'): (5, 'x', 'R'),
        (2, 's'): (6, 'x', 'R'),
        (2, '$'): (8, ' ', 'R'),

        # write r
        (3, 'r'): (3, 'r', 'R'),
        (3, 'e'): (3, 'e', 'R'),
        (3, 'v'): (3, 'v', 'R'),
        (3, 's'): (3, 's', 'R'),
        (3, '$'): (3, '$', 'R'),
        (3, 'x'): (3, 'x', 'R'),
        (3, ' '): (7, 'r', 'L'),

        # write e
        (4, 'r'): (4, 'r', 'R'),
        (4, 'e'): (4, 'e', 'R'),
        (4, 'v'): (4, 'v', 'R'),
        (4, 's'): (4, 's', 'R'),
        (4, '$'): (4, '$', 'R'),
        (4, 'x'): (4, 'x', 'R'),
        (4, ' '): (7, 'e', 'L'),

        # write v
        (5, 'r'): (5, 'r', 'R'),
        (5, 'e'): (5, 'e', 'R'),
        (5, 'v'): (5, 'v', 'R'),
        (5, 's'): (5, 's', 'R'),
        (5, '$'): (5, '$', 'R'),
        (5, 'x'): (5, 'x', 'R'),
        (5, ' '): (7, 'v', 'L'),

        # write s
        (6, 'r'): (6, 'r', 'R'),
        (6, 'e'): (6, 'e', 'R'),
        (6, 'v'): (6, 'v', 'R'),
        (6, 's'): (6, 's', 'R'),
        (6, '$'): (6, '$', 'R'),
        (6, 'x'): (6, 'x', 'R'),
        (6, ' '): (7, 's', 'L'),

        # go back to start
        (7, 'r'): (7, 'r', 'L'),
        (7, 'e'): (7, 'e', 'L'),
        (7, 'v'): (7, 'v', 'L'),
        (7, 's'): (7, 's', 'L'),
        (7, '$'): (7, '$', 'L'),
        (7, 'x'): (7, 'x', 'L'),
        (7, ' '): (0, ' ', 'R'),

        # clean up
        (8, 'r'): (8, 'r', 'R'),
        (8, 'e'): (8, 'e', 'R'),
        (8, 'v'): (8, 'v', 'R'),
        (8, 's'): (8, 's', 'R'),
        (8, '$'): (8, '$', 'R'),
        (8, 'x'): (8, ' ', 'R'),
        (8, ' '): (9, '$', 'R'),

        (9, ' '): (9, ' ', None),
    }

    finalStates = [9]

    while True:
        inputStr = raw_input('Please enter a string (leave blank to exit): ')
        if len(inputStr) < 1: break
        tape = Tape(inputStr)

        state = 0
        while True:
            ch = tape.read()
            state, symbol, direction = transitions[(state, ch)]

            tape.write(symbol)

            if direction == 'R':
                tape.moveRight()
            if direction == 'L':
                tape.moveLeft()

            if state in finalStates:
                break

        print(tape)

if __name__ == "__main__":
    main()