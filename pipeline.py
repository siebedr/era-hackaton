from typing import List
from rdflib import Graph, URIRef

requirements_graph = Graph()
requirements_graph.parse("requirements_.ttl", format="turtle")

era_ccstms_graph = Graph()
era_ccstms_graph.parse("era-ccstms_.ttl", format="turtle")

prefixes = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ccs: <http://data.europa.eu/949/>
"""

def resolve_uri(uri: str) -> dict:
    query = prefixes + """
        SELECT ?p ?o
        WHERE {{   
            <{uri}> ?p ?o 
            }}
    """.format(uri=uri)
    attributes = era_ccstms_graph.query(query)   
    
    dict_result = {}
    for key, value in attributes:
        dict_result[str(key).split("#")[-1]] = str(value)
        
    print(dict_result)
    return dict_result

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

result = []
for domain in domains:
    domain_uri = str(domain[0])
    result.append({"domain": domain_uri, "name": domain[0].split("/")[-1], "attributes": []})
    
    tmp_attributes = [str(x[0]) for x in requirements_graph.query(query_attribute.format(domain_uri=domain_uri))]
    
    for attribute in tmp_attributes:
        tmp = resolve_uri(attribute)
        if tmp:
            result[-1]['attributes'].append(tmp)
            
print(result)