from data_streamer.data_streamer import DataStreamer
from lib.stream_data import StreamData
from lib.data_handler.shoutcast import ShoutcastDataHandler
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define port as argument.')
        sys.exit(1)

    port: int = int(sys.argv[1])
    data: StreamData = StreamData('test_files/sweep_5sec.mp3', 320000)
    data.prepare_shoutcast_file(True)

    # # test
    # shoutcastDataHandler: ShoutcastDataHandler = ShoutcastDataHandler(keep_data=True, remove_header=True)
    # for portion in data.file_portions:
    #     shoutcastDataHandler.handle(portion)

    # for meta in shoutcastDataHandler.metadata:
    #     ShoutcastDataHandler.print_metadata(meta)

    # stream data
    data_streamer: DataStreamer = DataStreamer(port, data, is_server=True)
    data_streamer.run()
