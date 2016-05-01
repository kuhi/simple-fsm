from flask import Flask
app = Flask(__name__)

@app.route('/')
def main_fsm():
    return 'Welcome to simple-fsm'

if __name__ == '__main__':
    app.run()