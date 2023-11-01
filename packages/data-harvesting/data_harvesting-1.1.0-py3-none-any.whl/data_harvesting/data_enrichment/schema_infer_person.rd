# 1. The rule for identifying resources that have to be of type schema:Person
PREFIX schema: <http://schema.org/>
INSERT { ?p a schema:Person}
WHERE {
  ?r schema:creator|schema:author  ?p.
  ?p schema:affiliation ?aff.
  ?p schema:name ?name
}
