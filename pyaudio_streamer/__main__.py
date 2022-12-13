from pyaudio_streamer.pyaudio_streamer import PyAudioStreamer
import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Please define filepath, host_ip and port as argument.')
        sys.exit(1)
    filepath: str = sys.argv[1]
    host_ip: str = sys.argv[2]
    port: int = int(sys.argv[3])
    audio_streamer: PyAudioStreamer = PyAudioStreamer(port, host_ip, filepath)
    audio_streamer.run()
