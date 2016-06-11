# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for, flash, make_response, jsonify
from drawfsm import *
from lxml import etree
from forms import ContactForm
from flask.ext.mail import Message, Mail
#python 3 requires import from parse
from urllib.parse import unquote
import simplejson as json
import traceback
from xml.sax.saxutils import escape

# Initialize the Flask application
mail = Mail()

app = Flask(__name__)

app.secret_key = 'mega secret open source development key 008'

with open('conf.txt', 'r') as f:
    data = f.readlines()

app.config["MAIL_SERVER"] = data[2].strip()
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = data[0].strip()
app.config["MAIL_PASSWORD"] = data[1].strip()

#max word permitted
app.config["MAX_WORDS"] = 15

mail.init_app(app)

# This route will prompt a file download with the csv lines
@app.route('/export', methods=['POST'])
def export():

    scxml = request.form['scxml']
    document = etree.fromstring(scxml)
    dom = etree.parse(document)
    xslt = etree.parse("fsm_to_scxml.xsl")
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    print(etree.tostring(newdom, pretty_print=True))

    # We need to modify the response, so the first thing we 
    # need to do is create a response out of the CSV string
    response = make_response(dom)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=export.xml"
    return response

@app.route('/')
def form():
    return render_template('form_submit.html', maxwords=app.config["MAX_WORDS"])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender="simple.fsm@gmail.com", recipients=["simple.fsm@gmail.com"])
      try:
       #msg.body = ' '
        msg.body = """
        From: %s <%s>
        %s
        """ % (form.name.data, form.email.data, form.message.data)
        mail.send(msg)
      except Exception as e:
        #to tu je len aby mi to vypisalo rovno na stranke co nedjde
        print(e)
        traceback.print_exc()
        return render_template('invalidInput.html', error = e)
      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)


@app.route('/export_fsmxml')
def export_fsmxml():
    nodes = request.args['nodes']
    edges = request.args['edges']
    #Create a copy
    nodes = json.loads((nodes+'.')[:-1])
    edges = json.loads((edges+'.')[:-1])
    fsm = FSM()
    for stateId in nodes.keys():
        try:
            isFinal = nodes[stateId]['color']['background'] == '#33cc33'
        except:
            isFinal = False
        try:
            isInitial = nodes[stateId]['shape'] == 'diamond'
        except:
            isInitial = False
        if isFinal and not isInitial:
            type = 'f'
        elif isInitial and not isFinal:
            type = 'i'
        elif isFinal and isInitial:
            type = 'if'
        else:
            type = 'r'
        fsm.addState(stateId,nodes[stateId]['label'],type)
    for trans in edges:
        try:
            fsm.transitions[str(edges[trans]['from'])].append((edges[trans]['label'],str(edges[trans]['to'])))
        except:
            fsm.transitions[str(edges[trans]['from'])] = []
            fsm.transitions[str(edges[trans]['from'])].append((edges[trans]['label'],str(edges[trans]['to'])))
    print(fsm)
    print(fsm.getFsmXml())
    return jsonify(outputArea=escape(fsm.getFsmXml()))

@app.route('/export_scxml')
def export_scxml():

    nodes = request.args['nodes']
    edges = request.args['edges']
    #Create a copy
    nodes = json.loads((nodes+'.')[:-1])
    edges = json.loads((edges+'.')[:-1])
    fsm = FSM()

    for stateId in nodes.keys():
        try:
            isFinal = nodes[stateId]['color']['background'] == '#33cc33'
        except:
            isFinal = False
        try:
            isInitial = nodes[stateId]['shape'] == 'diamond'
        except:
            isInitial = False
        if isFinal and not isInitial:
            type = 'f'
        elif isInitial and not isFinal:
            type = 'i'
        elif isFinal and isInitial:
            type = 'if'
        else:
            type = 'r'
        fsm.addState(stateId,nodes[stateId]['label'],type)
    for trans in edges:
        try:
            fsm.transitions[str(edges[trans]['from'])].append((edges[trans]['label'],str(edges[trans]['to'])))
        except:
            fsm.transitions[str(edges[trans]['from'])] = []
            fsm.transitions[str(edges[trans]['from'])].append((edges[trans]['label'],str(edges[trans]['to'])))
  
    try:
        fsmString = fsm.getFsmXml()
        print(fsmString)
        dom = etree.fromstring(fsmString)
        xslt = etree.parse("fsm_to_scxml.xsl")
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        scxml = etree.tostring(newdom, pretty_print=True)
    except Exception as e:
        print(e)
    
    return jsonify(outputArea=escape(scxml.decode()))
    
    
@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/editor')
def editor():
    return render_template('editor.html')

@app.errorhandler(403)
def page_forbidden(e):
    print("page_forbidden")
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    print("page_not_found")
    return render_template('404.html'), 404

@app.errorhandler(410)
def page_gone(e):
    print("page_gone")
    return render_template('410.html'), 410

@app.errorhandler(500)
def internal_server_error(e):
    print("internal_server_error")
    return render_template('500.html'), 501

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/evaluate_fsm/', methods=['POST'])
def evaluate_fsm():
    fsm = FSM()
    out = ""
    scxml = request.form['scxml']
    schema = etree.parse("fsm_schema.xsd")
    xmlschema = etree.XMLSchema(schema)

    try:
        document = etree.fromstring(scxml)
        print("Parse complete!")
    except etree.XMLSyntaxError as e:
        print(e)
        return render_template('invalidInput.html', error = e)
        
    if not xmlschema.validate(document):
        #for error in xmlschema.error_log:
        #    print("ERROR ON LINE %s: %s" % (error.line, error.message.encode("utf-8")))
        return render_template('invalidInput.html', error = xmlschema.error_log.last_error)
        
    try:    
        fsm = parseFsmFromStringXml(scxml)
        edges = getEdgeIds(fsm)
        out = fsmIntoJavaScript(fsm, edges)
        
        words = request.form['words']
        transitionscripts = ""
        wordsDict = dict()
        wordCount = 0
        for word in words.splitlines():
            if wordCount == app.config["MAX_WORDS"]:
                break
            wordsDict[word] = fsm.calculate(word, ['resetgraph','displayedGraph','navbar'])
            transitionscripts += viewTransitionOnClickJs(word, edges, wordsDict[word])
            wordCount += 1
        resetgraph = viewTransitionOnClickJs('resetgraph', edges, (True, []))
    except Exception as e:
        print(e)
    return render_template('form_action.html', scxml=scxml, words=wordsDict, graphvis=out, transitionscripts=transitionscripts, resetgraph=resetgraph)

# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=int("5000")
  )