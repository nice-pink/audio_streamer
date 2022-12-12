from typing import List
from lib.shoutcast_data import ShoutcastData

class ShoutcastDataEnricher:

    def __init__(self, id: str, add_header: bool = True, metaint: int = 16000) -> None:
        self.id: str = id
        self.metaint: int = metaint
        self.metadata_index: int = 0
        self.current_block_index: int = 0
        self.header_end: int = 0
        self.split: bytes = bytes('\r\n\r\n'.encode('utf-8'))
        self.handeled_size: int = 0
        self.add_header: bool = add_header
        self.did_add_header: bool = False

    def handle(self, data: bytearray) -> bytearray:
        if self.add_header and not self.did_add_header:
            icecast_header: bytes = ShoutcastData.get_icecast_header(True, audio_block_size=self.metaint)
            data = icecast_header + data
            self.current_block_index -= len(icecast_header)
            print('Added header')
            self.did_add_header = True
        data_size: int = len(data)
        # don't add metadata to block
        if self.current_block_index + data_size < self.metaint:
            self.current_block_index += data_size
            self.handeled_size += data_size
            return data
        
        metadata: bytes = ShoutcastData.get_shoutcast_metadata(self.id, str(self.metadata_index), 8)
        metadata_size: int = len(metadata)
        self.metadata_index += 1

        # append metadata
        if self.current_block_index + data_size == self.metaint:
            self.handeled_size += data_size + metadata_size
            self.current_block_index = 0
            return data + metadata
        
        # insert metadata to block
        offset: int = self.metaint - self.current_block_index
        self.handeled_size += data_size + metadata_size
        self.current_block_index = data_size - offset
        return data[:offset] + metadata + data[offset:]
