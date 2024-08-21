import logging
from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.storage import Storage

from utils.pubsub import PubSub

class ProtocolHandler(object):
    """
    Interface for protocol interest handles
    """
    def __init__(self, app: NDNApp, data_storage: Storage, pb: PubSub, config: dict):
        self.app = app
        self.data_storage = data_storage
        self.pb = pb
        self.config = config
        self.logger = logging.getLogger()
    async def listen(self, prefix: Name):
        raise NotImplementedError
