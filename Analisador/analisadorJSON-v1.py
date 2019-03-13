##!/usr/local/bin/python3
#!/usr/bin/python3

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

def checkNcount(comentario,keywords):
	ocurrencias = []
	for keyword in keywords:
			nOcur = len(re.findall(r"\b"+keyword+r"\b",comentario.commentMessage,re.I))
			if(nOcur > 0):
				value = (keyword, nOcur)
				ocurrencias.append(value)
				print(comentario.commentMessage)
	return ocurrencias


def analise(comentarios,keywords):
	ocurrencias = []
	arrayComens = []
	for comentario in comentarios:
		ocurrencias = checkNcount(comentario,keywords)
		if ocurrencias:
			comentario.ocurrencias = ocurrencias
			arrayComens.append(comentario)
	return arrayComens

def printOcurrencias(comentarios):
	str = ""
	for comentario in comentarios:
		str += comentario.comment_id + " --> "
		for value in comentario.ocurrencias:
			str += "{}".format(value)
		str += "\n"
	
	print(str)		

def main():
	comentarios = loadInfoExtract("../Extratos/result2.json")
	keywords = loadKeywords("../Keywords/keywords_pt.json")
	estatistica = analise(comentarios,keywords)
	printOcurrencias(estatistica)
	
main()
