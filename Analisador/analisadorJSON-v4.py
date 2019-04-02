#!/usr/bin/python3
##!/usr/local/bin/python3


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

def loadKeywordsRecAux(inventory,prejudice):
	value = ()
	for items in inventory:
		if (items['type_prejudice'] == prejudice):
			value = (prejudice, parseValues(items['Sociolinguistic variables']))
	return value

def loadKeywordsRec(inventory,choice):
	prejudices = ["Sexism","Ageism","Sexism","Racism","Nationalism","Classism","Intolerance_to"] 
	arrayKW = []
	if (choice == 6):
		for prejudice in prejudices:
				arrayKW.append(loadKeywordsRecAux(inventory,prejudice)) 
	else:
		arrayKW.append(loadKeywordsRecAux(inventory,prejudices[choice]))
	return arrayKW

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


def analiseAux(comentarios,keywords,prejudice):
	ocurrencias = []
	arraycoments = []
	#totalWordCount = 0
	for comentario in comentarios:
		#totalWordCount += len(comentario.commentMessage.split())
		ocurrencias = checkNcount(comentario,keywords)
		if ocurrencias:
			comentario.ocurrencias = ocurrencias
			arraycoments.append(comentario)
	#Array de comentarios, em que cada um possui um array de ocurrencias 
	value = (prejudice,arraycoments)
	return value

def analise(comentarios, keywords):
	prejsComents = []
	for kw in keywords:
		prejsComents.append(analiseAux(comentarios,kw[1],kw[0]))
	return prejsComents

def getPostOcur(prejsComents):
	postOcur = []
	for prejComents in prejsComents:
		for comentario in prejComents[1]:
			postOcur.extend(comentario.ocurrencias)
	my_set = {x[0] for x in postOcur}
	postOcur = [(i,sum(x[1] for x in postOcur if x[0] == i)) for i in my_set]
	return postOcur

def printOcurrencias(prejsComents):
	str = ""
	for prejComents in prejsComents:
		str += prejComents[0]
		str += "\n"
		for comentario in prejComents[1]:
			str += comentario.comment_id + " --> "
			for value in comentario.ocurrencias:
				str += "{}".format(value)
			str += "\n"
		str += "\n"
	
	print(str)

def excelWriter(prejsComents,nComents,totais):
	#variaveis
	#tam= len(comentarios[1])+3
	total_linhas = 0
	final=0
	final_id=0
	currente = 4
	#criação
	workbook = xlsxwriter.Workbook('test.xlsx')
	worksheet = workbook.add_worksheet('Estatistica')
	#Parte estatica
	bold = workbook.add_format({'bold': True})
	princ = workbook.add_format({'bold': True,'font_color':'white','font_size':'14','bg_color':'green'})
	pre = workbook.add_format({'bold': True,'font_color':'black','font_size':'10','valign': 'vcenter','align': 'center','border_color':'black'})
	worksheet.write('B3', 'Prejudice',princ)
	worksheet.write('C3', 'Comentario',princ)
	worksheet.write('D3', 'ID',princ)
	worksheet.write('E3', 'Frequencia',princ)
	worksheet.write('H3', 'Total',princ)

	#Parte dinamica
	for prejComents in prejsComents:
		tam = len(prejComents[1])
		tam_str = str(tam)
		currente_str = str(currente)
		total_linhas += tam
		worksheet.merge_range('B'+currente_str+':B'+tam_str,prejComents[0],pre)
		for comentario in prejComents[1]:
			curr_str = str(currente)
			maior_mm = len(comentario.commentMessage)
			maior_id = len(comentario.comment_id)
			if(maior_mm > final):
				final = maior_mm
			if(maior_id > final_id):
				final_id = maior_id
			worksheet.write('C'+curr_str, comentario.commentMessage)
			worksheet.write('D'+curr_str,comentario.comment_id)
			currente+=1
			worksheet.write('E'+curr_str,str(comentario.ocurrencias))

	worksheet.set_column('B:D',len('prejudice..'))
	worksheet.set_column('C:D',final)
	worksheet.set_column('D:E',final_id)

	worksheet.write('J3','Ocorrencias',princ)
	worksheet.set_column('J:G',20)

	counter=4
	for info in totais:
		str_counter=str(counter)
		worksheet.write('J'+str_counter,str(info[0])+' ----> '+str(info[1]))
		counter+=1


	worksheet.merge_range('H4:H'+tam_str,str(total_linhas)+'/'+str(nComents),pre)

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
	menu['7']="All"
	menu['8']="Exit"
	while True: 
		options=menu.keys()
		for entry in options: 
			print (entry, menu[entry])

		selection=input("Please Select:") 
		if selection =='1':
			prejudice = 0
			print("Sexism Selected")
			break 
		elif selection == '2':
			prejudice = 1 
			print("Ageism Selected")
			break
		elif selection == '3':
			prejudice = 2
			print("Racism Selected")
			break
		elif selection == '4':
			prejudice = 3
			print("Nationalism Selected")
			break
		elif selection == '5':
			prejudice = 4
			print("Classism Selected")
			break
		elif selection == '6':
			prejudice = 5
			print("Intolerance_to Selected")
			break
		elif selection == '7':
			prejudice = 6
			print("All selected")
			break
		elif selection == '8':
			prejudice = "none" 
			break
		else: 
			print("Unknown Option Selected!") 

	kw_inventory = loadInfo("../Keywords/keywords_pt.json")
	com_inventory = loadInfo("../Extratos/youtube/fase1/Youtube_extraction_portuguese_1.json")
	comentarios = loadInfoExtract(com_inventory,'id','commentText','user')
	keywords = loadKeywordsRec(kw_inventory,prejudice)
	prejsComents = analise(comentarios,keywords)
	printOcurrencias(prejsComents)
	totais=getPostOcur(prejsComents)
	nComents=len(comentarios)
	excelWriter(prejsComents,nComents,totais)

	
main()
