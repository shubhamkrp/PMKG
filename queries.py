from neo4j import GraphDatabase


URI = "bolt://localhost:7687"
AUTH = ("neo4j", "InitialKB")

people = [{"name": "Alice", "age": 42, "friends": ["Bob", "Peter", "Anna"]},
          {"name": "Bob", "age": 19},
          {"name": "Peter", "age": 50},
          {"name": "Anna", "age": 30}]

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    try:
        # #Load CSV
        # driver.execute_query("""LOAD CSV WITH HEADERS FROM 'file:///relationship1.csv' as row
        #                         MERGE (s:Symptom {name: row.Symptom})
        #                         with s, split(row.Disease,';') AS diseases
        #                         UNWIND diseases AS disease
        #                         MERGE (d:Disease {name: trim(disease)})
        #                         MERGE (s)-[:HAS_DISEASE]->(d)""")

        # intersection of diseases from list of symptoms
        records, summary, keys = driver.execute_query("""WITH ['hemmorhage', 'bleeding','hemorrhagic gastroenteritis'] as names
                                                        MATCH (s:Symptom)
                                                        WHERE s.name in names
                                                        WITH collect(s) as symptoms
                                                        WITH head(symptoms) as head, tail(symptoms) as symptoms
                                                        MATCH (head)-[:HAS_DISEASE]->(d:Disease)
                                                        WHERE ALL(s in symptoms WHERE (s)-[:HAS_DISEASE]->(d))
                                                        RETURN d""",
                                                        database_="neo4j")
        # Create some nodes
        # for person in people:
        #     records, summary, keys = driver.execute_query(
        #         "MERGE (p:Person {name: $person.name, age: $person.age})",
        #         person=person,
        #         database_="neo4j",
        #     )

        # # Create some relationships
        # for person in people:
        #     if person.get("friends"):
        #         records, summary, keys = driver.execute_query("""
        #             MATCH (p:Person {name: $person.name})
        #             UNWIND $person.friends AS friend_name
        #             MATCH (friend:Person {name: friend_name})
        #             MERGE (p)-[:KNOWS]->(friend)
        #             """, person=person,
        #             database_="neo4j",
        #         )

        # # Retrieve Alice's friends who are under 40
        # records, summary, keys = driver.execute_query("""
        #     MATCH (p:Person {name: $name})-[:KNOWS]-(friend:Person)
        #     WHERE friend.age < $age
        #     RETURN friend
        #     """, name="Alice", age=40,
        #     routing_="r",
        #     database_="neo4j",
        # )
        # Loop through results and do something with them
        for record in records:
            print(record)
        # Summary information
        print("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))

    except Exception as e:
        print(e)
        # further logging/processing