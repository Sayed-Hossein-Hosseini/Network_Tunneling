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


    def process_packet(self, packet):
        if packet.haslayer(IP) and packet[IP].id == 65535:
            outer_packet = packet[IP]
            raw_ip_header = bytes(outer_packet)[:20]

            if self.packet_service.validate_checksum(packet, raw_ip_header):
                inner_packet = outer_packet[IP][1]
                custom_layer_raw_data = inner_packet.load
                custom_layer = CustomLayer(custom_layer_raw_data)
                if self.seq_number == custom_layer.seq_number:
                    packet = PacketHandler.create_packet(self.src_ip, self.dst_ip, 64, custom_layer.load, self.id, custom_layer.more_chunk, self.seq_number)

                    custom_layer.show()
                    self.packet_service.send_packet(packet)
                    self.dict['last_packet'] = packet
                    self.dict['ack'] = 0
                    self.seq_number += 1

                if custom_layer.more_chunk == 0:
                    self.packet_received = True
                    self.dict['packet_received'] = True
                    self.process.terminate()
            else:
                self.logger_service.log_error(f"Invalid checksum for packet ID: {self.id}")