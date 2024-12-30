import multiprocessing
import time
from scapy.layers.inet import IP
from scapy.sendrecv import sniff, send
from utils.control_layer import CustomLayer
from utils.utills import LoggerService, PacketService, PacketHandler

class Client:
    def __init__(self, file_path, identifier, dst_ip="127.0.0.1", src_ip="127.0.0.1", ttl=64, logger_service=None, packet_service=None, chunks_length=20, seq_number=1):
        self.file_path = file_path
        self.id = identifier
        self.dst_ip = dst_ip
        self.src_ip = src_ip
        self.ttl = ttl
        self.logger_service = logger_service or LoggerService()
        self.packet_service = packet_service or PacketService(self.logger_service)
        self.packet_received = False
        self.chunks_length = chunks_length
        self.seq_number = seq_number
        self.chunks = []
        self.chunk_number = 0

        self.process = None

        manager = multiprocessing.Manager()
        self.dict = manager.dict()

    @staticmethod
    def time_exceeded(self, dict):
        while True:
            time.sleep(1)
            if dict and not dict.get('packet_received') and dict.get('ack') == 0 and dict.get('last_packet'):
                self.packet_service.send_packet(dict['last_packet'])

    def send_packet(self):
        file_data = PacketHandler.read_file(self.file_path)
        if not file_data:
            self.logger_service.log_error(f"Error: No data to send from the file '{self.file_path}'")
            return

        self.chunks = self._chunk_file_data(file_data)

        outer_packet = self._create_and_send_packet(self.chunks[self.chunk_number], 1)
        self.dict['last_packet'] = outer_packet
        self.dict['ack'] = 0