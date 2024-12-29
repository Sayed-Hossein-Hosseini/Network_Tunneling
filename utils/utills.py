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


    def create_packet(src_ip, dst_ip, ttl, file_data, identifier, more_chunk, seq_number):
        ip_packet = IP(src=src_ip, dst=dst_ip, ttl=ttl, version=4, id=identifier)

        if isinstance(file_data, IP):
            result = ip_packet / file_data
        else:
            control_layer = CustomLayer(more_chunk=more_chunk, load=file_data, seq_number=seq_number)
            result = ip_packet / control_layer

        calculated_checksum = checksum(bytes(result)[:20])
        result[IP].chksum = calculated_checksum
        return result