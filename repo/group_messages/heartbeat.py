from typing import Callable
from ndn.encoding import *

from group_messages.specific_message import SpecificMessage
from modules.favor_calculator import FavorCalculator, FavorParameters

class HeartbeatMessageTypes:
    NODE_NAME = 84
    FAVOR_PARAMETERS = 85
class HeartbeatMessageTlv(TlvModel):
    node_name = BytesField(HeartbeatMessageTypes.NODE_NAME)
    favor_parameters = ModelField(HeartbeatMessageTypes.FAVOR_PARAMETERS, FavorParameters)

class HeartbeatMessage(SpecificMessage):
    def __init__(self, nid:str, seqno:int, raw_bytes:bytes):
        super(HeartbeatMessage, self).__init__(nid, seqno)
        self.message = HeartbeatMessageTlv.parse(raw_bytes)

    async def apply(self, global_view, fetch_file, svs, config):
        node_name = self.message.node_name.tobytes().decode()
        favor = FavorCalculator().calculate_favor(self.message.favor_parameters)
        self.logger.debug(f"[MSG][HB]   nam={node_name};fav={favor}")
        global_view.update_node(node_name, favor, self.seqno)
