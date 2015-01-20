from flask import Flask, request, render_template
from flask.ext import restful
from flask.ext.restful import Resource, Api, request, reqparse
from flask.views import View
from sys import argv
from os.path import exists
from random import randrange
import time
import requests
from xml.etree import ElementTree as ET
import urllib
import sys
import json
import operator
from firebase import firebase

#firebase = firebase.FirebaseApplication('https://group3-hangman.firebaseio.com', None)
#firebase = firebase.FirebaseApplication('https://popping-inferno-6024.firebaseio.com/', None)

class HangMan():
	def clear_scores():
		firebase.delete('/scores',0)

	def insert(name,score):
		mydict = {name: score};
		firebase.post('/scores/', mydict)


	def getScores():

		rs = firebase.get("/scores", None)
		json_encode = json.dumps(rs)
		json_decode = json.loads(json_encode)

		top_score = {}
		for key, val in json_decode.items():
		    for un, scr in val.items():
			top_score[un] = scr


		#sort
		limit = 1
		for k, v in sorted(top_score.items(), key = operator.itemgetter(1), reverse=True):
		    if (limit >= 1 and limit <= 10) :
		        print '%d %s %d' % (limit,k,v)
		        limit += 1


	def dictionary(word):
	    try:

		CurrentConditions = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'+word+'?key=0cf5838d-0e7a-4d3c-815b-0241aaf76ea6'
		urllib.socket.setdefaulttimeout(8)
		usock = urllib.urlopen(CurrentConditions)
		tree = ET.parse(usock)
		usock.close()

		for weather in tree.findall(".//dt"):
		    print weather.text
	    except:
		print 'ERROR - Could not get information from server...'
		sys.exit(1)

	def word_list(self, textfile):
		word_list = []
		infile = open(textfile)
		for line in infile:
		        word_list.append(line.strip())
		infile.close()
		randindex = randrange(len(word_list))
		has_found_new = False
		newWord = ''
		while not has_found_new:
		        newWord =  word_list[randindex-1]
		        if len(newWord)>=4:
		                has_found_new = True
		return newWord
        def isExist(self, word_list,char,lives):
                if char in word_list:
                        return lives
                else:
                        return lives-1
                
                
                
	def checkWord(self, wordlist, guesses,score):
		verify_word = ''
                one = "eaionrtlsu"
                two = "dg"
                three = "bcmp"
                four = "fhvwy"
                five = "l"
                eight = "jx"
                ten = "qz"
                
		for char in wordlist:
		        if char in guesses:
                                if char in one:
                                        score+=1
                                elif char in two:
                                        score+=2
                                elif char in three:
                                        score+=3
                                elif char in four:
                                        score+=4
                                elif char in five:
                                        score+=5
                                elif char in eight:
                                        score+=8
                                elif char in ten:
                                        score+=10
		                verify_word+=char
		        else:
		                verify_word+='_'

                params = {'word':verify_word,'score':score}
                return params
		                

	def hangman_start():

		while status != "gameover":
		        print "Hello, " + name, "Time to play hangman!"

		        print "\n"
		        temp = 0
		        print "Start guessing..."
		        infile = open('txt.txt', 'r')
		        word_list= []
		        for line in infile:
		            word_list.append(line.strip())

		        infile.close()
		        randindex = randrange(len(word_list))
		        has_found_new = False
		        newWord = ''
		        while not has_found_new:
		            newWord =  word_list[randindex-1]
		            if len(newWord)>=4:
		                has_found_new = True
		        word= newWord
		        guesses = ''
		        turns = 6
		        one = "eaionrtlsu"
		        two = "dg"
		        three = "bcmp"
		        four = "fhvwy"
		        five = "l"
		        eight = "jx"
		        ten = "qz"
		        while turns > 0:
		                failed = 0
		                for char in word:
		                    if char  in guesses:

		                        print char,
		                        #scoring system for the app
		                        if char in one:
		                            temp+=1
		                        elif char in two:
		                            temp+=2
		                        elif char in three:
		                            temp+=3
		                        elif char in four:
		                            temp+=4
		                        elif char in five:
		                            temp+=5
		                        elif char in eight:
		                            temp+=8
		                        elif char in ten:
		                            temp+=10
		                    else:
		                        print "_" ,
		                        failed += 1


		                if failed == 0:
		                    print "\nYou won"
		                    temp+=50
		                    score+=temp
		                    level+=1
		                    break
		                print
		                print "Level: %s" % level
		                guess = raw_input("guess a character:")
		                if guess.isalpha():
		                        if len(guess) == 1:
		                            guesses += guess
		                            if guess not in word:
		                                turns -= 1
		                                print "Wrong\n"
		                                print "You have", + turns, 'more guesses'
		                                if turns == 2:
		                                    dictionary(word)
		                                if turns == 0:
		                                    score+=temp
		                                    print "You Loose\n Game over!"
		                                    print "The word is %s" % word
		                                    print "Your score is being saved. please wait"
		                                    print "%s your score is %s" % (name,score)
		                                    insert(name,score)
		                                    status = "gameover"
		                                    time.sleep(5)
		                        else:
		                            print "Enter 1 letter only!"
		                else:
		                        print "Enter characters only!"
		        #ans = raw_input("Try again?: ")



#hangman_start()



app = Flask(__name__)
api = restful.Api(app)

todos = {}

class Hangman(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}
    def put(self, todo_id):
        return {todo_id: todos[todo_id]}

class HelloWorld(restful.Resource):

    def dispatch_request(self):
        headers = {'Content-Type': 'text/html'}
        data = {"Name":"Joeper","Last":"Serrano"}

        return render_template('hello.html' , was=data)

class ShowUsers(View):
    
    def dispatch_request(self):
        #users = User.query.all()
        data = [1,2,3]
        return render_template('hello.html', d=data)
    
class hangman_start(View):
    
    def dispatch_request(self):
        scores = getScores()
        return render_template('hello.html', fire=scores)

    


app.add_url_rule('/', view_func=ShowUsers.as_view('show_users'))
app.add_url_rule('/users', view_func=HelloWorld.as_view('get_user'))
app.add_url_rule('/hangman', view_func=hangman_start.as_view('highscores'))



#api.add_resource(HelloWorld, '/')
#api.add_resource(Hangman, '/')


if __name__ == '__main__':
    app.run(debug=True)
