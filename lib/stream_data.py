from typing import List
from lib.data_handler.shoutcast import ShoutcastDataHandler
from lib.shoutcast_data import ShoutcastData

class StreamData:

    def __init__(self, filepath: str, audio_bitrate: int, chunk_size: int = 1024) -> None:
        self.audio_bitrate: int = audio_bitrate
        self.filepath: str = filepath
        self.chunk_size: int = chunk_size
        self.file_portions: List[bytearray] = []
        self.portions: int = 0

    def prepare(self) -> None:
        with open(self.filepath, 'rb') as file:
            while (data := file.read(self.chunk_size)):
                self.file_portions.append(data)
        self.portions = len(self.file_portions)
        print('Prepared', self.portions, 'portions of size', self.chunk_size, 'from file', self.filepath)

    def prepare_shoutcast_file(self, contains_metadata: bool, audio_block_size: int = 16000, add_http_header: bool = True) -> None:
        with open(self.filepath, 'rb') as file:
            full_data: bytearray = file.read()

        shoutcast_file: bytearray = bytearray()
        
        # Add Shoutcast/Icecast Header
        if add_http_header:
            header: bytes = ShoutcastData.get_icecast_header(contains_metadata, audio_block_size)
            # print(header)
            shoutcast_file += header
        
        # Add audio data and metadata
        data_size: int = 0
        metadata_block_count: int = 0
        while (data_size + audio_block_size < len(full_data)):
            shoutcast_file += full_data[data_size:data_size+audio_block_size]
            data_size += audio_block_size
            if contains_metadata:
                shoutcast_file += ShoutcastData.get_shoutcast_metadata('1', str(metadata_block_count), 8)
            metadata_block_count += 1
        if data_size < len(full_data):
            shoutcast_file += full_data[data_size:]

        shoutcast_file_size: int = len(shoutcast_file)
        print('Full file of size', shoutcast_file_size, 'with', metadata_block_count, 'metadata blocks. Before', len(full_data))
        
        # split to portions
        index = 0
        while (index + self.chunk_size < shoutcast_file_size):
            self.file_portions.append(shoutcast_file[index:index+self.chunk_size])
            index += self.chunk_size
        if index < shoutcast_file_size:
            self.file_portions.append(shoutcast_file[index:])
        self.portions = len(self.file_portions)
        print('Prepared', self.portions, 'portions of size', self.chunk_size, 'from file', self.filepath)
