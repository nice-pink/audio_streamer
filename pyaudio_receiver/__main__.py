from pyaudio_receiver.pyaudio_receiver import PyAudioReceiver
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define port as argument.')
        sys.exit(1)
    port: int = int(sys.argv[1])
    audio_receiver: PyAudioReceiver = PyAudioReceiver(port)
    audio_receiver.run()
