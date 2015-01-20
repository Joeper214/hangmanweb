from flask import Flask
app = Flask (__name__)
from flask import request
from flask import render_template

@app.route('/')
def login(name = None):

    return render_template('login.html', name = None)



@app.route('/register')
def register(name1=None):
    return render_template('reg.html', name1 = None)

@app.route('/index')
def index(name2 = None):
    return render_template('index.html')

@app.route('/leadscore')
def leadscore(name3 = None):
    return render_template('leadscore.html')

@app.route('/game')
def game(name4 = None):
    return render_template('game.html')

if __name__ == "__main__":
    app.run(debug=True)
