from data_streamer.data_streamer import DataStreamer
from lib.stream_data import StreamData
from lib.data_enricher.shoutcast import ShoutcastDataEnricher

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define port as argument.')
        sys.exit(1)
    port: int = int(sys.argv[1])
    data: StreamData = StreamData('test_files/sweep_5sec.mp3', 320000)
    data.prepare()
    shoutcast_data_enricher: ShoutcastDataEnricher = ShoutcastDataEnricher('shoutcast_stream', add_header=True)
    data_streamer: DataStreamer = DataStreamer(port, data, is_server=True, data_enricher=shoutcast_data_enricher)
    data_streamer.run()
