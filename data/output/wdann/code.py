#Automatic annotation of sentences with Wikidata items
#Created by Houcemeddine Turki


import json
import requests


endpoint_url = "https://query.wikidata.org/sparql"

def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

#Reading the pack file
f = open(r"C:\Users\Houcemeddine Turki\Downloads\cord19-ann.txt", "r")
g = open("wikidata-auto.txt", "w")
for n1 in range(5):
    print("Analysis of sentence "+str(n1+1)+"...\n")
    p = f.readline()
    #Eliminating punctuation
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
    p00 = ""
    for i in range(len(p23)):
        p00 += p23[i]
    p0 = p00.split('\n')
    p25 = ""
    for i in range(len(p0)):
        p25 += p0[i]
    p0n = p25.split('/')
    p24 = ""
    for i in range(len(p0n)):
        p24 += p0n[i] + " "
    #Splitting the sentence into words
    a = p24.split(" ")

    #Getting two grams
    str1 = ""
    for i in range(len(a)-1):
        str1 = str1+a[i] + " " + a[i+1]
        if (i < len(a)-2): str1=str1+";"
    b=str1.split(";")

    #Getting three grams
    str1 = ""
    for i in range(len(a)-2):
        str1 = str1+a[i] + " " + a[i+1] + " " + a[i+2]
        if (i < len(a)-3): str1=str1+";"
    c=str1.split(";")

    #Grouping all n-grams in a unique list
    for h9 in a:
        if h9.upper() in ["IN", "AN", "ON", "TO", "OF", "OFF", "AND", "OR", "NOT", "IF", "FOR", "THE"]: a.remove(h9)
    for h9 in a:
        if (len(h9)<=2): a.remove(h9)
    entities = a + b + c
    print(entities)

    
    #Defining several verification variables
    align = 0
    var1 = ""
    var2 = ""
    vv = ""
    
    #Aligning between concepts and Wikidata items
    print("Annotation of sentence "+str(n1+1)+" with Wikidata items...\n")
    for i in range(len(entities)):
         https = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search='+entities[i]+'&language=en&limit=50&format=json'
         r = requests.get(https)
         dat = r.json()
         n = 0
         for result in dat["search"]:
             try:
                 if (var1.find(result["id"])==-1):
                     if (var1!=""): var1 += ";"
                     var1 += result["id"]
                     if (var2!=""): var2 += ";"
                     var2 += entities[i]
             except KeyError:
                 print("KeyError")
             n += 1
             if n == 4: break
         align += n

    #Annotating semantic relations between Wikidata items
    print("Annotation of sentence "+str(n1+1)+" with Wikidata relations...\n")
    l = var1.split(";")
    lll = var2.split(";")
    for i in range(len(l)):
        url = "https://www.wikidata.org/w/api.php?action=wbgetclaims&entity="+l[i]+"&format=json"
        rrrr = requests.get(url)
        dat1 = rrrr.json()
        for t in dat1["claims"].keys():
            for result1 in dat1["claims"][t]:
                try:
                    if (result1["mainsnak"]["datavalue"]["value"]["id"] in l):
                        for hh in range(len(l)):
                            if (l[hh] == result1["mainsnak"]["datavalue"]["value"]["id"]) and (lll[i]!=lll[hh]):
                                g.write(str(n1+1)+";"+l[i]+";"+lll[i]+";"+t+";"+result1["mainsnak"]["datavalue"]["value"]["id"]+";"+lll[hh])
                except: vv = ""
                

g.close()
f.close()
