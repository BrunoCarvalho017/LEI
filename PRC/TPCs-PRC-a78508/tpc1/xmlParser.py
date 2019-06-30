#!/usr/bin/python3

import xml.etree.ElementTree as ET
uri = "##  http://prc.di.uminho.pt/2019/pubs#"

def getClassTags(root):
    tags = []
    for childs in root:
        if len(list(childs)):
                tags.append(childs.tag)
                tags += getClassTags(childs)
        elif (len(childs.attrib)):
            tags.append(childs.tag)

    return tags

def getDataTags(root):
    tags = []
    for childs in root:
        if len(list(childs)):
            tags += getDataTags(childs)
        elif (not childs.attrib): 
            tags.append(childs.tag)
    return tags

def printClass(class_tags):
    str = ""
    for tag in class_tags:
        str += uri+tag.title()+"\n"
        str += ":"+tag.title()+" rdf:type owl:Class .\n\n\n"
    return str

def printDataProp(data_tags):
    str = ""
    for tag in data_tags:
        str += uri+tag+"\n"
        str += ":"+tag+" rdf:type owl:DatatypeProperty .\n\n\n"
    return str

def printAll(class_tags,data_tags):
    str = ""
    str += "@prefix : <http://prc.di.uminho.pt/2019/pubs#> .\n"
    str += "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
    str += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
    str += "@prefix xml: <http://www.w3.org/XML/1998/namespace> .\n"
    str += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
    str += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
    str += "@base <http://prc.di.uminho.pt/2019/pubs> .\n\n"

    str += "<http://prc.di.uminho.pt/2019/pubs> rdf:type owl:Ontology .\n\n"

    str += "#################################################################\n"
    str += "#    Classes\n"
    str += "#################################################################\n\n\n"

    str += printClass(class_tags)

    str += "#################################################################\n"
    str += "#    Data properties\n"
    str += "#################################################################\n\n\n"
    str += uri+"name\n"
    str += ":name rdf:type owl:DatatypeProperty .\n\n\n"

    str += printDataProp(data_tags)

    str += "#################################################################\n"
    str += "#    Object properties\n"
    str += "#################################################################\n\n\n"
    str += uri + "hasAuthor\n"
    str += ":hasAuthor rdf:type owl:ObjectProperty .\n\n\n"
    str += uri + "hasEditor\n"
    str += ":hasEditor rdf:type owl:ObjectProperty .\n\n\n"
    
    str += "#################################################################\n"
    str += "#    Individuals\n"
    str += "#################################################################\n\n\n"
    return str


root = ET.parse('jcrpubs.xml').getroot()
output = open("parserOut.ttl", "w")

class_tags = getClassTags(root)
class_tags = list(set(class_tags))
class_tags.remove('author-ref')
class_tags.remove('editor-ref')
class_tags.sort()

data_tags = getDataTags(root)
data_tags = list(set(data_tags))
data_tags.sort()

print("::CLASS TAGS::")
print(class_tags)

print()

print("::DATA TAGS::")
print(data_tags)

print("\n\n")

str = printAll(class_tags,data_tags)
output.write(str)
output.close()
