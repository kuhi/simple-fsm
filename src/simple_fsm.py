#simple-fsm main evaluation module  (class and function definitions)

#Internal representation of the automaton
class FSM:

    #Construct the Automaton
    def __init__(self):
        self.alphabet = set()
        self.states = set()
        self.transitions = dict()
        self.initial = "0"
        self.final = set()
    
    #String representation of the automaton, mainly for debugging
    def __str__(self):
        out = ""
        out += "Alphabet: " + str(self.alphabet) + "\n"
        out += "States: " + str(self.states) + "\n"
        out += "Transitions: " + str(self.transitions) + "\n"
        out += "Initial state: " + str(self.initial) + "\n"
        out += "Final states: " + str(self.final) + "\n"
        return out
    
    #Insert a new state into the Automaton.
    #The format is derived from the FSMXML element 'state'
    #'id' - id of the state in the FSMXML doc,
    #'label', 
    #'type' - regular or final (or initial)
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
    
    #Insert a new transition into the Automaton:
    #-from 'stateId' under 'under' to 'to'
    def addTransition(self, stateId, under, to):
        print('adding' + stateId + under + to)
        self.alphabet.add(under)
        self.transitions[stateId].append((under,to))
    
    #Transition from 'stateId' under 'letter' on this Automaton    
    def transition(self, stateId, letter):
        newstate = "-1"
        if stateId in self.transitions.keys():
            destinations = self.transitions[stateId]
            for (under, to) in destinations:
                if under == letter:
                    newstate = to
                    break
            return newstate
        else:
            return "-1"
    
    #Calculate a word on this Automaton
    def calculate(self, word, disallowedWords = None):
        if word in disallowedWords:
            return (False, "Disallowed word!")
        newstate = self.initial #To allow empty word (newline)
        state = self.initial
        trans = set()
        if set(word).issubset(self.alphabet):
            for letter in word:
                newstate = self.transition(state, letter)
                trans.add((state,newstate))
                state = newstate
            if str(newstate) in self.final:
                return (True, trans)
            else:
                return (False, "Word didn't reach a final state.")
        else:
            return (False, "Invalid letter found.")
    
    #Return this Automaton in the FSMXML format (native)        
    def getFsmXml(self):
        xml = "<fsm>\n"
        type = ""
        for state in self.states:
            if state[0] == self.initial:
                if state[2] == "if":
                    type = "f"
                else:
                    type = "r"
                xml += "    <state id=\"" + state[0] + "\" label=\"" + state[1] + "\" type=\"" + type + "\">\n"
                for transition in self.transitions[state[0]]:
                    xml += "        <transition under=\"" + transition[0] + "\">" + transition[1] + "</transition>\n"
                xml += "    </state>\n" 
                break
            
        for state in self.states:
            if state[0] == self.initial:
                continue
            xml += "    <state id=\"" + state[0] + "\" label=\"" + state[1] + "\" type=\"" + state[2] + "\">\n"
            for transition in self.transitions[state[0]]:
                xml += "        <transition under=\"" + transition[0] + "\">" + transition[1] + "</transition>\n"
            xml += "    </state>\n"        
        xml += "</fsm>"
        return xml
    
    