from lib.data_streamer import DataStreamer
from lib.stream_data import StreamData
from lib.data_enricher.shoutcast import ShoutcastDataEnricher
from lib.metrics_handler import MetricsHandler

import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Please define filepath, host_ip and port as argument.')
        sys.exit(1)
    filepath: str = sys.argv[1]
    host_ip: str = sys.argv[2]
    port: int = int(sys.argv[3])
    
    # prepare stream data
    data: StreamData = StreamData(filepath, 320000)
    data.prepare()

    # metrics
    # metrics handler
    counters = [{'id': 'bytes_sent', 'name': 'bytes_sent', 'description': 'Total bytes handled.'},
                {'id': 'enriched', 'name': 'icy_metadata_sent', 'description': 'Total icy metadata blocks sent.'},
                {'id': 'companion_sent', 'name': 'zetta_metadata_sent', 'description': 'Total zetta metadata blocks sent.'},
                {'id': 'cycles', 'name': 'cycles', 'description': 'Total repitiontions of sending file.'}]
    metrics_handler: MetricsHandler = MetricsHandler(counters, metric_prefix='e2e_zetta_streamer_')
    metrics_handler.run()
    
    # data enricher
    shoutcast_data_enricher: ShoutcastDataEnricher = ShoutcastDataEnricher('shoutcast_stream', add_header=True)
    
    # streamer
    data_streamer: DataStreamer = DataStreamer(port,
                                               host_ip,
                                               data,
                                               is_server=True,
                                               data_enricher=shoutcast_data_enricher,
                                               metrics_handler=metrics_handler)
    data_streamer.run()
