# Quang Lam

# Here is the output from running this.
# Kent's Mac> python3 dfa2mindfa.py
# The MINIMAL DFA CREATED FOR THE REGULAR EXPRESSIONS IS:

# The start state is: 0

# STATE     ON CLASS     GO TO     ACCEPTS
# -----     --------     -----     -------
#     0
#                  a         2

#     1                                yes
#                  a         2

#     2
#                  b         4

#     3
#                  a         1

#     4
#                  b         3

import state
import orderedcollections
import sys


class DFA:
    def __init__(self, classes, states, startStateId):
        self.classes = classes
        self.states = states
        self.startStateId = startStateId

class MinimalDFA:
    def __init__(self):
        self.classes = orderedcollections.OrderedMap()
        self.states = orderedcollections.OrderedMap()
        self.numStates = 0

    def buildFromDFA(self,dfa):
        def newState():
            aState = state.State(self.numStates)
            self.states[self.numStates] = aState
            self.numStates+=1
            return self.numStates-1

        # Returns the Minimized DFA Partition Id given
        # a DFA State and Input symbol class.
        def transToMinPartition(fromDFAStateId, onClass):
            toStateId = dfa.states[fromDFAStateId].onClassGoTo(onClass)
            if toStateId < 0:
                return -1
            return self.dfa2min[toStateId]

        # Returns an ordered set of all the character classes
        # of all DFA states in a minimized DFA partition.
        def onClasses(minStateId):
            minClasses = orderedcollections.OrderedSet()
            for stateId in self.min2dfa[minStateId]:
                for onClass in self.classes:
                    if dfa.states[stateId].hasTransition(onClass):
                        minClasses.add(onClass)
            return minClasses

        def finer(minStateId):
            #(********************************************************************************)
            #(* Check each node in the given partition (the one passed as a parameter)       *)
            #(* with the first node in the partition. If a node is found that transitions    *)
            #(* to a different partition than the first node on the same input make a new    *)
            #(* set with this node and put all subsequent nodes that don't have similar      *)
            #(* transitions to the first node into this new set. After going through all     *)
            #(* states, if the new set of distinquished states is not empty then create a    *)
            #(* new partition and then remove all states in the set from the current         *)
            #(* partition and add them to the new partion (i.e. minimal state). Return true  *)
            #(* if a new partition was created and false otherwise. Aho, Sethi, Ullman p. 142*)
            #(********************************************************************************)
            distinguishedStates = orderedcollections.OrderedSet()

            partition = self.min2dfa[minStateId]
            
            firstStateId = next(iter(partition))

            for onClass in onClasses(minStateId):
                goTo = transToMinPartition(firstStateId, onClass)
                for stateId in partition:
                    if stateId != firstStateId and transToMinPartition(stateId, onClass) != goTo:
                        distinguishedStates.add(stateId)

            if len(distinguishedStates) < 1:
                return False

            for stateId in distinguishedStates:
                self.min2dfa[minStateId].remove(stateId)

            minStateId = newState()
            self.min2dfa[minStateId] = distinguishedStates
            for stateId in distinguishedStates:
                self.dfa2min[stateId] = minStateId

            return True


        # Run through all the states and make transitions
        # in the minimized DFA for all transitions that existed
        # in the unminimized DFA. Also sets the state to be accepting
        # if any state in the unminimized DFA was accepting.
        def constructMinStateTransitions():
            for minStateId in self.states:
                minState = self.states[minStateId]

                # Find the first dfa stateid in the set
                dfaStateIds = list(self.min2dfa[minStateId])
                dfaStateIds.sort()
                dfaStateId = dfaStateIds[0]

                if dfa.states[dfaStateId].isAccepting():
                    minState.setAccepting(dfa.states[dfaStateId].getAcceptsTokenId())
                minState.transitions = {}

                trans = dfa.states[dfaStateId].getTransitions()
                for onClass in trans:
                    toDFAStateId = trans[onClass]
                    dfaState = dfa.states[toDFAStateId]
                    toStateId = self.dfa2min[toDFAStateId]
                    minState.addTransition(onClass,toStateId)


            self.startStateId = self.dfa2min[dfa.startStateId]

        self.classes = dfa.classes


        startStateId = newState()
        self.min2dfa = orderedcollections.OrderedMap()
        self.dfa2min = orderedcollections.OrderedMap()

        self.min2dfa[startStateId] = orderedcollections.OrderedSet()

        # Build state sets. One with all
        # the non-final states in it, and one
        # for each accepting state of the dfa
        # since we want separate accepting states
        # for all the tokens of the dfa.

        for stateId in dfa.states:
            dfaState = dfa.states[stateId]

            if not dfaState.isAccepting():
                self.min2dfa[startStateId].add(stateId)
                self.dfa2min[stateId] = startStateId
            else:
                # Now we have to either add another partition (i.e. state) or
                # find the accepting state that this dfa state belongs to.

                found = False

                for minStateId in self.states:
                    minState = self.states[minStateId]
                    if minState.getAcceptsTokenId() == dfaState.getAcceptsTokenId():
                        self.min2dfa[minStateId].add(stateId)
                        self.dfa2min[stateId] = minStateId
                        found = True


                if not found:
                    finalStateId = newState()
                    self.min2dfa[finalStateId] = orderedcollections.OrderedSet([stateId])
                    self.dfa2min[stateId] = finalStateId
                    self.states[finalStateId].setAccepting(dfaState.getAcceptsTokenId())

        self.startStateId = self.dfa2min[dfa.startStateId]

        # Now begin partitioning by finding distinguishable states
        # You must write code here to repeatedly call finer on all states
        # of the minimized DFA until no more changes can be made.

        changed = True
        while changed:
            changed = False
            for minStateId in range(self.numStates):
                if finer(minStateId):
                    changed = True


        # WRITE THE CODE DESCRIBED ABOVE HERE.


        # After we are done splitting the states we call constructMinStateTransitions
        # to build the transitions in the new states.
        constructMinStateTransitions()

    def writeListing(self, outStream):

        outStream.write("The MINIMAL DFA CREATED FOR THE REGULAR EXPRESSIONS IS:\n\n")

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

    classes = {"a":frozenset(['a']), "b": frozenset(['b'])}

    q0 = state.State(0)
    q1 = state.State(1)
    q2 = state.State(2)
    q3 = state.State(3)
    q4 = state.State(4,1)
    q5 = state.State(5)
    q6 = state.State(6)



    q0.addTransition("a", 1)
    q1.addTransition("b", 2)
    q2.addTransition("b", 3)
    q3.addTransition("a", 4)
    q4.addTransition("a", 5)
    q5.addTransition("b", 6)
    q6.addTransition("b", 3)


    states = {0:q0, 1:q1, 2:q2, 3:q3, 4:q4, 5:q5, 6:q6}

    dfa = DFA(classes, states, 0)

    mindfa = MinimalDFA()
    mindfa.buildFromDFA(dfa)
    mindfa.writeListing(sys.stdout)


main()