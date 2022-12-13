from typing import List
from prometheus_client import Counter

class MetricsHandler:
    
    def __init__(self, counters: List[dict], metric_prefix: str = "") -> None:
        # counters = [{'id': 'bytes_sent', 'name': 'bytes_handled', 'description': 'Total bytes handled.'}]
        self.counters: dict = {}

        for metric in counters:
            self.counters[metric['id']] = Counter(metric_prefix+metric['name'], metric['description'])

    def increase(self, counter: dict) -> None:
        if counter['id'] in self.counters:
            self.counters[counter['id']].inc(counter['value'])
