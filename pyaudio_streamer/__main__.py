from pyaudio_streamer.pyaudio_streamer import PyAudioStreamer
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please define port as argument.')
        sys.exit(1)
    port: int = int(sys.argv[1])
    audio_streamer: PyAudioStreamer = PyAudioStreamer(port, 'test_files/sweep.wav')
    audio_streamer.run()
