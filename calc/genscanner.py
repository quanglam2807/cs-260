import streamreader
import state
from orderedcollections import *

class Scanner:
    def __init__(self, instream = None, startStateId = None, states={}, classes={}, keywords = {}, identifierTokenId = -1, eatComments = False, commentTokenId = -1):
        # The use of dict below creates a copy of the default parameter because
        # only one copy of default parameters is created and if multiple scanner
        # objects were created this would be a problem... for Python...
        self.states = dict(states)
        self.classes = dict(classes)
        self.startStateId = startStateId
        self.reader = streamreader.StreamReader(instream)
        self.keywords = dict(keywords)
        self.identiferTokenId = identifierTokenId
        self.eatComments = eatComments
        self.commentTokenId = commentTokenId
        for stateId in states:
            states[stateId].setClasses(classes)

    def getToken(self):

        # Here the getToken method must skip whitespace and then run the finite state machine starting with self.startStateId.
        # The finite state machine is an infinite loop of getting characters from the reader and transitioning between states.
        # The getToken method returns a tuple of (tokenId, lex) where tokenId is the token Identifier from the state or from the
        # map of keywords if the lexeme is in the keyword map.
        # If a transition is not found, then an exception can be raised like this.
        # raise Exception("Bad Token '"+lex+"' found at line " + str(self.reader.getLineNumber()) + " and column " + str(self.reader.getColNumber()) + ".")

        # When you call the onGoTo method of the state class, you'll have to pass in the ord(c) where
        # c is the character you read from the StreamReader object self.reader. This is necessary because
        # the transitions in the calscanner.py are on the ASCII equivalents of the characters and
        # not the actual characters themselves. This is because some characters are unprintable.
        pass
