#simple-fsm main evaluation module  (class and function definitions)

class TransitionException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class FSM:

    alphabet = set()
    states = set()
    transitions = dict()
    initial = "0"
    final = set()
    
    def addState(self, id, label, type = "r"):
        self.states.add((id,label,type))
        if type == "if":
            self.initial = str(id)
            self.final.add(str(id))
        if type == "i":
            self.initial = str(id)
        if type == "f":
            self.final.add(str(id))        
        self.transitions[str(id)] = []
        
    def addTransition(self, stateId, under, to):
        self.alphabet.add(under)
        self.transitions[stateId].append((under,to))
        
    def transition(self, stateId, letter):
        newstate = "0"
        print("transitioning from " + str(stateId) + " under " + str(letter))
        if stateId in self.transitions.keys():
            destinations = self.transitions[stateId]
            for (under, to) in destinations:
                if under == letter:
                    newstate = to
                    break
            print("transitioned to " + newstate)
            return newstate
        else:
            return "0"

    def calculate(self, word):
        print(self.alphabet)
        print(self.states)
        print(self.transitions)
        print(self.initial)
        print(self.final)
        state = self.initial
        if set(word).issubset(self.alphabet):
            for letter in word:
                state = self.transition(state, letter)
            return str(state) in self.final
        else:
            return False
            
        
    
    