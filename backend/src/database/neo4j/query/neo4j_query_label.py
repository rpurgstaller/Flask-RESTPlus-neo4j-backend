from backend.src.database.neo4j.query.neo4j_query import Neo4jQuery


class Neo4jQueryLabel(Neo4jQuery):
    def __init__(self, labels):

        label_str = ":".join([label for label in labels])
        stmt = 'Match (n:{}) return n'.format(label_str)

        Neo4jQuery.__init__(self, stmt)
