#Automatic annotation of sentences with Wikidata items
#Created by Houcemeddine Turki


import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import xlsxwriter

#Creating the XSLX File
w = xlsxwriter.Workbook("wdentities.xlsx")
sheet = w.add_worksheet("alignment")
var1 = ""

#Eliminating punctuation
p = input("What is the string")
p1 = p.split(",")
p2 = ""
for i in range(len(p1)):
    p2 += p1[i]
p3 = p2.split(":")
p4 = ""
for i in range(len(p3)):
    p4 += p3[i]
p5 = p4.split(";")
p6 = ""
for i in range(len(p5)):
    p6 += p5[i]
p7 = p6.split(".")
p8 = ""
for i in range(len(p7)):
    p8 += p7[i]
p9 = p8.split("'")
p10 = ""
for i in range(len(p9)):
    p10 += p9[i]
p11 = p10.split('"')
p12 = ""
for i in range(len(p11)):
    p12 += p11[i]
p13 = p12.split('(')
p14 = ""
for i in range(len(p13)):
    p14 += p13[i]
p15 = p14.split(')')
p16 = ""
for i in range(len(p15)):
    p16 += p15[i]
p17 = p16.split('{')
p18 = ""
for i in range(len(p17)):
    p18 += p17[i]
p19 = p18.split('}')
p20 = ""
for i in range(len(p19)):
    p20 += p19[i]
p21 = p20.split('[')
p22 = ""
for i in range(len(p21)):
    p22 += p21[i]
p23 = p22.split(']')
p24 = ""
for i in range(len(p23)):
    p24 += p23[i]

#Splitting the sentence into words
a = p24.split(" ")
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

#Initializing the XLSX File
row = 0
align = 0
x = 0

#Aligning between concepts and Wikidata items
for i in range(len(entities)):
         print(entities[i])
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
         FILTER(STRSTARTS(UCASE(?label), UCASE("'''+entities[i]+'''")))
         }
         ORDER BY (?title)'''
         def get_results(endpoint_url, query):
             user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
             # TODO adjust user agent; see https://w.wiki/CX6
             sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
             sparql.setQuery(query)
             sparql.setReturnFormat(JSON)
             return sparql.query().convert()
         if (len(entities[i])>2): results = get_results(endpoint_url, query)
         n = 0
         for result in results["results"]["bindings"]:
             sheet.write(row,0,entities[i])
             try:
                 sheet.write(row,1,result["item"]["value"])
                 if (var1.find(result["item"]["value"])==-1):
                     if (var1!=""): var1 += ";"
                     var1 += result["item"]["value"]
             except KeyError:
                 sheet.write(row,1,"KeyError")
             try:
                 sheet.write(row,2,result["label"]["value"])
             except KeyError:
                 sheet.write(row,2,"KeyError")
             x += 1
             row += 1
             n += 1
             if n == 4: break
         align += n
w.close()

#Annotating semantic relations between Wikidata items
l = var1.split(";")
print(var1)
for i in range(len(l)):
    for j in range(len(l)):
        if (i!=j):
            endpoint_url = "https://query.wikidata.org/sparql"
            query = """SELECT ?p ?label WHERE {
              <"""+l[i]+"""> ?prop <"""+l[j]+""">.
              ?p wikibase:directClaim ?prop.
              ?p rdfs:label ?label.
              FILTER(LANG(?label)="en")
            }"""
            print(query)
            results = get_results(endpoint_url, query)
            for result in results["results"]["bindings"]:
                print(result)
