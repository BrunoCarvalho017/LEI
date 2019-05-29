#!/usr/bin/python3
##!/usr/local/bin/python3
#Esta versão oferece uma transformação aos ficheiros com a row indicativa dos nomes de cada campo

import json
import sys

def printArray(array):
	str = ""
	for elem in array:
		str += elem + " "
	return str 

def buildMeta(file):
	file = f"../Analisador/{file}"
	with open(file) as json_file:  
		obj = json.load(json_file)
	
	str = ""
	str += "---" + obj['fname'] + "\n\n"
	str += "CMC Source Text type: " + obj['cmc'] + "\n"
	str += "Language: " + obj['lang'] + "\n"
	str += "Date Posted: " + obj['date_p'] + "\n"
	str += "Date Extraction: " + obj['date_e'] + "\n"
	str += "Title  type='fbPost': " + obj['title_type'] + "\n"
	str += "URL type='fbPost': " + obj['url_type'] + "\n"
	str += "Setting: " + obj['setting'] + "\n"
	str += "Type of online platform/channel: " + obj['platform'] + "\n"
	str += "Sociolinguistic variables: " + printArray(obj['svs']) + "\n"
	str += "Keywords/Expressions of Comments: " + printArray(obj['kws']) + "\n"
	str += "Extracted file type: " + obj['extract_file_type'] + "\n"
	str += "Source type: " + obj['source_type'] + "\n"
	str += "Comments permanently open: " + obj['cpo'] + "\n"
	
	out_fname = f"metadata_{obj['fname']}.txt"
	with open(out_fname, "w") as text_file:
		text_file.write(str)

buildMeta(sys.argv[1])
