import asyncio as aio
import logging
import time
from ndn.app import NDNApp
from ndn.encoding import Name, NonStrictName, DecodeError
from ndn.storage import Storage

from group_messages.message import Message, MessageTypes
from group_messages.remove import RemoveMessageTlv
from handlers.protocol_handler import ProtocolHandler
from main_loop import MainLoop
from modules.global_view import GlobalView
from protocol.base_modules import DeleteCommand
from utils.pubsub import PubSub

class DeleteCommandHandler(ProtocolHandler):
    """
    DeleteCommandHandle processes delete command handles, and deletes corresponding data stored
    in the database.
    TODO: Add validator
    """
    def __init__(self, app: NDNApp, data_storage: Storage, pb: PubSub, config: dict,
                main_loop: MainLoop, global_view: GlobalView):
        """
        :param app: NDNApp.
        :param data_storage: Storage.
        :param pb: PubSub.
        :param config: All config Info.
        :param main_loop: SVS interface, Group Messages.
        :param global_view: Global View.
        """
        super(DeleteCommandHandler, self).__init__(app, data_storage, pb, config)
        self.prefix = None
        self.main_loop = main_loop
        self.global_view = global_view
        self.repo_prefix = config['repo_prefix']
        #self.register_root = config['repo_config']['register_root']

    async def listen(self, prefix: NonStrictName):
        """
        Register routes for command interests.
        This function needs to be called explicitly after initialization.
        :param name: NonStrictName. The name prefix to listen on.
        """
        self.prefix = prefix
        self.logger.info(f'Insert handle: subscribing to {Name.to_str(self.prefix) + "/delete"}')
        self.pb.subscribe(self.prefix + ['delete'], self._on_delete_msg)
        # start to announce process status
        # await self._schedule_announce_process_status(period=3)

    def _on_delete_msg(self, msg):
        try:
            cmd = DeleteCommand.parse(msg)
            # if cmd.name == None:
            #     raise DecodeError()
        except (DecodeError, IndexError) as exc:
            logging.warning('Parameter interest decoding failed')
            return
        aio.ensure_future(self._process_delete(cmd))

    async def _process_delete(self, cmd: DeleteCommand):
        """
        Process delete command.
        """
        file_name = Name.to_str(cmd.file_name)
        self.logger.info(f"[CMD][DELETE]   file {file_name}")
        file = self.global_view.get_file(file_name)
        if file == None:
            self.logger.debug("file does not exist")
            return
        favor = 1.85
        remove_message = RemoveMessageTlv()
        remove_message.node_name = self.config['node_name'].encode()
        remove_message.favor = str(favor).encode()
        remove_message.file_name = cmd.file_name
        message = Message()
        message.type = MessageTypes.REMOVE
        message.value = remove_message.encode()
        self.global_view.delete_file(file_name)
        self.main_loop.svs.publishData(message.encode())
        self.logger.info(f"[MSG][REMOVE]*  fil={file_name}")
