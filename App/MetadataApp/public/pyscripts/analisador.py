#!/usr/bin/python3
##!/usr/local/bin/python3

import json,sys,xlsxwriter,os,glob
import re

#class Post:
	#def __init__(newObject,postid,arrayComments,ocur):
		#newObject.post_id=postid
		#newObject.arrayComments=arrayComments
		#newObject.ocurrencias=ocur


#Classe Comentario
#comment_id : ID do comentário
#commentMessage : Texto do Comentario
#user : ID do utilizador 
#occurrencias : Objeto ocorrencias que permite guardar as ocorrencias de cada palavra reservada do respetivo comentario
class Comentario:
	def __init__(newObject,comment_id,commentMessage,user,ocur):
		newObject.comment_id=comment_id
		newObject.commentMessage=commentMessage
		newObject.user=user
		newObject.ocurrencias=ocur


#Função que extrai informação dos ficheiros de comentarios para um array
def loadInfoExtract(inventory,com_id,com_txt,com_user):
	arrayComments = []
	i=0
	for item in inventory:
		arrayComments.append(Comentario(item[com_id],item[com_txt],item[com_user],[]))
		i+=1
	return arrayComments

#Função de inicialização do python para tratar ficheiro JSON
def loadInfo(file):
	info = open(file).read()
	inventory = json.loads(info)
	return inventory

#Função recursiva que trata de guardar para um array todos os valores do tipo lista de um objeto  
def parseValues(objeto):
	lista = []
	for key in objeto.keys():
		if type(objeto[key]) is list:
			lista += objeto[key]
		else:
			lista += parseValues(objeto[key])		
	return lista

#Função que dado um preconceito e o inventário de comentários 
#retorna um tuplo com o tipo de preconceito e as palavras reservadas (keywords)
def loadKeywordsRecAux(inventory,prejudice):
	value = ()
	for items in inventory:
		if (items['type_prejudice'] == prejudice):
			value = (prejudice, parseValues(items['Sociolinguistic variables']))
	return value

#Função global, que dada a escolha do utilizador, se auxilia na função loadKeywordsRec 
#para retornar a lista de tuplos de preconceitos-keywords
def loadKeywordsRec(inventory,choice):
	prejudices = ["Sexism","Ageism","Racism","Nationalism","Classism","Intolerance_to"]
	arrayKW = []
	if (choice == 6):
		for prejudice in prejudices:
				arrayKW.append(loadKeywordsRecAux(inventory,prejudice)) 
	else:
		arrayKW.append(loadKeywordsRecAux(inventory,prejudices[choice]))
	return arrayKW


#Função Obsoleta
def loadKeywords(inventory,keyword):
	arrayKeywords = []
	i=0
	for items in inventory:
		if(items['type_prejudice']==keyword):	
			for values in items['Sociolinguistic variables'].values():
				print(values)
				arrayKeywords=values
	return arrayKeywords

#Função que realiza o trabalho de procura da string da Keyword na string do texto do comentário
#Caso encotre, cria um triplo com a keyword, o numero de occorencias e o total de palavras do comentario em questao
def checkNcount(comentario,keywords):
	ocurrencias = []
	#print(keywords)
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

#Função que retorna um tuplo com o preconceito e um array de comentarios 
# onde existe a ocorrencia desse preconceito
#
#Nesse array de comentarios, estes são carregados com a informação das 
# suas ocorrencias no elemento ocurrencias da classe comentario
def analiseAux(comentarios,keywords,prejudice):
	ocurrencias = []
	arraycoments = []
	#totalWordCount = 0
	for comentario in comentarios:
		#totalWordCount += len(comentario.commentMessage.split())
		ocurrencias = checkNcount(comentario,keywords)
		if ocurrencias:
			comentario_copia = Comentario(comentario.comment_id,comentario.commentMessage,comentario.user,[])
			comentario_copia.ocurrencias = ocurrencias
			arraycoments.append(comentario_copia)
	#Array de comentarios, em que cada um possui um array de ocurrencias 
	value = (prejudice,arraycoments)
	#print(value)
	return value


