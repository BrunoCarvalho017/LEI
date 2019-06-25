#!/usr/bin/python3
##!/usr/local/bin/python3

import json,sys,xlsxwriter,os,glob
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pymongo

#class Post:
	#def __init__(newObject,postid,arrayComments,ocur):
		#newObject.post_id=postid
		#newObject.arrayComments=arrayComments
		#newObject.occurrences=ocur


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
		newObject.occurrences=ocur


#Função que extrai informação dos ficheiros de comentarios para um array
def loadInfoExtract(inventory,com_id,com_txt,com_user):
	arrayComments = []
	i=0
	for item in inventory["commentThread"]:
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
			lista += (key,objeto[key])
		else:
			lista += parseValues(objeto[key])		
	return lista

#Função que dado um preconceito e o inventário de keywords 
#retorna um triplo com o tipo de preconceito, variavel sociolinguistica e as palavras reservadas (keywords)
def loadKeywordsRecAux(inventory,prejudice):
	value = ()
	parsedValues = ()
	for items in inventory:
		if (items['type_prejudice'] == prejudice):
			parsedValues = parseValues(items['sociolinguistic_variables'])
			var_sociol = parsedValues[0]
			kws = parsedValues[1] 
			value = (prejudice, var_sociol,kws)
	return value

#Função global, que dada a escolha do utilizador, se auxilia na função loadKeywordsRec 
#para retornar a lista de tuplos de preconceitos-keywords
def loadKeywordsRec(inventory):
	prejudices = ["Sexism","Ageism","Racism","Nationalism","Classism","Homophobia","Anti-Clericalism","Body-Shaming","Addiction-Shaming","Ideological-Shaming"]
	prej_sociol_kws_triples = []   		
	for prejudice in prejudices:
		prej_sociol_kws_triples.append(loadKeywordsRecAux(inventory,prejudice)) 
	return prej_sociol_kws_triples

#Função Obsoleta
def loadKeywords(inventory,keyword):
	arrayKeywords = []
	i=0
	for items in inventory:
		if(items['type_prejudice'] == keyword):	
			for values in items['Sociolinguistic variables'].values():
				print(values)
				arrayKeywords=values
	return arrayKeywords

#Função que realiza o trabalho de procura da string da Keyword na string do texto do comentário
#Caso encotre, cria um triplo com a keyword, o numero de occorencias e o total de palavras do comentario em questao
def checkNcount(comentario,keywords):
	occurrences = []
	#print(keywords)
	nOcur = 0
	wordcount = 0
	for keyword in keywords:
		"""
		#contabilizar o numero de occurencias da keyword dentro do comentario
		nOcur = len(re.findall(r"\b"+keyword+r"\b",comentario.commentMessage,re.I))
		if(nOcur > 0):
			#contabilizar o numero total de palavras
			wordcount = len(comentario.commentMessage.split())
			value = (keyword, nOcur, wordcount)
			occurrences.append(value)
			#print(comentario.commentMessage)
		"""
		words = comentario.commentMessage.split()
		for word in words:
			if fuzz.ratio(word,keyword) >= 75:
				nOcur += 1
		if(nOcur > 0):
			#contabilizar o numero total de palavras
			wordcount = len(comentario.commentMessage.split())
			value = (keyword, nOcur, wordcount)
			occurrences.append(value)
			#print(comentario.commentMessage)
			nOcur = 0
			wordcount = 0

	return occurrences

#Função que retorna um tuplo com o preconceito e um array de comentarios 
# onde existe a ocorrencia desse preconceito
#
#Nesse array de comentarios, estes são carregados com a informação das 
# suas ocorrencias no elemento ocurrencias da classe comentario
def lexicalAnalysisAux(comentarios,var_sociol,keywords):
	occurrences = []
	arraycoments = []
	#totalWordCount = 0
	for comentario in comentarios:
		#totalWordCount += len(comentario.commentMessage.split())
		occurrences = checkNcount(comentario,keywords)
		if occurrences:
			comentario_copia = Comentario(comentario.comment_id,comentario.commentMessage,comentario.user,[])
			comentario_copia.occurrences = occurrences
			arraycoments.append(comentario_copia)
	#Array de comentarios, em que cada um possui um array de ocurrencias 
	var_sociolPost = (var_sociol,arraycoments)
	#print(var_sociolPost)
	return var_sociolPost


