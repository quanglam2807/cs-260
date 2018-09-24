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
    q0 = state.State(0)
    q1 = state.State(1)
    q2 = state.State(2)
    q3 = state.State(3)
    q4 = state.State(4)
    q5 = state.State(5)
    q6 = state.State(6)
    q7 = state.State(7)
    q8 = state.State(8, True)
    q9 = state.State(9)
    q10 = state.State(10)
    q11 = state.State(11, True)
    q12 = state.State(12, True)
    q13 = state.State(13, True)
    q14 = state.State(14)
    
    classes = {}
    classes["a"] = set(["a"])
    classes["b"] = set(["b"])
    
    q0.addTransition("a", 1)
    q0.addTransition("b", 0)

    q1.addTransition("a", 2)
    q1.addTransition("b", 0)

    q2.addTransition("a", 3)
    q2.addTransition("b", 0)

    q3.addTransition("a", 4)
    q3.addTransition("b", 5)

    q4.addTransition("a", 4)
    q4.addTransition("b", 0)

    q5.addTransition("a", 6)
    q5.addTransition("b", 5)

    q6.addTransition("a", 7)
    q6.addTransition("b", 5)

    q7.addTransition("a", 8)
    q7.addTransition("b", 5)

    q8.addTransition("a", 9)
    q8.addTransition("b", 11)

    q9.addTransition("a", 9)
    q9.addTransition("b", 10)

    q10.addTransition("a", 9)
    q10.addTransition("b", 5)

    q11.addTransition("a", 12)
    q11.addTransition("b", 11)

    q12.addTransition("a", 13)
    q12.addTransition("b", 11)

    q13.addTransition("a", 14)
    q13.addTransition("b", 11)

    q14.addTransition("a", 14)
    q14.addTransition("b", 14)
    
    q0.setClasses(classes)
    q1.setClasses(classes)
    q2.setClasses(classes)
    q3.setClasses(classes)
    q4.setClasses(classes)
    q5.setClasses(classes)
    q6.setClasses(classes)
    q7.setClasses(classes)
    q8.setClasses(classes)
    q9.setClasses(classes)
    q10.setClasses(classes)
    q11.setClasses(classes)
    q12.setClasses(classes)
    q13.setClasses(classes)
    q14.setClasses(classes)
        
    states = {0: q0, 1: q1, 2: q2, 3: q3, 4: q4, 5: q5, 6: q6, 7: q7, 8: q8, 9: q9, 10: q10, 11: q11, 12: q12, 13: q13, 14: q14 }
    
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