#!/usr/bin/python3
#Esta versão oferece uma transformação aos ficheiros com a row indicativa dos nomes de cada campo

import csv,re,sys,json
import time

obj = {}
comments = []
comment = {}
replies = []
header = {}
flag_replies = 0
reply = 0
int_replies = 0

header['title'] = ""
header['subtitle'] = ""
header['owner'] = ""
header['views'] = "NA"
header['likes'] = ""
header['dislikes'] = "NA"
header['shares'] = ""
header['datePosted'] = ""
header['dateExtraction'] = ""
header['language'] = ""
header['plataform'] = ""
header['url'] = ""
header['postText'] = ""
header['numberPosts'] = ""
header['srcType'] = ""
header['nameNewspaper'] = "NA"
header['socioLingVar'] = ""
header['listEvents'] = ""
header['articleKeywords'] = "NA"
header['keywords'] = ""
header['commentsOpen'] = ""
header['id'] = ""

obj['header'] = header

def toJson(file):
	localtime = time.localtime(time.time())
	json_name =  str(localtime.tm_year) + str(localtime.tm_mon) + str(localtime.tm_mday) + str(localtime.tm_hour) + str(localtime.tm_min) + str(localtime.tm_sec)
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
			printInfo(i,row,tam,infoCabe)
		i += 1

	obj['commentThread'] = comments

	#Save to json file
	with open('public/exports/'+json_name+'.json', 'w') as outfile:
		json.dump(obj, outfile, indent=4, ensure_ascii=False)
	print(json_name)

def normalizeAspas(info):
	str = info.replace('\"','\'')
	return str

def printInfo(first,info,tam,infoCabe):
	global flag_replies
	global reply
	global comment
	global replies
	global comments
	global int_replies


	args = len(info)
	i = 0
	
	while(i<args):
		if infoCabe[i] == "is_reply":
			reply = info[i]
		#Header Construction
		if infoCabe[i] == "post_text" and first == 1:
			header['title'] = info[i]
		if infoCabe[i] == "post_by" and first == 1:
			header['owner'] = info[i]
		if infoCabe[i] == "post_published" and first == 1:
			header['datePosted'] = info[i]
		#Comment Construction
		if infoCabe[i] == "comment_id":
			comment['id'] = info[i]
		if infoCabe[i] == "comment_by":
			comment['user'] = info[i]
		if infoCabe[i] == "comment_published":
			comment['date'] = info[i]
		if infoCabe[i] == "comment_message":
			comment['commentText'] = info[i]
		if infoCabe[i] == "comment_like_count":
			comment['likes'] = int(info[i])
		i += 1

	comment['timestamp'] = 0
	comment['hasKW'] = 0

	if (reply == '0'):
		comment['hasReplies'] = False
		if flag_replies == 1:
			comment["hasReplies"] = True
			comment["numberOfReplies"] = int_replies 
			comment["replies"] = replies
			replies = []
			int_replies = 0
			flag_replies = 0
		#Save info row into comments object
		comments.append(comment)
		comment = {}
	else:
		flag_replies = 1
		int_replies += 1
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