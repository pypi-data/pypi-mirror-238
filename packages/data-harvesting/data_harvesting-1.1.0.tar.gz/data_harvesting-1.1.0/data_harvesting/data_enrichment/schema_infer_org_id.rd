# 2. a. if the affiliation is an IRI representing an organization, then
# schema:Organization type is added to that organization (IRI)
PREFIX schema: <http://schema.org/>
INSERT { ?org a schema:Organization }
WHERE {
  ?r schema:affiliation ?org.
  ?org a schema:Organization. FILTER (ISIRI(?org))
  ?org schema:name ?oname.
}
# . FILTER(!ISIRI(?org))
