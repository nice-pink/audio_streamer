from typing import List

class ShoutcastData:

    @staticmethod
    def get_icecast_header(contains_metadata: bool, audio_block_size: int) -> bytes:
        header_string: str = """HTTP/1.0 200 OK
Content-Type: audio/mpeg
Date: Sun, 11 Dec 2022 20:35:06 GMT
icy-br:320
icy-genre:Test
icy-name:SineSweep
icy-notice1:<BR>This is a radiosphere test stream.<BR>
icy-notice2:SHOUTcast stream<BR>
icy-pub:0
icy-url:http://channel...
Server: Icecast 2.4.0-kh15
Cache-Control: no-cache, no-store
Expires: Mon, 26 Jul 2028 05:00:00 GMT
Connection: Close
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Origin, Accept, X-Requested-With, Content-Type, Icy-MetaData
Access-Control-Allow-Methods: GET, OPTIONS, SOURCE, PUT, HEAD, STATS
"""
        # http header needs: \n -> \r\n
        header_string = header_string.replace('\n', '\r\n')
        
        if contains_metadata:
            header_string += 'icy-metaint:' + str(audio_block_size) + '\r\n\r\n'
        else:
            header_string += '\r\n'

        header: bytes = ShoutcastData.bytes_from(header_string)
        print('header size', len(header))
        return header

    @staticmethod
    def get_shoutcast_metadata(id: str, title: str, encoded_size: int) -> bytes:
        # add metdata block size (/16)
        metadata: bytearray = bytearray([encoded_size])
        # add metadata string
        metadata_block_size: int = encoded_size * 16
        metadata_string: str = 'StreamTitle=' + id + ';' + title
        metadata += ShoutcastData.bytes_from(metadata_string)
        metdata_size: int = len(metadata)
        if metdata_size > metadata_block_size:
            print('Error: Metadata dont fully fit the metadata block.', metdata_size > metadata_block_size)
            return metadata[0:metadata_block_size]
        # add zero padding
        padding: int = metadata_block_size - metdata_size
        metadata += bytes(padding)
        return bytes(metadata)

    @staticmethod
    def bytes_from(string: str) -> bytes:
        return bytes(string, 'UTF-8')
