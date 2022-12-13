from data_http_receiver.data_http_receiver import DataHttpReceiver
from lib.data_handler.shoutcast import ShoutcastDataHandler
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define url as argument.')
        sys.exit(1)
    url: str = sys.argv[1]
    shoutcast_data_handler: ShoutcastDataHandler = ShoutcastDataHandler(remove_header=False)
    data_receiver: DataHttpReceiver = DataHttpReceiver(url, {'icy-metadata':'1'}, data_handler=shoutcast_data_handler)
    data_receiver.run()
