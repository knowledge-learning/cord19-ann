#Automatic annotation of sentences with Wikidata items
#Created by Houcemeddine Turki


import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import xlsxwriter

#Creating the CSV File
w = xlsxwriter.Workbook("wdentities.xlsx")
sheet = w.add_worksheet("alignment")


#Splitting the sentence into words
p = input("What is the string")
a = p.split(" ")
print(a)

#Getting two grams
str1 = ""
for i in range(len(a)-1):
    str1 = str1+a[i] + " " + a[i+1]
    if (i < len(a)-2): str1=str1+";"
    print(str1)
b=str1.split(";")
print(b)

#Getting three grams
str1 = ""
for i in range(len(a)-2):
    str1 = str1+a[i] + " " + a[i+1] + " " + a[i+2]
    if (i < len(a)-3): str1=str1+";"
    print(str1)
c=str1.split(";")
print(c)

#Grouping all n-grams in a unique list
entities = a + b + c
print(entities)

#Initializing the CSV File
row = 0

#Aligning between concepts and Wikidata items
for i in range(len(entities)):
         print(entities[i])
         endpoint_url = "https://query.wikidata.org/sparql"
         query = '''SELECT DISTINCT ?item (UCASE(?label) AS ?title) WHERE {
            {?item wdt:P2892 [].} UNION {?item wdt:P6680 [].} UNION {?item wdt:P351 []; wdt:P703 wd:Q15978631.}
            {?item rdfs:label ?label} UNION { ?item skos:altLabel ?label. }
            FILTER(LANG(?label)="en")
            FILTER(STRSTARTS(UCASE(?label),UCASE("'''+entities[i]+'''")))
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
         n = 0
         for result in results["results"]["bindings"]:
             sheet.write(row,0,entities[i])
             try:
                 sheet.write(row,1,result["item"]["value"])
             except KeyError:
                 sheet.write(row,1,"KeyError")
             try:
                 sheet.write(row,2,result["label"]["value"])
             except KeyError:
                 sheet.write(row,2,"KeyError")
             row += 1
             n += 1
             if n == 4: break
 
w.close()
