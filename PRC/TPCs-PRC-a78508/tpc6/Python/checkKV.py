#!/usr/bin/python3

import json

with open('freguesias.json') as json_file:
    doc1 = json.load(json_file)

with open('freguesias-metadata.xlsx.json') as json_file:
    doc2 = json.load(json_file)

doc1_KV = []
doc2_KV = []

for entry in doc1['d']:
    for key,value in entry.items():
        doc1_KV.append(str(key+":"+value))
        #doc1_V.append(field.value())
        #doc1_K.append(field.key())

for entry in doc2['d']:
    for key, value in entry.items():
        doc2_KV.append(str(key+":"+value))
        #doc2_V.append(field.value())
        #doc2_K.append(field.key())

print(set(doc1_KV) == set(doc2_KV))

#print(doc1_V)
#print(doc1_K)
#print(doc2_V)
#print(doc2_K)

