# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
from drawfsm import *
from lxml import etree

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/help')
def help():
    return render_template('help.html')

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
        
    fsm = parseFsmFromStringXml(scxml)
    out = fsmIntoJavaScript(fsm)
    
    words = request.form['words']
    transitionscripts = ""
    wordsDict = dict()
    for word in words.splitlines():
        transitionscripts += viewTransitionOnClickJs(word, fsm)
        wordsDict[word] = fsm.calculate(word)
    print('Rendering template')
    return render_template('form_action.html', scxml = scxml, words = wordsDict, graphvis = out, transitionscripts = transitionscripts )

# Run the app :)
if __name__ == '__main__':
  app.run( 
        host="0.0.0.0",
        port=int("5000")
  )
