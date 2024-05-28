from typing import List
from rdflib import Graph, URIRef

requirements_graph = Graph()
requirements_graph.parse("/home/siebe/Documents/era-hackaton/requirements_.ttl", format="turtle")

era_ccstms_graph = Graph()
era_ccstms_graph.parse("/home/siebe/Documents/era-hackaton/era-ccstms_.ttl", format="turtle")

prefixes = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ccs: <http://data.europa.eu/949/>
"""

query_domains = prefixes + """
SELECT DISTINCT ?domain
WHERE {
    ?domain rdf:type ccs:Domain;
}
"""

query_attribute = prefixes + """
SELECT ?attribute
WHERE {{
    <{domain_uri}> ccs:hasAttribute ?attribute;
}}
"""

domains = requirements_graph.query(query_domains)

def resolve_uri(uri: str) -> dict:
    import json
    query = prefixes + """
        SELECT ?class ?attribute ?value 
        WHERE {{   
            ?class rdf:type <{uri}> .   
            ?class ?attribute ?value . 
        }}
    """.format(uri=uri)
    attributes = era_ccstms_graph.query(query)
    print(attributes.serialize(format="json-ld"))

result = []
for domain in domains:
    domain_uri = str(domain[0])
    result.append({"domain": domain_uri, "name": domain[0].split("/")[-1], "attributes": []})
    
    [result[-1]['attributes'].append(str(x[0])) for x in requirements_graph.query(query_attribute.format(domain_uri=domain_uri))]
    
    for attribute in result[-1]['attributes']:
        resolve_uri(attribute)
        
print(result)
    