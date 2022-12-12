from data_receiver.data_receiver import DataReceiver
from lib.data_handler.shoutcast import ShoutcastDataHandler
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define port as argument.')
        sys.exit(1)
    port: int = int(sys.argv[1])
    shoutcast_data_handler: ShoutcastDataHandler = ShoutcastDataHandler(remove_header=True)
    data_receiver: DataReceiver = DataReceiver(port, is_server=False, data_handler=shoutcast_data_handler)
    data_receiver.run()
