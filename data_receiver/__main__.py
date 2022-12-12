from data_receiver.data_receiver import DataReceiver
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define port as argument.')
        sys.exit(1)
    port: int = int(sys.argv[1])
    data_receiver: DataReceiver = DataReceiver(port, is_server=False)
    data_receiver.run()
