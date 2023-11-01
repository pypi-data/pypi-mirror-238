#2. b. the string affiliation of a resource is replaced by the organization IRI (if exist)
# This would be done by every serialization of the graph anyways right?
INSERT { ?r schema:affiliation ?org}
WHERE {
  ?r schema:affiliation ?name. 
  ?org a schema:Organization. FILTER (ISIRI(?org)).
  ?org schema:name ?oname . FILTER (STR(?oname) =STR(?name))
  
};
DELETE {?r schema:affiliation ?affstr}
WHERE{ 
  ?r schema:affiliation ?affstr.  
  FILTER (!ISIRI(?affstr))
  ?org a schema:Organization.
  ?org schema:name ?oname . 
  FILTER (STR(?oname) =STR(?affstr))
}
