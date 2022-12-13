from data_streamer.data_streamer import DataStreamer
from lib.stream_data import StreamData
from lib.data_enricher.shoutcast import ShoutcastDataEnricher

import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Please define filepath, host_ip and port as argument.')
        sys.exit(1)
    filepath: str = sys.argv[1]
    host_ip: str = sys.argv[2]
    port: int = int(sys.argv[3])
    data: StreamData = StreamData(filepath, 320000)
    data.prepare()
    shoutcast_data_enricher: ShoutcastDataEnricher = ShoutcastDataEnricher('shoutcast_stream', add_header=True)
    data_streamer: DataStreamer = DataStreamer(port, host_ip, data, is_server=True, data_enricher=shoutcast_data_enricher)
    data_streamer.run()
