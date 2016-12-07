from datetime import datetime
from google.cloud import datastore
import utility


class Capital:

    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "Note"

    def insert_capital(self, comment):
        key = self.ds.key(self.kind)
        entity = datastore.Entity(key)

        entity['text'] = comment
        entity['timestamp'] = datetime.utcnow()

        return self.ds.put(entity)

    def fetch_capitals(self):
        query = self.ds.query(kind=self.kind)
        query.order = ['-timestamp']
        return self.get_query_results(query)

    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(dict(entity))
        return results


def parse_captals_time(note):
    """converts a greeting to an object"""
    return {
        'text': note['text'],
        'timestamp': note['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    }
