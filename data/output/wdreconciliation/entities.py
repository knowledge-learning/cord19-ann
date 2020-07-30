# Aligining annotated concepts with Wikidata items
# Created by Houcemeddine Turki

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import csv

file = open("wdentities.csv","w")

with open(r'C:\Users\Houcemeddine Turki\Downloads\entities11.tsv', newline='') as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     for row in spamreader:
         print(row[0])
         endpoint_url = "https://query.wikidata.org/sparql"
         query = '''SELECT * WHERE {
            {?item wdt:P2892 [].} UNION {?item wdt:P6680 [].}
            {?item rdfs:label ?label} UNION { ?item skos:altLabel ?label. }
            FILTER(LANG(?label)="en")
            FILTER(CONTAINS(UCASE(?label),UCASE("'''+row[0]+'''")))
         }'''
         print(query)
         def get_results(endpoint_url, query):
             user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
             # TODO adjust user agent; see https://w.wiki/CX6
             sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
             sparql.setQuery(query)
             sparql.setReturnFormat(JSON)
             return sparql.query().convert()
         results = get_results(endpoint_url, query)
         for result in results["results"]["bindings"]:
             s = row[0] + ';' + result["item"]["value"] + ';' + result["label"]["value"]
             file.write(s)
 
file.close() 
