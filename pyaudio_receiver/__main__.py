from pyaudio_receiver.pyaudio_receiver import PyAudioReceiver
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please define host_ip and port as argument.')
        sys.exit(1)
    host_ip: str = sys.argv[1]
    port: int = int(sys.argv[2])
    audio_receiver: PyAudioReceiver = PyAudioReceiver(port, host_ip)
    audio_receiver.run()
