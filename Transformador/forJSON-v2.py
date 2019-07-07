#!/usr/local/bin/python3
#Esta versão oferece uma transformação aos ficheiros com a row indicativa dos nomes de cada campo

import csv
import re

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
		if (i==0):
			infoCabe=row
		printInfo(row,i,tam,infoCabe)
		i+=1
	print(']')

def normalizeAspas(info):
	str = info.replace('\"','\'')
	return str

def printInfo(info,flag,tam,infoCabe):
	args=len(info)
	i=0

	if(flag!=0):
		print('\t{')
		while(i<args):
			#if(representInt(info[i])):
				#print('\t\t"%s" : %d ,' % (infoCabe[i],int(info[i])))
			#else:
			if(i!=args-1):
				print('\t\t"%s" : "%s",' % (infoCabe[i],normalizeAspas(info[i])))
				i+=1
			else:
				print('\t\t"%s" : "%s"' % (infoCabe[i],normalizeAspas(info[i])))
				i+=1
	#Se for o ultimo elemento a ser processado nao contem ','
		if flag!=tam-1:
			print('\t},\n')
		else:
			print('\t}\n')

#Responsavel por saber se info[i] representa um número ou não. Importante para a representação correta em json?
def representInt(info):
		if(re.match(r'\d+',info)):
			print('reconheci inteiro')
			return True
		else:
			return False

toJson("../Extratos/facebook/facebook_extraction_portuguese_2.tab")

