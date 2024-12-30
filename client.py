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