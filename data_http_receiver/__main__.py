from data_http_receiver.data_http_receiver import DataHttpReceiver
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define url as argument.')
        sys.exit(1)
    url: str = sys.argv[1]
    data_receiver: DataHttpReceiver = DataHttpReceiver(url, {})
    data_receiver.run()
