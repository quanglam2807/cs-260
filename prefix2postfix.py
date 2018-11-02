# Quang Lam

import streamreader
import io

class SubtractionNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return " ".join([self.left.eval(), self.right.eval(), '-'])


class AdditionNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return " ".join([self.left.eval(), self.right.eval(), '+'])

class MultiplicationNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return " ".join([self.left.eval(), self.right.eval(), '*'])

class DividationNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return " ".join([self.left.eval(), self.right.eval(), '/'])

class NumberNode:
    def __init__(self, num):
        self.num = int(num)
    
    def eval(self):
        return str(self.num)

def LL1(reader):
    token = reader.getToken()

    if token == '-':
        return SubtractionNode(LL1(reader), LL1(reader))
    
    if token == '+':
        return AdditionNode(LL1(reader), LL1(reader))

    if token == '*':
        return MultiplicationNode(LL1(reader), LL1(reader))

    if token == '/':
        return DividationNode(LL1(reader), LL1(reader))
    
    return NumberNode(token)
    

def main():
    while True:
        expression = input("Please enter a prefix expression (or press enter to stop): ")

        if len(expression) < 1:
            return
          
        reader = streamreader.StreamReader(io.StringIO(expression))

        postfix = LL1(reader)
        print("The postfix form is:", postfix.eval())

        
        

if __name__ == "__main__":
    main()