#Função que retorna um array com todos os tuplos preconceito-comentarios 
#resultantes da funçãoauxiliar analiseAux
def analise(comentarios, keywords):
	prejsComents = []
	for kw in keywords:
		#print(kw[1])
		prejsComents.append(analiseAux(comentarios,kw[1],kw[0]))
	return prejsComents


#Função que retorna os tuplos de ocorrencias de keywords para o post
#Basicamente soma as ocorrencias dos comentarios para gerar as do post 
def getPostOcur(prejsComents):
	postOcur = []
	for prejComents in prejsComents:
		for comentario in prejComents[1]:
			postOcur.extend(comentario.ocurrencias)
	my_set = {x[0] for x in postOcur}
	postOcur = [(i,sum(x[1] for x in postOcur if x[0] == i)) for i in my_set]
	return postOcur

#Função de pretty printing para debbugging
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

#Função que desenha o excell com as estatísticas
#Frequencias relativas, absolutas e totais dos comentarios para cada post
def excelWriter(prejsComents,nComents,totais,worksheetName,workbook, file_name):
	#variaveis
	#tam= len(comentarios[1])+3
	total_linhas = 0
	final=0
	final_id=0
	currente = 4

	worksheet = workbook.add_worksheet(worksheetName)

	#Parte estatica
	bold = workbook.add_format({'bold': True})
	princ = workbook.add_format({'bold': True,'font_color':'white','font_size':'14','bg_color':'green'})
	pre = workbook.add_format({'bold': True,'font_color':'black','font_size':'10','valign': 'vcenter','align': 'center','border_color':'black'})
	worksheet.write('B1', 'Ficheiro',princ)
	worksheet.merge_range('C1:E1',file_name,pre)
	worksheet.write('B3', 'Prejudice',princ)
	worksheet.write('C3', 'Comentario',princ)
	worksheet.write('D3', 'ID',princ)
	worksheet.write('E3', 'Frequencia',princ)
	worksheet.write('G3', 'Total',princ)

	#Parte dinamica
	for prejComents in prejsComents:
		tamC = len(prejComents[1])
		tam = tamC + currente
		tam_str = str(tam-1)
		curr_str = str(currente)
		if(tamC>1):
			worksheet.merge_range('B'+curr_str+':B'+tam_str,prejComents[0],pre)
		else:
			worksheet.write('B'+curr_str,prejComents[0],pre)
		for comentario in prejComents[1]:
			total_linhas += 1
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

	worksheet.write('I3','Ocorrencias',princ)
	worksheet.set_column('I:J',20)

	counter=4
	for info in totais:
		str_counter=str(counter)
		worksheet.write('I'+str_counter,str(info[0])+' ----> '+str(info[1]))
		counter+=1


	worksheet.merge_range('G4:G'+str(total_linhas+3),str(total_linhas)+'/'+str(nComents),pre)

	print('terminei')	

#Função geral
def main():
	selection = sys.argv[1]
	file_path = sys.argv[2]
	keywords_path = sys.argv[3]
	#file_path = f"../Extratos/{selection}/{file_name}"

	# criação do inventário das keywords
	kw_inventory = loadInfo(keywords_path)

	# criação do xslx
	workbook = xlsxwriter.Workbook('resultado.xlsx')

	prejudice = 6
	
	counter = 0
	
	print('A analisar ficheiro.....')
	##Fazer análise do ficheiro escolhido
	print(file_path)

	com_inventory = loadInfo(file_path)
	if(selection == "youtube"):
		comentarios = loadInfoExtract(com_inventory, 'id', 'commentText', 'user')
	else:
		comentarios = loadInfoExtract(com_inventory, 'comment_id', 'comment_message', 'comment_by')
	keywords = loadKeywordsRec(kw_inventory, prejudice)
	prejsComents = analise(comentarios, keywords)
	printOcurrencias(prejsComents)
	totais = getPostOcur(prejsComents)
	nComents = len(comentarios)

	excelWriter(prejsComents, nComents, totais, f"sheet{counter}", workbook, file_path)
	counter += 1

	#fechar o workbook
	workbook.close()

main()
