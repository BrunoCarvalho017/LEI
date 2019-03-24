#!/usr/bin/env python
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


def loadInfoExtract(inventory,com_id,com_txt,com_user):
	arrayComments = []
	i=0
	for item in inventory:
		arrayComments.append(Comentario(item[com_id],item[com_txt],item[com_user],[]))
		i+=1
	return arrayComments

def loadInfo(file):
	info = open(file).read()
	inventory = json.loads(info)
	return inventory

def parseValues(objeto):
	lista = []
	for key in objeto.keys():
		if type(objeto[key]) is list:
			lista += objeto[key]
		else:
			lista += parseValues(objeto[key])		
	return lista

def loadKeywordsRec(inventory,prejudice):
	arrayKeywords = []
	for items in inventory:
		if (items['type_prejudice'] == prejudice):
			arrayKeywords = parseValues(items['Sociolinguistic variables'])
	
	return arrayKeywords


def loadKeywords(inventory,keyword):
	arrayKeywords = []
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
			#contabilizar o numero de occurencias da keyword dentro do comentario
			nOcur = len(re.findall(r"\b"+keyword+r"\b",comentario.commentMessage,re.I))
			if(nOcur > 0):
				#contabilizar o numero total de palavras
				wordcount = len(comentario.commentMessage.split())
				value = (keyword, nOcur, wordcount)
				ocurrencias.append(value)
				#print(comentario.commentMessage)
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
			prejudice = menu[selection] 
			print("Sexism Selected")
			break 
		elif selection == '2':
			prejudice = menu[selection] 
			print("Ageism Selected")
			break
		elif selection == '3':
			prejudice = menu[selection]
			print("Racism Selected")
			break
		elif selection == '4':
			prejudice = menu[selection]
			print("Nationalism Selected")
			break
		elif selection == '5':
			prejudice = menu[selection]
			print("Classism Selected")
			break
		elif selection == '6':
			prejudice = menu[selection]
			print("Intolerance_to Selected")
			break
		elif selection == '7':
			prejudice = "none" 
			break
		else: 
			print("Unknown Option Selected!") 

	kw_inventory = loadInfo("../Keywords/keywords_pt.json")
	com_inventory = loadInfo("../Extratos/youtube/fase1/Youtube_extraction_portuguese_1.json")
	comentarios = loadInfoExtract(com_inventory,'id','commentText','user')
	keywords = loadKeywordsRec(kw_inventory,prejudice)
	estatistica = analise(comentarios,keywords)
	printOcurrencias(estatistica)

	
main()
