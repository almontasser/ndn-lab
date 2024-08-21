import logging


class SpecificMessage:
    def __init__(self, nid:str, seqno:int) -> None:
        self.nid, self.seqno, self.logger = nid, seqno, logging.getLogger()
