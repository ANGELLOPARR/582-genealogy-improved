from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

# Useful links
# https://query.wikidata.org/ - sparql testing/formatting sandbox: use it to preview output columns/add fields
# https://www.wikidata.org/wiki/Wikidata:WikiProject_Genealogy - list of wikidata properties related to genealogies

# Example sparql query for getting all ancestors of Willem-Alexander of the Netherlands
# https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Ancestors_of_Willem-Alexander_of_the_Netherlands


# Testing notes:
# itemLabel should be the person's full name (verified in the sandbox), but the code below shows their wikidata ID instead
# "given name" property usually has the person's first name
# "family name" property rarely has the person's last name
# Other name-related fields are almost always empty, which is why we need itemLabel as a name instead of Wikidata ID


def test_sparql():
    s = SPARQLWrapper("https://query.wikidata.org/sparql")

    s.setQuery("""
        SELECT DISTINCT ?item ?itemLabel ?dateofbirth ?name ?given_name ?given_nameLabel ?family_name ?family_nameLabel ?birth_name ?named_after ?named_afterLabel WHERE {
          wd:Q154952 ((wdt:P22|wdt:P25)*) ?item.
          OPTIONAL { ?item wdt:P569 ?dateofbirth. }
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          OPTIONAL { ?item wdt:P2561 ?name. }
          OPTIONAL { ?item wdt:P735 ?given_name. }
          OPTIONAL { ?item wdt:P734 ?family_name. }
          OPTIONAL { ?item wdt:P1477 ?birth_name. }
          OPTIONAL { ?item wdt:P138 ?named_after. }
        }
        ORDER BY (?itemLabel)
        """)

    # SparQL queries returned as JSON, maybe could look there for missing name value
    s.setReturnFormat(JSON)
    results = s.query().convert()

    # Not super sure how this actually handles JSON, but seems to work except for itemLabel
    results_df = pd.json_normalize(results['results']['bindings'])
    print(results_df.columns)

    # To get certain columnames listed in SparQL, usually <column_name>.value as index
    print(results_df[["itemLabel.value", "dateofbirth.value"]].head())


if __name__ == '__main__':
    test_sparql()
