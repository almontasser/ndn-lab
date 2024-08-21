from ndn.encoding import TlvModel, ModelField, NameField, UintField, RepeatedField, BytesField

from protocol.tlv import TlvTypes

class File(TlvModel):
    file_name = NameField()
    packets = UintField(TlvTypes.PACKETS)
    packet_size = UintField(TlvTypes.PACKET_SIZE)
    size = UintField(TlvTypes.SIZE)

class FileList(TlvModel):
    list = RepeatedField(ModelField(TlvTypes.FILE, File))

class InsertCommand(TlvModel):
    file = ModelField(TlvTypes.FILE, File)
    fetch_path = NameField()


class DeleteCommand(TlvModel):
    file_name = NameField()

class CommandStatus(TlvModel):
    code = UintField(TlvTypes.STATUS_CODE)

class FirstContact(TlvModel):
    prefix = NameField()
    cmduri = BytesField(TlvTypes.CMD_URI)

class NotificationSpecification(TlvModel):
    cmduri = BytesField(TlvTypes.CMD_URI)
