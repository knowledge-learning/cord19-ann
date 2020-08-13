# Aligining annotated concepts with Wikidata items
# Created by Houcemeddine Turki and Alejandro Piad Morffis

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
import xlsxwriter

row1 = 0
list1 = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q"]
list2 = ["R","S","T","U","V","W","X","Y","Z"]
lis = list1 + list2

with open(sys.argv[2], "w") as writer:
    with open(sys.argv[1], newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in spamreader:
            entity = row[0].strip('"(),.;')
            print(entity)
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
            UNION
            { ?item wdt:P5008 wd:Q87748614.}
            { ?item rdfs:label ?label. }
            UNION
            { ?item skos:altLabel ?label. }
            FILTER((LANG(?label)) = "en")
            FILTER(STRSTARTS(UCASE(?label), UCASE("'''+entity+'''")))
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
            if (len(entity)>2):
                try:
                    results = get_results(endpoint_url, query)
                    e = 1
                except KeyboardInterrupt:
                    raise
                except:
                    print("EndPointInternalError")
                    continue

                for result in results["results"]["bindings"]:
                    c1 = result["title"]["value"][len(entity):len(entity)+1] in lis
                    if (len(entity)==len(result["title"]["value"])) or (c1==True):    
                        writer.write(f"{row1},0,{entity}\n")
                        try:
                            writer.write(f"{row1},1,{result['item']['value']}\n")
                            print(result["item"]["value"])
                        except KeyError:
                            writer.write(f"{row1},1,KeyError\n")
                        try:
                            writer.write(f"{row1},2,{result['title']['value']}\n")
                            print(result["title"]["value"])
                        except KeyError:
                            writer.write(f"{row1},2,KeyError\n")
                        row1 += 1
                        writer.flush()
