#process xml and feed it into the fsm
#produce the vis.js script necessary to draw the graph
#
#example from visjs.org
#<script type="text/javascript">
#  // create an array with nodes
#  var nodes = new vis.DataSet([
#    {id: 1, label: 'Node 1'}, the label is program-generated, the label is gained from the 
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

def parseXmlFromString(document):
    #parse the xml and create an empty finite state machine
    root = ET.fromstring(document)
    fsm = FSM()
    for state in root.findall('state'):
        fsm.addState(int(state.get('id')),state.get('label'))
        for transition in state.findall('transition'):
            fsm.addTransition(int(state.get('id')),transition.get('under'),transition.text)
    return fsm
        
        
def intoJavascript(fsm):
    #first, define the nodes
    output = "var nodes = new vis.DataSet([\n"
    
    for (id,label) in fsm.states:
        output += "{id:"+str(id)+",label:'"+label+"'},\n"
    
    output = output[:-2] + "\n" #to remove the trailing comma
    
    output += "]);\n"
    
    #then transitions
    output += "var edges = new vis.DataSet([\n"
    
    for (id,label) in fsm.states:
        for (under,to) in fsm.transitions[id]:
            output += "{from:" + str(id) + ",to:"  + to + ",arrows:'to',label:'" + under +"'},\n"
   
    output = output[:-2] + "\n" 
    
    output += "]);\n"
    
    output += """var container = document.getElementById('mynetwork');
var data = {
    nodes: nodes,
    edges: edges
};
var options = {};
var network = new vis.Network(container, data, options);"""
    return output
    
    
    
    