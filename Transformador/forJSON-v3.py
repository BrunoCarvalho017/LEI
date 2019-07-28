#!/usr/bin/python3
#Esta versão oferece uma transformação aos ficheiros com a row indicativa dos nomes de cada campo

import csv,re,sys,json

f = open("cenas.json", "a")

arr = []
obj = {}
comments = []
comment = {}
replies = []
flag_replies = 0
reply = 0

def toJson(file):
	#seccao para saber apenas quantas rows tem o ficheiro
	idf_counter = open(file)
	counter = csv.reader(idf_counter,dialect='excel-tab')
	tam = sum(1 for row in counter)

	#percorrer todas as rows e extrair a informação
	idf = open(file)
	spamreader= csv.reader(idf,dialect='excel-tab')
	i = 0

	for row in spamreader:
		if (i == 0):
			infoCabe = row
		else:			
			printInfo(row,tam,infoCabe)
		i += 1

	#Save to json file
	with open('data.json', 'w') as outfile:
		json.dump(comments, outfile, indent=4, ensure_ascii=False)
	print("data.json criado")

def normalizeAspas(info):
	str = info.replace('\"','\'')
	return str

def printInfo(info,tam,infoCabe):
	global flag_replies
	global reply
	global comment
	global replies
	global comments

	args = len(info)
	i = 0
	
	while(i<args):
		if infoCabe[i] == "is_reply":
			reply = info[i]
		comment[infoCabe[i]] = info[i]
		i += 1
		
	if (reply == '0'):
		if flag_replies == 1:
			comment["replies"] = replies
			replies = []
			flag_replies = 0
		#Save info row into comments object
		comments.append(comment)
		comment = {}
	else:
		flag_replies = 1
		replies.append(comment)
		comment = {}
		
#Responsavel por saber se info[i] representa um número ou não. Importante para a representação correta em json?
def representInt(info):
		if(re.match(r'\d+',info)):
			#print('reconheci inteiro')
			return True
		else:
			return False

toJson(sys.argv[1])