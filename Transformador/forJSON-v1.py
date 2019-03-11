#!/usr/local/bin/python3
#Esta versão oferece uma transformação aos ficheiros que não contenham uma row indicativa do nome de cada campo

import csv

def toJson(file):
	#seccao para saber apenas quantas rows tem o ficheiro
	idf_counter= open(file)
	counter= csv.reader(idf_counter,dialect='excel-tab')
	tam= sum(1 for row in counter)
	
	#percorrer todas as rows e extrair a informação
	idf= open(file)
	spamreader= csv.reader(idf,dialect='excel-tab')
	i=0
	print('[\n')
	for row in spamreader:
		printInfo(row,i,tam)
		i+=1
	print(']')

def printInfo(info,flag,tam):
	if(flag!=0):
		print('\t{')
		print('\t\t"position" : "%s",' % info[0])
		print('\t\t"post_id" : "%s",' % info[1])
		print('\t\t"post_by" : "%s" ,' % info[2])
		print('\t\t"ppost_text" : "%s",' % info[3])
		print('\t\t"post_published" : "%s",' % info[4])
		print('\t\t"comment_id" : "%s",' % info[5])
		print('\t\t"comment_by" : "%s",' % info[6])
		print('\t\t"is_reply" : %d ,' % int(info[7]))
		print('\t\t"comment_message" : "%s" ,' % info[8])
		print('\t\t"comment_published" : "%s" ,' % info[9])
		print('\t\t"comment_like_count" :%d ,' % int(info[10]))
		print('\t\t"attachment_type" : "%s" ,' % info[11])
		print('\t\t"attachment_url" : "%s" ,' % info[12])
		if(flag!=tam-1):
			print('\t},\n')
		else:
			print('\t}\n')

toJson("../Extratos/teste.tab")