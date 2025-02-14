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


class LoggerService:
    def __init__(self, name=__name__):
        self.logger = logging.getLogger(name)
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)


class PacketService:
    def __init__(self, logger_service):
        self.logger_service = logger_service

    @staticmethod
    def create_outer_packet(src_ip, dst_ip, ttl, file_data, identifier, more_chunk, seq_number):
        inner_packet = PacketHandler.create_packet(src_ip, dst_ip, ttl, file_data, identifier, more_chunk,
                                                   seq_number)
        outer_packet_data = inner_packet
        return PacketHandler.create_packet(src_ip, dst_ip, ttl, outer_packet_data, identifier, 0, 0)

    def validate_checksum(self, packet, raw_ip_header):
        calculated_checksum = checksum(raw_ip_header)
        if int(calculated_checksum) != int(packet[IP].chksum):
            self.logger_service.log_error(f"Checksum mismatch: {packet[IP].chksum} != {calculated_checksum}")
            return False
        return True



    def send_packet(self, packet):
        try:
            send(packet)
        except Exception as e:
            self.logger_service.log_error(f"Error sending packet: {e}")


def checksum(data):
    if len(data) % 2 == 1:
        data += b'\0'

    data = data[:10] + b'\x00\x00' + data[12:]  # Zero out checksum field
    unpacked_data = struct.unpack('!%sH' % (len(data) // 2), data)
    s = sum(unpacked_data)
    s = (s >> 16) + (s & 0xFFFF)
    s += (s >> 16)

    return ~s & 0xFFFF
