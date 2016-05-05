#simple-fsm main evaluation module (class and function definitions)

class FSM:

    alphabet = set()
    states = set()
    transitions = dict()
    
    def addState(self, id, label):
        self.states.add((id,label))
        self.transitions[id] = []
        
    def addTransition(self, stateId, under, to):
        self.transitions[stateId].append((under,to))
        
    def calculate(self, word):
        pass
        
    
    