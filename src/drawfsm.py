#process xml and feed it into the fsm
#produce the vis.js script necessary to draw the graph
from simple_fsm import *
import xml.etree.ElementTree as ET

def parseFsmFromStringXml(document):
    #parse the xml and create an empty finite state machine
    root = ET.fromstring(document)
    newfsm = FSM()
    i=0
    for state in root.findall('state'):
        if not i:
            type = str(state.get('type'))
            if type == "r":
                type = "i"
            elif type == "f":
                type = "if"
            newfsm.addState(str(state.get('id')),state.get('label'),type)
            i+=1
        else:
            newfsm.addState(str(state.get('id')),state.get('label'),str(state.get('type')))    
        for transition in state.findall('transition'):
            newfsm.addTransition(str(state.get('id')),transition.get('under'),transition.text)
                   
    return newfsm
        
def serializeLetters(input):
    output = ""
    for i in input:
        output += str(i) + ","
    return output[:-1]
    
def getEdgeIds(fsm):
    edgeId = 0
    edges = []
    for (id,label,_) in fsm.states:
        toTrans = dict()
        for (under,to) in fsm.transitions[id]:
            try:
                toTrans[to].append(under)
            except:
                toTrans[to] = []
                toTrans[to].append(under)
        for finalNode in toTrans.keys():
            edges.append((str(edgeId),str(id),finalNode,serializeLetters(toTrans[finalNode])))
            edgeId += 1
    return edges
                
    
def fsmIntoJavaScript(fsm, edges):
    #first, define the 
    if len(fsm.states) == 0:
        output = "\tvar nodes = new vis.DataSet();\n"
    else:     
        output = "\tvar nodes = new vis.DataSet([\n" 
        for (id,label,type) in fsm.states:
            highlight = ""
            if type == "f":
                highlight = ",color:{background:'#33cc33'}"
            elif type == "i":
                highlight = ",shape:'diamond'"
            elif type == "if":
                highlight = ",shape:'diamond',color:{background:'#33cc33'}"
            output += "\t\t{id:"+str(id)+",label:'"+label+"'"+highlight+"},\n"
        output = output[:-2] + "\n" #to remove the trailing comma   
        output += "\t]);\n"
    #then transitions
    if len(edges) == 0:
        output += "\tvar edges = new vis.DataSet();\n"
    else: 
        output += "\tvar edges = new vis.DataSet([\n"
        for (edgeId,stateId,finalNode,letters) in edges:
            output += "\t\t{id:"+edgeId+",from:" + stateId + ",to:"  + finalNode + ",arrows:'to',label:'" + letters +"'},\n"
        output = output[:-2] + "\n" 
        output += "\t]);\n"    
    output += """
\tvar container = document.getElementById('displayedGraph');
\tvar data = {
\t\tnodes: nodes,
\t\tedges: edges
\t};
\tvar options = {};
\tvar network = new vis.Network(container, data, options);"""
    return output
    
#edges: (edge id, starting state id, end state id, letters as a string e.g. 1,2,3,4)
def viewTransitionOnClickJs(word, edges, path):
    if path[0]:
        output = "\t$( \"#"+word+"\").click(function() {\n"
        for (eid,sid,fid,let) in edges:
            if (sid,fid) in path[1] and word != "resetgraph":
                output += "\t\tedges.update({id:"+eid+",from:"+sid+",to:"+fid+",arrows:'to',label:'"+let+"',color:'green'});\n"
            else:
                output += "\t\tedges.update({id:"+eid+",from:"+sid+",to:"+fid+",arrows:'to',label:'"+let+"',color:'#2B7CE9'});\n"
        output += "\t});\n"
        return output
    else:
        return ""
    
def computeWord(fsm, word):
    return fsm.calculate(word, ['resetgraph','displayedGraph','navbar'])
    
    
    
    