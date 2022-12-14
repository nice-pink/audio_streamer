from typing import List
from prometheus_client import Counter, start_http_server

class MetricsHandler:
    
    def __init__(self, counters: List[dict], metric_prefix: str = "") -> None:
        # counters = [{'id': 'bytes_sent', 'name': 'bytes_handled', 'description': 'Total bytes handled.'}]
        self.metric_prefix: str = metric_prefix
        self.counters: dict = {}

        for metric in counters:
            self.add_metric(metric)

    def run(self, port: int = 8000):
        start_http_server(port)

    def add_metric(self, metric: dict) -> None:
        if metric['id'] in self.counters:
            # metric already exists
            return
        print('Add metric with id', metric['id'], 'and name', metric['name'])
        self.counters[metric['id']] = Counter(self.metric_prefix+metric['name'], metric['description'])

    def increase(self, counter: dict) -> None:
        if counter['id'] in self.counters:
            self.counters[counter['id']].inc(counter['value'])
