#!/usr/local/bin/python3

import json
import re


#class Post:
	#def __init__(newObject,postid,arrayComments,ocur):
		#newObject.post_id=postid
		#newObject.arrayComments=arrayComments
		#newObject.ocurrencias=ocur

class Comentario:
	def __init__(newObject,comment_id,commentMessage,ocur):
		newObject.comment_id=comment_id
		newObject.commentMessage=commentMessage
		newObject.ocurrencias=ocur


def loadInfoExtract(file):
	arrayComments = []
	info = open(file).read()
	inventory = json.loads(info)
	i=0
	for item in inventory:
		arrayComments.append(Comentario(item['comment_id'],item['comment_message'],[]))
		i+=1
	return arrayComments


def loadKeywords(file):
	arrayKeywords = []
	info = open(file).read()
	inventory = json.loads(info)
	i=0
	for items in inventory:
		if (items['type_prejudice']=='Sexism'):
			for values in items['Sociolinguistic variables'].values():
				arrayKeywords=values
	return arrayKeywords

def check(comentario,keywords):
	for keyword in keywords:
			if(len(re.findall(r"\b"+keyword+r"\b",comentario.commentMessage,re.I))>0):
				print(comentario.commentMessage)


def analise(comentarios,keywords):
	for comentario in comentarios:
		check(comentario,keywords)


def main():
	comentarios=loadInfoExtract("../Extratos/result2.json")
	keywords= loadKeywords("../Keywords/keywords_pt.json")
	analise(comentarios,keywords)


main()
