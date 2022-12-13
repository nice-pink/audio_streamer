from lib.data_receiver import DataReceiver
from lib.data_handler.shoutcast import ShoutcastDataHandler
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please define host_ip and port as argument.')
        sys.exit(1)
    host_ip: str = sys.argv[1]
    port: int = int(sys.argv[2])
    shoutcast_data_handler: ShoutcastDataHandler = ShoutcastDataHandler(remove_header=True)
    data_receiver: DataReceiver = DataReceiver(port, host_ip, is_server=False, data_handler=shoutcast_data_handler)
    data_receiver.run()
