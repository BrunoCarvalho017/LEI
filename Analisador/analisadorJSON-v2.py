#!/usr/local/bin/python3
##!/usr/bin/python3

import json,sys
import re


#class Post:
	#def __init__(newObject,postid,arrayComments,ocur):
		#newObject.post_id=postid
		#newObject.arrayComments=arrayComments
		#newObject.ocurrencias=ocur

class Comentario:
	def __init__(newObject,comment_id,commentMessage,user,ocur):
		newObject.comment_id=comment_id
		newObject.commentMessage=commentMessage
		newObject.user=user
		newObject.ocurrencias=ocur


def loadInfoExtract(file):
	arrayComments = []
	info = open(file).read()
	inventory = json.loads(info)
	i=0
	for item in inventory:
		arrayComments.append(Comentario(item['id'],item['commentText'],item['user'],[]))
		i+=1
	return arrayComments


def loadKeywords(file,keyword):
	arrayKeywords = []
	info = open(file).read()
	inventory = json.loads(info)
	i=0
	for items in inventory:
		if(items['type_prejudice']==keyword):	
			for values in items['Sociolinguistic variables'].values():
				print(values)
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
	menu = {}
	menu['1']="Sexism" 
	menu['2']="Ageism"
	menu['3']="Racism"
	menu['4']="Nationalism"
	menu['5']="Classism"
	menu['6']="Intolerance_to"
	menu['7']="Exit"
	while True: 
		options=menu.keys()
		for entry in options: 
			print (entry, menu[entry])

		selection=input("Please Select:") 
		if selection =='1':
			keyword= menu[selection] 
			print("Sexism Selected")
			break 
		elif selection == '2':
			keyword= menu[selection] 
			print("Ageism Selected")
			break
		elif selection == '3':
			keyword= menu[selection]
			print("Racism Selected")
			break
		elif selection == '4':
			keyword= menu[selection]
			print("Nationalism Selected")
			break
		elif selection == '5':
			keyword= menu[selection]
			print("Classism Selected")
			break
		elif selection == '6':
			keyword= menu[selection]
			print("Intolerance_to Selected")
			break
		elif selection == '7':
			keyword= "none" 
			break
		else: 
			print("Unknown Option Selected!") 
	comentarios = loadInfoExtract("../Extratos/youtube/fase1/Youtube_extraction_portuguese_1.json")
	keywords = loadKeywords("../Keywords/keywords_pt.json",keyword)
	#estatistica = analise(comentarios,keywords)
	#printOcurrencias(estatistica)

	
main()