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
firebase = firebase.FirebaseApplication('https://popping-inferno-6024.firebaseio.com/', None)


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

def hangman_start():
	ans="y"
	while ans=="y":
		score = 0
		level = 1
		print "Let's Play Hangman V2.0"
		print "(a) start a new game"
		print "(b) View topscores"
		print "\n"
		choice = raw_input("Your Choice?")
		print "\n"
		status = ""
		if choice == "a":
		    name = raw_input("What is your name?(max of 3 letters only!) ")
		    while len(name)<=3 and status != "gameover":
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

		elif choice == "b":
		    print "Highscores!"
		    getScores()
		else:
		    print "Goodbye!"
		    sys.exit(1)

hangman_start()

