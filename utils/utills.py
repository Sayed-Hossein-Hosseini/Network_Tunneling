import logging
import os
import struct

from scapy.layers.inet import IP
from scapy.sendrecv import send

from utils.control_layer import CustomLayer


class PacketHandler:

    def __init__(self, logger_service=None):
        self.logger_service = logger_service or LoggerService()