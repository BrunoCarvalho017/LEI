#!/usr/bin/python3

import json 
from rdflib import *
def printClasses():
    str = ""
    str += "### http://prc.di.uminho.pt/2019/mapa#Freguesia\n"
    str += ":Freguesia rdf:type owl:Class .\n\n"
    str += "### http://prc.di.uminho.pt/2019/mapa#Concelho\n"
    str += ":Concelho rdf:type owl:Class .\n\n"
    return str
def printObjectProperties():
    str = ""
    str += "### http://prc.di.uminho.pt/2019/mapa#pertenceConcelho\n"
    str += ":pertenceConcelho rdf:type owl:ObjectProperty .\n\n"
    return str

def printDataProperties():
    str = ""
    str += "### http://prc.di.uminho.pt/2019/mapa#brasao\n"
    str += ":brasao rdf:type owl:DatatypeProperty .\n\n"
    str += "### http://prc.di.uminho.pt/2019/mapa#dicofre\n"
    str += ":dicofre rdf:type owl:DatatypeProperty .\n\n"
    return str

def printFreguesias(json_data):
    str = ""
    for entry in json_data['d']:
        str += "### http://prc.di.uminho.pt/2019/mapa#fre" + entry['dicofre'] + "\n"
        str += ":fre" + entry['dicofre'] + " rdf:type owl:NamedIndividual ,\n"
        str += "\t\t\t:Freguesia ;\n"
        str += "\t\t:nome " +"\""+ entry['freguesia'] +"\""+ " ;\n" 
        if 'brasao' in entry.keys():
            str += "\t\t:brasao " +"\""+ entry['brasao'] +"\""+ " ;\n" 
        concelho_key = entry['concelho'].replace(" ","")
        str += "\t\t:pertenceConcelho :conc" + concelho_key + " ;\n"
        str += "\t\t:dicofre " +"\""+ entry['dicofre'] +"\""+ " .\n\n"
    
    return str

def getConcelhos(json_data):
    concelhos = []
    for entry in json_data['d']:
        value = (entry['concelho'],entry['distrito'])
        concelhos.append(value)
    return concelhos

def printConcelhos(concelhos):
    str = ""
    for tuple in concelhos:
        concelho = tuple[0]
        concelho_key = concelho.replace(" ","")
        distrito = tuple[1]
        str += "### http://prc.di.uminho.pt/2019/mapa#conc" + concelho_key + "\n"
        str += ":conc" + concelho_key + " rdf:type owl:NamedIndividual , \n"
        str += "\t\t\t:Concelho ;\n"
    
        distrito_up = distrito.upper()
        distritoURI = existDistrito(rdf_data,distrito_up)
        if distritoURI:
            distritoURI = distritoURI.split('#')[1]
            str += "\t\t:pertenceDistrito :" + distritoURI + " ;\n"

        str += "\t\t:nome " +"\""+ concelho +"\""+ " .\n\n"
    return str

def getDistritos(json_data):
    distritos = []
    for entry in json_data['d']:
        distritos.append(entry['distrito'])
    return distritos

def printDistritos(distritos, rdf_data):
    str = ""
    for distrito in distritos:
        distrito_up = distrito.upper()
        distritoURI = existDistrito(rdf_data,distrito_up)
        distrito_key = distrito.replace(" ","")
        if not distritoURI:
            str += "### http://prc.di.uminho.pt/2019/mapa#dist" + distrito_key + "\n"
            str += ":dist" + distrito_key + " rdf:type owl:NamedIndividual , \n"
            str += "\t\t\t:Distrito ;\n"
            str += "\t\t:nome " +"\""+ distrito +"\""+ " .\n\n"
    return str

def existDistrito(rdf_data, distrito):
    distritoURI = ""
    distrito = Literal(distrito)
    for s,p,o in rdf_data:
        if o in distrito or distrito in o:
            if (s,RDF.type,mapa.Distrito):
                distritoURI = s
                break
    return distritoURI 


json_file = open("../Extratos/freguesias-metadata.xlsx.json")
json_data = json.load(json_file)


graph = Graph()
graph.parse("../Ontologia/mapa-grande.rdf")
rdf_data = graph
mapa = Namespace("http://prc.di.uminho.pt/2019/mapa#")    

concelhos = getConcelhos(json_data)
concelhos = list(set(concelhos))

distritos = getDistritos(json_data)
distritos = list(set(distritos))

classes = printClasses()
dataProps = printDataProperties()
objProps = printObjectProperties()
fre = printFreguesias(json_data)
conc = printConcelhos(concelhos)
dist = printDistritos(distritos, rdf_data)

str = ""
str = classes + dataProps + objProps + fre + conc + dist

print(str)
