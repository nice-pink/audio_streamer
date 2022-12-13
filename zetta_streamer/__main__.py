from data_streamer.data_streamer import DataStreamer
from lib.stream_data import StreamData
from lib.data_enricher.shoutcast import ShoutcastDataEnricher
from lib.metadata_handler.zetta_metadata import ZettaMetadata, ZettaLogEventType
from lib.companion_sender.zetta_metadata import ZettaMetadataSender

import sys

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Please define filepath, host_ip, port, metadata_receiver_url, metadata_receiver_port as argument.')
        sys.exit(1)
    filepath: str = sys.argv[1]
    host_ip: str = sys.argv[2]
    port: int = int(sys.argv[3])
    metadata_receiver_url: str = sys.argv[4]
    metadata_receiver_port: str = sys.argv[5]
    data: StreamData = StreamData(filepath, 320000)
    data.prepare()

    if not metadata_receiver_url.startswith('http'):
        metadata_receiver_url = 'http://' + metadata_receiver_url
    if metadata_receiver_port:
        metadata_receiver_url += ':' + metadata_receiver_port

    shoutcast_data_enricher: ShoutcastDataEnricher = ShoutcastDataEnricher('shoutcast_stream', add_header=True)
    zetta_metadata_sender: ZettaMetadataSender = ZettaMetadataSender(id='id', url=metadata_receiver_url, file_duration=5.0)

    # metadata test
    # zetta_metadata: ZettaMetadata = ZettaMetadata()
    # zetta_metadata.build(1, [ZettaLogEventType.Default, ZettaLogEventType.LastStarted], 5.0)

    data_streamer: DataStreamer = DataStreamer(port, host_ip, data, is_server=True, data_enricher=shoutcast_data_enricher, companion_sender=zetta_metadata_sender)
    data_streamer.run()
