# Quang Lam

import sys
import stack
import state
import nfastate
import streamreader
import orderedcollections

epsilon = "epsilon"

class NFA:
    def __init__(self,classes,states):
        self.states = states
        self.classes = classes

class DFA:
    def __init__(self, classes=orderedcollections.OrderedMap(), states=orderedcollections.OrderedMap()):
        self.classes = orderedcollections.OrderedMap(classes)
        self.states = orderedcollections.OrderedMap(states)
        self.numStates = len(states)


    def __repr__(self):
        return ("DFA(" + repr(self.classes) + "," + repr(self.states) + ")")


    def buildFromNFA(self,nfa):
        def newState():
            # Add a new state to the map of stateIds to states in the state map.
            # Return the new state id.
            newState = state.State(self.numStates)
            self.states[self.numStates] = newState
            self.numStates += 1
            return self.numStates - 1

        def getAcceptingTokenId(stateSet):
            # Return the first accepting tokenId found in the NFA state set. Otherwise, return None
            for stateId in stateSet:
                if nfa.states[stateId].isAccepting():
                    return nfa.states[stateId].getAcceptsTokenId()

            return None

        def EPSclosure(stateSet):
            closureSet = orderedcollections.OrderedSet(stateSet)
            # Add to the closure set all NFA state Ids that are
            # in the epsilon closure of this stateSet. Then
            # return the OrderedFrozenSet of this closure set.
            unexploredStates = orderedcollections.OrderedSet(stateSet)

            while len(unexploredStates) != 0:
                stateID = unexploredStates.pop()
                toStates = nfa.states[stateID].onClassGoTo(epsilon)

                for toStateID in toStates:
                    if toStateID not in unexploredStates:
                        closureSet.add(toStateID)
                        unexploredStates.add(toStateID)

            return orderedcollections.OrderedFrozenSet(closureSet)


        def nfaTransTo(fromStates, onClass):
            # return the epsilon closure of the set of NFA states that
            # you can get to on the class of characters (i.e. onClass) from
            # this set of fromStates.
            toStates = orderedcollections.OrderedSet()

            for fromStateID in fromStates:
                for toStateID in nfa.states[fromStateID].onClassGoTo(onClass):
                    toStates.add(toStateID)

            return orderedcollections.OrderedFrozenSet(EPSclosure(toStates))


        def gatherClasses(states):
            # return the set of classes of transitions (i.e. classes of characters)
            # that are possible transitions from this set of NFA states.
            gatheredClasses = orderedcollections.OrderedSet()

            for stateID in states:
                transitions = nfa.states[stateID].getTransitions()
                for onClass in transitions:
                    if onClass != epsilon:
                        gatheredClasses.add(onClass)

            return gatheredClasses

        # This is the beginning of the buildFromNFA method.
        # Copy over the classes
        self.classes = nfa.classes


        # Create the start state and the DFA to NFA stateMap.
        self.startStateId = newState()
        self.stateMap = orderedcollections.OrderedMap()

        # Form the epsilon closure of the NFA start state (i.e. state 0) and then
        # map the start state of the DFA to the start state set of the NFA


        # keep track of the new DFA states. The first new DFA state is the start
        # state. You can keep track of this as an ordered set or a stack if you wish.

        # map the set of nfa state ids (as a frozen set) to the new DFA state id in the
        # nfa2dfa map.


        # set the new DFA state to accepting if the NFA states contained an accepting state.
        # You can use the getAcceptingTokenId function for this.


        # While there are no more unexplored states in the new DFA state set, follow the algorithm
        # given on the website by using the nfaTransTo function and creating new DFA states for each
        # new set of NFA states that are found by using gatherClasses. Remember to set accepting states
        # in the DFA as you proceed.

        # Code goes here
        startDFASet = EPSclosure(orderedcollections.OrderedSet([self.startStateId]))
        self.stateMap[self.startStateId] = startDFASet
        if getAcceptingTokenId(startDFASet):
            self.states[self.startStateId].setAccepting(True)

        unexploredStates = orderedcollections.OrderedSet([self.startStateId])

        nfa2dfa = orderedcollections.OrderedMap()
        nfa2dfa[startDFASet] = self.startStateId

        while len(unexploredStates) > 0:
            currentStateID = unexploredStates.pop()
            classes = gatherClasses(self.stateMap[currentStateID])
            for onClass in classes:
                toSet = nfaTransTo(self.stateMap[currentStateID], onClass)
                if toSet not in nfa2dfa:
                    newDFAStateId = newState()
                    self.stateMap[newDFAStateId] = toSet
                    nfa2dfa[toSet] = newDFAStateId
                    if getAcceptingTokenId(toSet):
                        self.states[newDFAStateId].setAccepting(True)
                    unexploredStates.add(newDFAStateId)

                    self.states[currentStateID].addTransition(onClass, newDFAStateId)
                else:
                    dfaStateId = nfa2dfa[toSet]
                    self.states[currentStateID].addTransition(onClass, dfaStateId)



    # The writeListing method is provided assuming you used the correct data structures
    # in your code.

    def writeListing(self, outStream):

        outStream.write("The start state is: " + str(self.startStateId) + "\n\n")

        outStream.write("STATE     ON CLASS     GO TO     ACCEPTS\n")
        outStream.write("-----     --------     -----     -------\n")

        for stateId in range(self.numStates):
            if self.states[stateId].isAccepting():
                acceptsId = self.states[stateId].getAcceptsTokenId()
                tokenName = "yes"
            else:
                tokenName = ""

            outStream.write("%5d %34s\n"%(stateId,tokenName))

            trans = self.states[stateId].getTransitions()

            for onClass in trans:
                outStream.write("%18s     %5d\n"%(onClass,trans[onClass]))

            outStream.write("\n")


def main():

    classes = { epsilon: frozenset([]), "a": frozenset(["a"]) }

    q0 = nfastate.NFAState(0, True)
    q1 = nfastate.NFAState(1, True)
    q2 = nfastate.NFAState(2)
    q3 = nfastate.NFAState(3)
    q4 = nfastate.NFAState(4, True)
    q5 = nfastate.NFAState(5)
    q6 = nfastate.NFAState(6)
    q7 = nfastate.NFAState(7)
    q8 = nfastate.NFAState(8)

    q0.addTransition(epsilon, 1)
    q0.addTransition(epsilon, 4)

    q1.addTransition("a", 2)
    q2.addTransition("a", 3)
    q3.addTransition("a", 1)

    q4.addTransition("a", 5)
    q5.addTransition("a", 6)
    q6.addTransition("a", 7)
    q7.addTransition("a", 8)
    q8.addTransition("a", 4)

    states = { 
        0: q0,
        1: q1,
        2: q2,
        3: q3,
        4: q4,
        5: q5,
        6: q6,
        7: q7,
        8: q8
    }

    nfa = NFA(classes, states)

    dfa = DFA()
    dfa.buildFromNFA(nfa)
    dfa.writeListing(sys.stdout)

main()