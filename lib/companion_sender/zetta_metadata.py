import requests
from threading import Thread
from lib.metadata_handler.zetta_metadata import ZettaMetadata, ZettaLogEventType

class ZettaMetadataSender:

    def __init__(self, id: str, url: str, file_duration: float = 0.0) -> None:
        self.id: str = id
        self.url: str = url
        self.file_duration: float = file_duration

    def send(self, index: int, end: bool = False) -> None:
        headers: dict = {'Content-Type': 'application/xml'}
        xml: str = self.get_xml(index, end)
        thread: Thread = Thread(target=ZettaMetadataSender.send_request, args=(self.url, xml, headers, ))
        thread.start()
        # thread.join()

    def get_xml(self, index: int, end: bool) -> str:
        zetta_metadata: ZettaMetadata = ZettaMetadata()
        events: List[ZettaLogEventType] = []
        if end:
            events = [ZettaLogEventType.Default, ZettaLogEventType.LastStarted]
        else:
            events = [ZettaLogEventType.LastStarted, ZettaLogEventType.Default]

        return zetta_metadata.build(index, events, 5.0)

    @staticmethod
    def send_request(url: str, xml: str, headers: dict) -> None:
        try:
            response = requests.post(url, headers=headers, data=xml)
            if response.status_code != 200:
                print(response)
        except Exception as exception:
            print('Error:', exception)