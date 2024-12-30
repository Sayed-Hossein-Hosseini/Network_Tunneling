import multiprocessing
import time

from scapy.all import sniff
from scapy.layers.inet import IP

from utils.control_layer import CustomLayer
from utils.utills import LoggerService, PacketService, PacketHandler


class Server:
    def __init__(self, id, src_ip="127.0.0.1", dst_ip="127.0.0.1", iface=r"\Device\NPF_Loopback", logger_service=None, packet_service=None, seq_number=1):
        self.id = id
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.iface = iface
        self.logger_service = logger_service or LoggerService()
        self.packet_service = packet_service or PacketService(self.logger_service)
        self.packet_received = False
        self.seq_number = seq_number

        self.process = None

        manager = multiprocessing.Manager()
        self.dict = manager.dict()

    @staticmethod
    def time_exceeded(self, dict):
        while True:
            time.sleep(1)
            if dict and not dict.get('packet_received') and dict.get('ack') == 0 and dict.get('last_packet'):
                self.packet_service.send_packet(dict['last_packet'])