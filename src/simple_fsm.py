#simple-fsm main evaluation module  (class and function definitions)

class FSM:

    def __init__(self):
        self.alphabet = set()
        self.states = set()
        self.transitions = dict()
        self.initial = "0"
        self.final = set()
    
    def __str__(self):
        out = ""
        out += "Alphabet: " + str(self.alphabet) + "\n"
        out += "States: " + str(self.states) + "\n"
        out += "Transitions: " + str(self.transitions) + "\n"
        out += "Initial state: " + str(self.initial) + "\n"
        out += "Final states: " + str(self.final) + "\n"
        return out
    
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
        newstate = "-1"
        print("Transitioning from " + str(stateId) + " under " + str(letter))
        if stateId in self.transitions.keys():
            destinations = self.transitions[stateId]
            for (under, to) in destinations:
                if under == letter:
                    newstate = to
                    break
            print("Transitioned to " + newstate)
            return newstate
        else:
            return "-1"

    def calculate(self, word):
        state = self.initial
        if set(word).issubset(self.alphabet):
            for letter in word:
                state = self.transition(state, letter)
            if str(state) in self.final:
                print("OK")
                return (True, "Word reached a final state.")
            else:
                print("NOK")
                return (False, "Word didn't reach a final state.")
        else:
            return (False, "Invalid letter found.")
            
        
    
    