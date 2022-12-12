from typing import List

class ShoutcastDataHandler:

    def __init__(self, metaint: int = 16000, keep_data: bool = False, remove_header: bool = True) -> None:
        self.keep_data: bool = keep_data
        self.metaint: int = metaint
        self.handled_size: int = 0
        self.metadata_index: int = 0
        self.audio_index: int = 0
        self.metadata: List[bytearray] = []
        self.current_metadata: bytearray = bytearray()
        self.audio_data: bytearray = bytearray()
        self.current_metadata_block_size: int = 0
        self.remove_header: bool = remove_header
        self.found_header: bool = False
        self.split: bytes = bytes('\r\n\r\n'.encode('utf-8'))

    def handle(self, data: bytearray) -> None:
        if self.remove_header and not self.found_header:
            index: int = data.find(self.split)
            if index:
                data = data[index+len(self.split):]
                self.found_header = True
                print('Skip header')
            else:
                return
        data_size: int = len(data)
        current_start: int = 0
        while current_start < data_size:
            handled: int = 0
            # start with audio
            if self.audio_index < self.metaint:
                handled = self.handle_audio_data(data[current_start:], self.handled_size + current_start)
            # start with metadata
            else:
                handled = self.handle_metadata(data[current_start:], self.handled_size + current_start)
            current_start += handled
        self.handled_size += data_size

    def handle_audio_data(self, data: bytearray, full_index: int) -> None:
        data_size: int = len(data)
        # only audio
        if self.audio_index + data_size <= self.metaint:
            if self.keep_data:
                self.audio_data += data
            self.audio_index += data_size
            return data_size
        
        # mixed
        audio_bytes: int = self.metaint - self.audio_index
        if self.keep_data:
            self.audio_data += data[:audio_bytes]
        self.audio_index += audio_bytes
        return audio_bytes


    def handle_metadata(self, data: bytearray, full_index: int) -> None:
        data_size: int = len(data)
        start_index: int = 0
        if self.metadata_index == 0:
            self.current_metadata_block_size = int(data[0]) * 16
            start_index = 1
            print('--- Found metadata. Index:', full_index, 'size:', self.current_metadata_block_size)
        contains_full_metadata_block: bool = False
        metadata_bytes: int = 0
        handled_bytes: int = 0
        # only metadata
        if self.metadata_index + data_size <= self.current_metadata_block_size:
            self.current_metadata += data[start_index:]
            self.metadata_index += data_size
            handled_bytes = data_size
            if len(self.current_metadata) == self.current_metadata_block_size:
                contains_full_metadata_block = True
        else:
            metadata_bytes = self.current_metadata_block_size - self.metadata_index
            self.current_metadata += data[start_index:metadata_bytes]
            contains_full_metadata_block = True
            handled_bytes = metadata_bytes
            self.metadata_index += metadata_bytes

        if contains_full_metadata_block:
            if self.keep_data:
                self.metadata.append(self.current_metadata)
            ShoutcastDataHandler.print_metadata(self.current_metadata)
            self.current_metadata = bytearray()
            self.metadata_index = 0
            self.audio_index = 0

        return handled_bytes

    @staticmethod
    def print_metadata(metadata: bytearray) -> None:
        print(metadata.decode("utf-8"))
