from typing import List, Optional
import time

class ShoutcastDataHandler:

    def __init__(self, metaint: int = 16000, keep_data: bool = False, remove_header: bool = False) -> None:
        self.keep_data: bool = keep_data
        self.metaint: int = metaint
        self.handled_size: int = 0
        self.metadata_index: int = 0
        self.audio_index: int = 0
        self.metadata: List[bytearray] = []
        self.current_metadata: bytearray = bytearray()
        self.last_metadata: bytearray = bytearray()
        self.last_received_metadata: Optional[time] = None
        self.audio_data: bytearray = bytearray()
        self.current_metadata_block_size: int = 0
        self.remove_header: bool = remove_header
        self.found_header: bool = False
        self.split: bytes = bytes('\r\n\r\n'.encode('utf-8'))
        self.metrics: List[dict] = []

    def update(self, info: dict) -> None:
        print('')
        print('Update data handler.')
        print(info)
        if 'icy-metaint' in info:
            self.metaint = int(info['icy-metaint'])
            print('Updated icy-metaint:', self.metaint)
        elif 'Icy-Metaint' in info:
            self.metaint = int(info['Icy-Metaint'])
            print('Updated icy-metaint:', self.metaint)
        elif 'Icy-MetaInt' in info:
            self.metaint = int(info['Icy-MetaInt'])
            print('Updated icy-metaint:', self.metaint)
        else:
            self.metaint = 0
            print('No metadata in stream.')
        print('')

    def handle(self, data: bytearray) -> None:
        if self.remove_header and not self.found_header:
            index: int = data.find(self.split)
            if index:
                data = data[index+len(self.split):]
                self.found_header = True
                print('Skip header')
            else:
                return
        self.metrics.clear()
        self.found_empty_metadata = False
        self.found_metadata = False
        data_size: int = len(data)
        current_start: int = 0
        while current_start < data_size:
            handled: int = 0
            # start with audio
            if self.metaint == 0 or self.audio_index < self.metaint:
                handled = self.handle_audio_data(data[current_start:], self.handled_size + current_start)
            # start with metadata
            else:
                handled = self.handle_metadata(data[current_start:], self.handled_size + current_start)
            current_start += handled
        self.handled_size += data_size

    def handle_audio_data(self, data: bytearray, full_index: int) -> None:
        data_size: int = len(data)
        # only audio
        if self.metaint == 0 or self.audio_index + data_size <= self.metaint:
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
        start_index: int = 0
        handled_bytes: int = 0
        contains_full_metadata_block: bool = False
        metadata_bytes: int = 0
        if self.metadata_index == 0:
            self.current_metadata_block_size = int(data[0]) * 16
            start_index = 1
            handled_bytes = 1
            print('--- Found metadata. Index:', full_index, 'size:', self.current_metadata_block_size)
        data_size: int = len(data[start_index:])
        
        if self.current_metadata_block_size == 0:
            # metadata block of size = 0
            contains_full_metadata_block = True
            self.add_empty_metadata_found()
        elif self.metadata_index + data_size < self.current_metadata_block_size:
            # data block is smaller than expected metadata block
            self.current_metadata += data[start_index:]
            self.metadata_index += data_size
            handled_bytes += data_size
            if len(self.current_metadata) == self.current_metadata_block_size:
                contains_full_metadata_block = True
        else:
            # complete metadata block
            metadata_bytes = self.current_metadata_block_size - self.metadata_index
            self.current_metadata += data[start_index:metadata_bytes]
            contains_full_metadata_block = True
            
            if ShoutcastDataHandler.is_metadata_empty(self.current_metadata):
                self.add_empty_metadata_found()
            else:
                self.add_metadata_found()

            handled_bytes += metadata_bytes
            self.metadata_index += metadata_bytes

        # reset for next metadata block
        if contains_full_metadata_block:
            if self.keep_data:
                self.metadata.append(self.current_metadata)
            print('Current metadata:')
            ShoutcastDataHandler.print_metadata(self.current_metadata)
            time_ago: str = "0"
            if self.last_received_metadata:
                time_ago = str(int(time.time()-self.last_received_metadata))
            print('Last parsed metadata (' + time_ago + ' sec ago):')
            ShoutcastDataHandler.print_metadata(self.last_metadata)
            if self.current_metadata:
                self.last_metadata = self.current_metadata
                self.last_received_metadata = time.time()
            self.current_metadata = bytearray()
            self.metadata_index = 0
            self.audio_index = 0

        return handled_bytes

    def get_metrics(self) -> List[str]:
        return self.metrics

    @staticmethod
    def is_metadata_empty(metadata: bytes) -> bool:
        metadata_string: str = metadata.decode('utf-8')
        metadata_stripped: str = metadata_string.strip(";'\x00").strip('"')
        metadata_stripped = metadata_stripped.replace('StreamTitle=', '')
        if len(metadata_stripped) == 0:
            return True
        return False

    def add_empty_metadata_found(self):
        self.metrics.append({'id': 'found_empty_metadata', 'value':1})

    def add_metadata_found(self):
        self.metrics.append({'id': 'found_metadata', 'value':1})

    @staticmethod
    def print_metadata(metadata: bytearray) -> None:
        try:
            print(metadata.decode("utf-8"))
        except Exception as exception:
            print(exception)

    @staticmethod
    def get_supported_metric() -> List[str]:
        return ['found_metadata', 'found_empty_metadata']
