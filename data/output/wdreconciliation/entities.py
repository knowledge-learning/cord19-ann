# Aligining annotated concepts with Wikidata items
# Created by Houcemeddine Turki

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import xlsxwriter

w = xlsxwriter.Workbook("wdentities.xlsx")
sheet = w.add_worksheet("alignment")

row1 = 0

with open(r'C:\Users\Houcemeddine Turki\Downloads\entities11.tsv', newline='') as csvfile:
     spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
     for row in spamreader:
         print(row[0])
         endpoint_url = "https://query.wikidata.org/sparql"
         query = '''SELECT DISTINCT ?item (UCASE(?label) AS ?title) WHERE {
         { ?item wdt:P2892 []. }
         UNION
         { ?item wdt:P6694 []. }
         UNION
         {
          ?item wdt:P351 [];
                wdt:P703 wd:Q15978631.
         }
         { ?item rdfs:label ?label. }
         UNION
         { ?item skos:altLabel ?label. }
         FILTER((LANG(?label)) = "en")
         FILTER(STRSTARTS(UCASE(?label), UCASE("'''+row[0]+'''")))
         }
         ORDER BY (?title)'''
         print(query)
         def get_results(endpoint_url, query):
             user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
             # TODO adjust user agent; see https://w.wiki/CX6
             sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
             sparql.setQuery(query)
             sparql.setReturnFormat(JSON)
             return sparql.query().convert()
         if (len(row[0])>2):
             results = get_results(endpoint_url, query)
             n = 0
             for result in results["results"]["bindings"]:
                 sheet.write(row1,0,row[0])
                 try:
                     sheet.write(row1,1,result["item"]["value"])
                     print(result["item"]["value"])
                 except KeyError:
                     sheet.write(row1,1,"KeyError")
                 try:
                     sheet.write(row1,2,result["label"]["value"])
                     print(result["label"]["value"])
                 except KeyError:
                     sheet.write(row1,2,"KeyError")
             row1 += 1
             n += 1
             if n == 4: break
 
w.close()
