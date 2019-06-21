#!/usr/bin/python3
##!/usr/local/bin/python3

import json,sys,xlsxwriter,os,glob
import re
from io import BytesIO

fileDirectory = "../Extratos/youtube2/"
outfileDirectory = "../Extratos/youtube3/"
#Função de inicialização do python para tratar ficheiro JSON
def loadInfo(file):
	info = open(file).read()
	inventory = json.loads(info)
	return inventory

files = os.listdir("../Extratos/youtube2")
print(files)
inventory =  {}
for file in files:
	print(file)
	if file != ".DS_Store":
		inventory = loadInfo(fileDirectory + file)
		inventory["header"]["id"] = ""
		for key in inventory.keys():
			if type(inventory[key]) is list:
				for item in inventory[key]:
					item["hasKW"] = 0
					for key2 in item.keys():
						if type(item[key2]) is list:
							for item2 in item[key2]:
								item2["hasKW"] = 0
		with open(outfileDirectory + file, 'w') as outfile:  
			json.dump(inventory, outfile, indent=4)
		inventory = {}
