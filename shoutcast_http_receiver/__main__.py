from lib.data_http_receiver import DataHttpReceiver
from lib.data_handler.shoutcast import ShoutcastDataHandler
from lib.metrics_handler import MetricsHandler
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define url as argument.')
        sys.exit(1)
    url: str = sys.argv[1]

    # data handler    
    shoutcast_data_handler: ShoutcastDataHandler = ShoutcastDataHandler(remove_header=False)
    
    # metrics handler
    counters = [{'id': 'bytes_received', 'name': 'bytes_received', 'description': 'Total bytes received.'},
                {'id': 'found_metadata', 'name': 'found_metadata', 'description': 'Found metadata block.'},
                {'id': 'found_empty_metadata', 'name': 'found_empty_metadata', 'description': 'Found metadata block of size 0 or empty string.'}]
    metrics_handler: MetricsHandler = MetricsHandler(counters, metric_prefix='e2e_shoutcast_receiver_')
    metrics_handler.run()

    # receiver
    data_receiver: DataHttpReceiver = DataHttpReceiver(url, {'icy-metadata':'1'}, data_handler=shoutcast_data_handler)
    data_receiver.run()
