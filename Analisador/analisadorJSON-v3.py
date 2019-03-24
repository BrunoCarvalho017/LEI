#!/usr/bin/python3
##!/usr/local/bin/python3
##!/usr/bin/python3

import json,sys,xlsxwriter
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
	arraycoments = []
	totalWordCount = 0
	for comentario in comentarios:
		totalWordCount += len(comentario.commentMessage.split())
		ocurrencias = checkNcount(comentario,keywords)
		if ocurrencias:
			comentario.ocurrencias = ocurrencias
			arraycoments.append(comentario)
	value = (totalWordCount,arraycoments)
	return value

def getcomentsOcur(estatistica):
	postOcur = []
	for entry in estatistica[1]:
		postOcur.extend(entry.ocurrencias)
	my_set = {x[0] for x in postOcur}
	postOcur = [(i,sum(x[1] for x in postOcur if x[0] == i)) for i in my_set]
	return postOcur

def printOcurrencias(comentarios):
	str = ""
	for comentario in comentarios:
		str += comentario.comment_id + " --> "
		for value in comentario.ocurrencias:
			str += "{}".format(value)
		str += "\n"
	
	print(str)

def excelWriter(prejudice,comentarios,nComents,totais):
	tam= len(comentarios[1])+3
	final=0
	final_id=0
	tam_str=str(tam)
	currente = 4
	workbook = xlsxwriter.Workbook('test.xlsx')
	worksheet = workbook.add_worksheet('Estatistica')

	bold = workbook.add_format({'bold': True})
	princ = workbook.add_format({'bold': True,'font_color':'white','font_size':'14','bg_color':'green'})
	pre = workbook.add_format({'bold': True,'font_color':'black','font_size':'10','valign': 'vcenter','align': 'center','border_color':'black'})
	worksheet.write('B3', 'Prejudice',princ)
	worksheet.write('C3', 'Comentario',princ)
	worksheet.write('D3', 'ID',princ)
	worksheet.write('E3', 'Frequencia',princ)
	worksheet.write('H3', 'Total',princ)
	worksheet.merge_range('B4:B'+tam_str,prejudice,pre)
	for comentario in comentarios[1]:
		curr_str=str(currente)
		maior_mm= len(comentario.commentMessage)
		maior_id= len(comentario.comment_id)
		if(maior_mm>final):
			final=maior_mm
		if(maior_id>final_id):
			final_id=maior_id
		worksheet.write('C'+curr_str, comentario.commentMessage)
		worksheet.write('D'+curr_str,comentario.comment_id)
		currente+=1
		worksheet.write('E'+curr_str,str(comentario.ocurrencias))
	worksheet.set_column('B:D',len('prejudice..'))
	worksheet.set_column('C:D',final)
	worksheet.set_column('D:E',final_id)

	worksheet.write('J3','Ocurrencias',princ)
	worksheet.set_column('J:G',20)

	counter=4
	for info in totais:
		str_counter=str(counter)
		worksheet.write('J'+str_counter,str(info[0])+' ----> '+str(info[1]))
		counter+=1


	worksheet.merge_range('H4:H'+tam_str,str(len(comentarios[1]))+'/'+str(nComents),pre)

	workbook.close()
	print('terminei')	

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
	com_inventory = loadInfo("../Extratos/youtube/fase2/Youtube_extraction_portuguese_1.json")
	comentarios = loadInfoExtract(com_inventory,'id','commentText','user')
	keywords = loadKeywordsRec(kw_inventory,prejudice)
	estatistica = analise(comentarios,keywords)
	printOcurrencias(estatistica[1])
	totais=getcomentsOcur(estatistica)

	nComents=len(comentarios)
	excelWriter(prejudice,estatistica,nComents,totais)

	
main()
