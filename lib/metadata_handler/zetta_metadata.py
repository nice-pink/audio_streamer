import xml.etree.ElementTree as ET
from enum import Enum
from typing import List
import uuid
from datetime import datetime, timedelta

class ZettaLogEventType(Enum):
    Default=0
    LastStarted=1
    AdTrigger=2

class ZettaMetadata:

    def __init__(self):
        self.base_tree = ET.parse('metadata_raw/zetta/base.xml')
        self.base_root = self.base_tree.getroot()
        default_tree = ET.parse('metadata_raw/zetta/logevent.xml')
        self.default_root = default_tree.getroot()
        started_tree = ET.parse('metadata_raw/zetta/logevent_laststarted.xml')
        self.started_root = started_tree.getroot()
        ad_trigger_tree = ET.parse('metadata_raw/zetta/start_ad.xml')
        self.ad_trigger_root = ad_trigger_tree.getroot()

        self.last_uuids: List[str] = [str(uuid.uuid1())]
        
    def build(self, index: int, log_event_types: List[ZettaLogEventType], file_duration: float) -> str:
        elem = None
        for elem in self.base_root.iter():
            #print(elem.tag)
            pass

        log_events = elem
        event_count: int = 0
        for log_event_type in log_event_types:
            sub_tree = self.get_item(index, event_count, log_event_type, file_duration)
            log_events.append(sub_tree)
            event_count += 1
        
        #ET.indent(self.base_root)
        # print(ET.tostring(self.base_root, encoding='unicode'))

        return ET.tostring(self.base_root, encoding='unicode')

    def get_item(self, index: int, event_count: int, log_event_type: ZettaLogEventType, file_duration: float):
        root = None
        if log_event_type == ZettaLogEventType.Default:
            root = self.default_root
        elif log_event_type == ZettaLogEventType.LastStarted:
            root = self.started_root
        elif log_event_type == ZettaLogEventType.AdTrigger:
            root = self.ad_trigger_root
        
        # update root
        root.attrib['UniversalIdentifier'] = self.last_uuids[0]

        # update timestamps
        start_timestamp: datetime = datetime.now()
        end_timestamp: datetime = start_timestamp + timedelta(seconds=file_duration)
        start = start_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        end = end_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        root.attrib['AirStarttime'] = str(start)
        root.attrib['AirStarttimeLocal'] = str(start)
        root.attrib['AirStoptime'] = str(end)
        root.attrib['AirStoptimeLocal'] = str(end)
        
        # update title
        for elem in root.iter():
            if elem.tag == 'Asset':
                elem.attrib['Title'] = str(index+event_count)

        return root
        