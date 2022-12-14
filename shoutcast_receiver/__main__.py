from lib.data_receiver import DataReceiver
from lib.data_handler.shoutcast import ShoutcastDataHandler
from lib.metrics_handler import MetricsHandler
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please define host_ip and port as argument.')
        sys.exit(1)
    host_ip: str = sys.argv[1]
    port: int = int(sys.argv[2])

    # data handler
    shoutcast_data_handler: ShoutcastDataHandler = ShoutcastDataHandler(remove_header=True)

    # metrics handler
    counters = [{'id': 'bytes_received', 'name': 'bytes_received', 'description': 'Total bytes received.'},
                {'id': 'found_metadata', 'name': 'found_metadata', 'description': 'Found metadata block.'},
                {'id': 'found_empty_metadata', 'name': 'found_empty_metadata', 'description': 'Found metadata block of size 0 or empty string.'}]
    metrics_handler: MetricsHandler = MetricsHandler(counters, metric_prefix='e2e_zetta_streamer_')
    metrics_handler.run()

    # receiver
    data_receiver: DataReceiver = DataReceiver(port,
                                               host_ip,
                                               is_server=False,
                                               data_handler=shoutcast_data_handler,
                                               metrics_handler=metrics_handler)
    data_receiver.run()
