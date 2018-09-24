# Quang Lam
import streamreader
import state
import sys
import io

class FiniteStateMachine:
    def __init__(self, states, startStateId, classes):
        self.states = states
        self.startStateId = startStateId
        self.classes = classes

        for stateId in self.states:
            self.states[stateId].setClasses(classes)

    def accepts(self, strm):        
        stateId = 0
        
        c = strm.readChar()
        
        while not strm.eof():
            # print(c, stateId)
            # process character 
            q = self.states[stateId]
            stateId = q.onGoTo(c)


            #state.NoTransition? Handle this?
            if stateId == state.NoTransition:
                return False

            c = strm.readChar()

            
        if self.states[stateId].isAccepting():
            return True
        else:
            return False
    


def main():
    q0 = state.State(0, True)
    q1 = state.State(1, True)
    q2 = state.State(2, True)
    q3 = state.State(3, True)
    q4 = state.State(4)
    
    classes = {}
    classes["a"] = set(["a"])
    classes["b"] = set(["b"])
    
    q0.addTransition("a", 1)
    q0.addTransition("b", 0)

    q1.addTransition("a", 2)
    q1.addTransition("b", 1)

    q2.addTransition("a", 3)
    q2.addTransition("b", 2)

    q3.addTransition("a", 4)
    q3.addTransition("b", 3)

    q4.addTransition("a", 4)
    q4.addTransition("b", 4)
    
    q0.setClasses(classes)
    q1.setClasses(classes)
    q2.setClasses(classes)
    q3.setClasses(classes)
    q4.setClasses(classes)
        
    states = {0: q0, 1: q1, 2: q2, 3: q3, 4: q4 }
    
    dfa = FiniteStateMachine(states, 0, classes)


    while True:
        s = input("Please enter a string of a's and b's: ")
        if len(s) > 0:
            strm = streamreader.StreamReader(io.StringIO(s))
            
            if dfa.accepts(strm):
                print("That string is accepted by this finite state machine.")
            else:
                print("That string is not accepted.")
        else:
            print("Program Completed.")
            break

    
if __name__ == "__main__":
    main()