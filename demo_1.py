import streamreader
import state
import sys
import io


def main():

    s = input("please enter a string of 0's and 1's:")
    strm = streamreader.StreamReader(io.StringIO(s))

    q0 = state.State(0, True)
    q1 = state.State(1, True)
    q2 = state.State(2)
    
    classes = {}
    classes["0"] = set(["0"])
    classes["1"] = set(["1"])
    
    
    q0.addTransition("0",1)
    q0.addTransition("1",2)
    q1.addTransition("0",1)
    q1.addTransition("1",2)
    q2.addTransition("0",2)
    q2.addTransition("1",0)
    
    q0.setClasses(classes)
    q1.setClasses(classes)
    q2.setClasses(classes)
    
    accepted = False
    
    states = {0:q0, 1:q1, 2:q2}
    
    stateId = 0
    
    c = strm.readChar()
    
    while not strm.eof():
        print(c, stateId)
        # process character 
        q = states[stateId]
        stateId = states[stateId].onGoTo(c)     
    
        #state.NoTransition? Handle this?
        if stateId == state.NoTransition:
            print("rejected")
            return

        c = strm.readChar()

        
    if states[stateId].isAccepting():
        print("accepted")
    else:
        print("rejected")
    
    
    
    
if __name__ == "__main__":
    main()