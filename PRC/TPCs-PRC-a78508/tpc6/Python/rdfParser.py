#!/usr/bin/python3

from rdflib import *

graph = Graph()
#graph.open("store", create=True)
graph.parse("../Ontologia/mapa-grandeRdf.rdf")

# print out all the triples in the graph
#for subject, predicate, object in graph:
#    print ("{} {} {}".format(subject, predicate, object))

#import pprint
#for stmt in graph:
#    pprint.pprint(stmt)

#from rdflib import Literal
#from rdflib import URIRef
#from rdflib.namespace import RDF, FOAF
mapa = Namespace("http://prc.di.uminho.pt/2019/mapa#")
amares = Literal("AMARES")
for s,p,o in graph:
   if (o == amares):
       print("Merdas")
       if(s,RDF.type,mapa.Cidade) in graph:
           print("{}".format(s))
#bob = URIRef("http://example.org/people/bob")
#if ( bob, RDF.type, FOAF.Person ) in graph:
##   print "This graph knows that Bob is a person!"
