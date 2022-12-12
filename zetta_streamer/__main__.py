from data_streamer.data_streamer import DataStreamer
from lib.stream_data import StreamData
from lib.data_enricher.shoutcast import ShoutcastDataEnricher
from lib.metadata_handler.zetta_metadata import ZettaMetadata, ZettaLogEventType
from lib.companion_sender.zetta_metadata import ZettaMetadataSender

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define port as argument.')
        sys.exit(1)
    port: int = int(sys.argv[1])
    data: StreamData = StreamData('test_files/sweep_5sec.mp3', 320000)
    data.prepare()
    shoutcast_data_enricher: ShoutcastDataEnricher = ShoutcastDataEnricher('shoutcast_stream', add_header=True)
    zetta_metadata_sender: ZettaMetadataSender = ZettaMetadataSender(id='id', url='http://127.0.0.1:8000', file_duration=5.0)
    
    # metadata test
    # zetta_metadata: ZettaMetadata = ZettaMetadata()
    # zetta_metadata.build(1, [ZettaLogEventType.Default, ZettaLogEventType.LastStarted], 5.0)
    
    data_streamer: DataStreamer = DataStreamer(port, data, is_server=True, data_enricher=shoutcast_data_enricher, companion_sender=zetta_metadata_sender)
    data_streamer.run()
