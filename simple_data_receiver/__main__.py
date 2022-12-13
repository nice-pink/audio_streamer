from lib.data_receiver import DataReceiver
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please define host ip and port as argument.')
        sys.exit(1)
    host_ip: str = sys.argv[1]
    port: int = int(sys.argv[2])
    data_receiver: DataReceiver = DataReceiver(port, host_ip, is_server=False)
    data_receiver.run()
