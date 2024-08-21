from typing import Optional
from ndn.encoding import TlvModel, UintField, BytesField

from group_messages.add import AddMessage
from group_messages.claim import ClaimMessage
from group_messages.heartbeat import HeartbeatMessage
from group_messages.remove import RemoveMessage
from group_messages.specific_message import SpecificMessage
from group_messages.store import StoreMessage
from protocol.tlv import TlvTypes

class MessageTypes:
    ADD = 1
    REMOVE = 2
    STORE = 3
    CLAIM = 4
    HEARTBEAT = 5

class Message(TlvModel):
    type = UintField(TlvTypes.MESSAGE_TYPE)
    value = BytesField(TlvTypes.MESSAGE)
    
    @staticmethod
    def specify(nid:str, seqno:int, message_bytes:bytes) -> Optional[SpecificMessage]:
        message = Message.parse(message_bytes)
        message_type, message_bytes = message.type, bytes(message.value)
        
        if message_type == MessageTypes.ADD:
            return AddMessage(nid, seqno, message_bytes)
        elif message_type == MessageTypes.REMOVE:
            return RemoveMessage(nid, seqno, message_bytes)
        elif message_type == MessageTypes.STORE:
            return StoreMessage(nid, seqno, message_bytes)
        elif message_type == MessageTypes.CLAIM:
            return ClaimMessage(nid, seqno, message_bytes)
        elif message_type == MessageTypes.HEARTBEAT:
            return HeartbeatMessage(nid, seqno, message_bytes)
        else:
            return None
