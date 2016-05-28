#process xml and feed it into the fsm
#produce the vis.js script necessary to draw the graph
#
#example from visjs.org
#<script type="text/javascript">
#  // create an array with nodes
#  var nodes = new vis.DataSet([
#    {id: 1, label: 'Node 1'}, 
#    {id: 2, label: 'Node 2'},
#    {id: 3, label: 'Node 3'},
#    {id: 4, label: 'Node 4'},
#    {id: 5, label: 'Node 5'},
#    {id: 6, label: 'Node 6'},
#    {id: 7, label: 'Node 7'},
#    {id: 8, label: 'Node 8'}
#  ]);
#
#  // create an array with edges
#  var edges = new vis.DataSet([
#    {from: 1, to: 8, arrows:'to', dashes:true},
#    {from: 1, to: 3, arrows:'to'},
#    {from: 1, to: 2, arrows:'to, from'},
#    {from: 2, to: 4, arrows:'to, middle'},
#    {from: 2, to: 5, arrows:'to, middle, from'},
#    {from: 5, to: 6, arrows:{to:{scaleFactor:2}}},
#    {from: 6, to: 7, arrows:{middle:{scaleFactor:0.5},from:true}}
#  ]);
#
#  // create a network
#  var container = document.getElementById('mynetwork');
#  var data = {
#    nodes: nodes,
#    edges: edges
#  };
#  var options = {};
#  var network = new vis.Network(container, data, options);
#</script>


#import simple-fsm as SFSM
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
    print("getting edge ids")
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
    print(edges)
    return edges
                
    
def fsmIntoJavaScript(fsm, edges):
    #first, define the nodes
    output = "var nodes = new vis.DataSet([\n" 
    for (id,label,type) in fsm.states:
        highlight = ""
        if type == "f":
            highlight = ",color:{background:'#33cc33'}"
        elif type == "i":
            highlight = ",shape:'diamond'"
        elif type == "if":
            highlight = ",shape:'diamond',color:{background:'#33cc33'}"
        output += "{id:"+str(id)+",label:'"+label+"'"+highlight+"},\n"
    output = output[:-2] + "\n" #to remove the trailing comma   
    output += "]);\n"
    #then transitions
    output += "var edges = new vis.DataSet([\n"
    for (edgeId,stateId,finalNode,letters) in edges:
        output += "{id:"+edgeId+",from:" + stateId + ",to:"  + finalNode + ",arrows:'to',label:'" + letters +"'},\n"
    output = output[:-2] + "\n" 
    output += "]);\n"    
    output += """
var container = document.getElementById('displayedGraph');
var data = {
    nodes: nodes,
    edges: edges
};
var options = {};
var network = new vis.Network(container, data, options);"""
    print(output)
    return output
    
#edges: (edge id, starting state id, end state id, letters as a string e.g. 1,2,3,4)
def viewTransitionOnClickJs(word, edges,path):
    print(word)
    if path[0]:
        output = "$( \"#"+word+"\").click(function() {\n"
        for (eid,sid,fid,let) in edges:
            if (sid,fid) in path[1]:
                output += "edges.update({id:"+eid+",from:"+sid+",to:"+fid+",arrows:'to',label:'"+let+"',color:'green'});\n"
            else:
                output += "edges.update({id:"+eid+",from:"+sid+",to:"+fid+",arrows:'to',label:'"+let+"',color:'#2B7CE9'});\n"
        output += "});\n"
        print(output)
        return output
    else:
        return ""
    
def computeWord(fsm, word):
    return fsm.calculate(word)
    
    
    
    