from flask import Flask, request, render_template, session, redirect, url_for, escape
from firebase import firebase
import urllib2
import json

guess = ''
score = 0
level = 1
lives = 6
from hangmanweb import *

firebase = firebase.FirebaseApplication('https://popping-inferno-6024.firebaseio.com/', None)

app = Flask(__name__)

Hang = HangMan()


def get_data(api):
    get = urllib2.urlopen(api).read()
    data = json.loads(get)

    return data

def insertScore(name,score):
    mydict = {name: score};
    firebase.post('/scores/', mydict)

def insertNewPlayer(name,username,password):
    mydict = {'name': name , 'username' : username, 'password' : password }
    try:
        result = firebase.post('/players', mydict)
        return True
    except:
        return 'ERROR - Could not get information from server...'

def valid_login(uname,passwrd):
    api = "https://popping-inferno-6024.firebaseio.com/players.json"
    data = get_data(api)
    players = {}
    for v in data.values():
        for k,v in v.items():
            return k[1], k[2]
            """if username ==uname and password == passwrd:
                                                        return True
                                                    else:
                                                        return False """
"""
@app.route('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''
"""

@app.route("/")
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return valid_login("root", "123455") #You are not logged in

@app.route('/login', methods=['POST','GET'])
def login():
    result = None
    if request.method == 'POST':
        username = request.form['txt_username']
        password = request.form['txt_password']
        result = valid_login(username,password)
        """if result == True:
                                    session['username'] = request.form['username']
                                    return redirect(url_for('hangman'))
                                else:
                                    result = 'Username/Password incorrect.'"""

    else:
        result = "Get Method"

    return render_template("login.html", result=result)


@app.route('/register', methods=['POST','GET'])
def register():
    response = ""
    if request.method == 'POST':
        username = request.form['reg_username']
        name = request.form['reg_name']
        password = request.form['reg_password']
        response = insertNewPlayer(name,username,password)
        if response == True:
            return redirect(url_for('login'))
    else:
        response = "Please use get method."

    return render_template("register.html", response=response)

@app.route('/hangman', methods=['POST','GET'])
def hangman():
    global guess, score,level,lives
    if request.method == 'POST':
        input = request.form['input_char']
        data = hangman_start(input)
        if data:
            return render_template("main-game.html", d=data)
        else:
            return render_template("main-game.html")
    else:
        level = 1
        score = 0
        guess = ''
        lives = 6
        word_list = Hang.word_list('1.txt')
        word = Hang.checkWord(word_list,guess,score)
        data = {"word":word['word'], "guess":guess, "true_word": word_list,
                "score":word['score'],"lives" : lives , "level":level}
        
        return render_template("game.html", data=data)

@app.route('/play', methods=['POST','GET'])
def play():
    if request.method == 'POST':
        global guess, score,level,lives
        winput = request.form['input_char']
        word_list = request.form['word']
        if lives > 0:
            if winput in guess:
                word = Hang.checkWord(word_list,guess,score)
                data = {"word":word['word'], "guess":guess, "true_word": word_list,
                        "score":word['score'],"lives" : lives , "level":level}
                
                return render_template("game.html", data=data)
            else:
                guess += winput
                #word_list = session['cur_word']
                blanks = '_'
                word = Hang.checkWord(word_list,guess,score)
                if  word['word'] == word_list:
                    prev_word = word_list
                    level+=1
                    score += 50
                    score += word['score']
                    word_list = Hang.word_list('1.txt')
                    guess = ''
                    word = Hang.checkWord(word_list,guess,score)
                    message = "Congrats You have guessed the word: %s." % prev_word
                    data = {"word":word['word'], "guess":guess, "true_word": word_list,
                            "score":word['score'],"lives" : lives, "level":level, "message":message}

                    return render_template("game.html", data=data)
                else:
                    word = Hang.checkWord(word_list,guess,score)
                    lives = Hang.isExist(word_list,winput,lives)
                    data = {"word":word['word'], "guess":guess, "true_word": word_list,
                            "score":word['score'],"lives" :lives, "level":level}
                    return render_template("game.html", data=data)
        else:
            message = "Sorry you lost!"
            score = request.form['score']
            lives = request.form['lives']
            data = {"level":level, "score":score, "message":message, "lives":lives}
            return render_template("gameover.html", data=data)

    else:
        return render_template("gameover.html")
    
    


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
