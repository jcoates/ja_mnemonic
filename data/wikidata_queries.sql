# surnames
SELECT DISTINCT ?name ?nameLabel ?nativeLabel ?kana (COUNT(*) AS ?count)
WHERE
{
  ?name wdt:P31/wdt:P279* wd:Q101352.
  ?person wdt:P734 ?name.
  ?name wdt:P407 wd:Q5287.
  ?name wdt:P1705 ?native.
  OPTIONAL { ?name p:P1705/pq:P1814 ?deepkana.}
  OPTIONAL { ?name wdt:P1814 ?shallowkana.}
  BIND(COALESCE(?shallowkana, ?deepkana, "<not found>") AS ?kana). 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,jp" } #adds labels
}
GROUP BY ?name ?nameLabel ?nativeLabel ?native ?kana
ORDER BY DESC(?count)

# given names
SELECT DISTINCT ?name ?nameLabel ?nativeLabel  (COUNT(*) AS ?count)
WHERE
{
  ?name wdt:P31/wdt:P279* wd:Q202444.
  ?person wdt:P735 ?name.
  ?name wdt:P407 wd:Q5287.
  ?name wdt:P1705 ?native.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en,jp" } #adds labels
}
GROUP BY ?name ?nameLabel ?nativeLabel ?native
ORDER BY DESC(?count)