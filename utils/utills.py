import logging
import os
import struct

from scapy.layers.inet import IP
from scapy.sendrecv import send

from utils.control_layer import CustomLayer


class PacketHandler:

    def __init__(self, logger_service=None):
        self.logger_service = logger_service or LoggerService()


    @staticmethod
    def read_file(file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, "rb") as file:
                file_data = file.read()
            return file_data
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {e}")