#simple-fsm main evaluation module (class and function definitions)

class TransitionException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class FSM:

    alphabet = set()
    states = set()
    transitions = dict()
    initial = 0
    final = set()
    
    def addState(self, id, label, type = "r"):
        self.states.add((id,label,type))
        if type == "if":
            self.initial = id
            self.final.add(id)
        if type == "i":
            self.initial = id
        if type == "f":
            self.final.add(id)        
        self.transitions[id] = []
        
    def addTransition(self, stateId, under, to):
        self.alphabet.add(under)
        self.transitions[stateId].append((under,to))
        
    def transition(self, stateId, letter):
        newstate = 0
        if stateId in self.transitions.keys():
            destinations = self.transitions[stateId]
            for (under, to) in destinations:
                if under == letter:
                    newstate = to
                    break
            return newstate
        else:
            return 0

    def calculate(self, word):
        state = self.initial
        if set(word).issubset(self.alphabet):
            for letter in word:
                state = self.transition(state, letter)
            return int(state) in self.final
        else:
            return False
            
        
    
    