#Função que retorna um array com todos os tuplos variavel_sociol-comentarios 
#resultantes da funçãoauxiliar lexicalAnalysisAux
def lexicalAnalysis(comentarios, prej_sociol_kws_triples):
	var_sociolsPost = []
	for triple in prej_sociol_kws_triples:
		var_sociol = triple[1]
		keywords = triple[2] 
		var_sociolsPost.append(lexicalAnalysisAux(comentarios,var_sociol,keywords))
	return var_sociolsPost


#Função que retorna os tuplos de ocorrencias de keywords para o post
#Basicamente soma as ocorrencias dos comentarios para gerar as do post 
def getPostOcur(var_sociolsPost):
	postOcur = []
	for prejComents in var_sociolsPost:
		for comentario in prejComents[1]:
			postOcur.extend(comentario.occurrences)
	my_set = {x[0] for x in postOcur}
	postOcur = [(i,sum(x[1] for x in postOcur if x[0] == i)) for i in my_set]
	return postOcur

#Função de pretty printing para debbugging
def printOcurrencias(var_sociolsPost):
	str = ""
	for prejComents in var_sociolsPost:
		str += prejComents[0]
		str += "\n"
		for comentario in prejComents[1]:
			str += comentario.comment_id + " --> "
			for value in comentario.occurrences:
				str += "{}".format(value)
			str += "\n"
		str += "\n"
	
	print(str)

#Função que desenha o excell com as estatísticas
#Frequencias relativas, absolutas e totais dos comentarios para cada post
def excelWriter(var_sociolsPost,nComents,totais,worksheetName,workbook, file_name):
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
	for prejComents in var_sociolsPost:
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
			worksheet.write('E'+curr_str,str(comentario.occurrences))

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

#Função que desmembra o array var_sociolsPost em prejsKW 
# (array que representa as keywords por preconceito) 
def kwNprej(var_sociolsPost):
	prejsKW = {}
	for prej,com in var_sociolsPost:
		if com:
			prejsKW[prej] = []
			for elem in com:
				ocur = elem.occurrences
				for item in ocur:
					if item[0] not in prejsKW[prej]:
						prejsKW[prej].append(item[0])
	#print(prejsKW)
	return prejsKW

#Função de criação do objeto JSON
def jsonMetadataWriter(var_sociolsPost):
	json_obj = {
		"fname":"",
		"cmc":"",
		"lang":"",
		"date_p":"",
		"date_e":"",
		"title_type":"",
		"url_type":"",
		"setting":"",
		"platform":"",
		"svs":[],
		"kws":[],
		"extract_file_type":"",
		"source_type":"",
		"cpo":""
	}
	prejsKW = kwNprej(var_sociolsPost)
	
	for key, value in prejsKW.items():
		json_obj['svs'].append(key)
		for elem in value:
			json_obj['kws'].append(elem)
	
	print(json_obj)
	with open('metadata.json', 'w') as outfile:  
		json.dump(json_obj, outfile, indent=4, ensure_ascii=False)

#Função geral
def main():
	file_path = sys.argv[1]

	myclient = pymongo.MongoClient("mongodb://localhost:27017/")
	mydb = myclient["harambe"]
	mycol = mydb["keywords"]

	# criação do inventário das keywords
	kw_inventory = []
	#x = mycol.find()
	for x in mycol.find():
		kw_inventory.append(x)

	# criação do xslx
	workbook = xlsxwriter.Workbook('resultado.xlsx')

	counter = 0
	
	print('A analisar ficheiro.....')
	##Fazer análise do ficheiro escolhido
	print(file_path)

	com_inventory = loadInfo(file_path)
	comentarios = loadInfoExtract(com_inventory, 'id', 'commentText', 'user')
	prej_sociol_kws_triples = loadKeywordsRec(kw_inventory)
	
	var_sociolsPost = lexicalAnalysis(comentarios, prej_sociol_kws_triples)
	printOcurrencias(var_sociolsPost)
	totais = getPostOcur(var_sociolsPost)
	
	jsonMetadataWriter(var_sociolsPost)

	nComents = len(comentarios)
	excelWriter(var_sociolsPost, nComents, totais, f"sheet{counter}", workbook, file_path)

	#counter += 1

	#fechar o workbook
	workbook.close()
	myclient.close()

main()