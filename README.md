# Network Tunneling

This project is a custom packet transmission system designed to send and receive data packets over a network using a custom protocol layer. It includes a client-server architecture where the client sends file data in chunks, and the server processes and acknowledges these packets. The project leverages Scapy for packet crafting and manipulation, and it includes features like checksum validation, packet retransmission, and sequence number management.

---

## Features

- **Custom Protocol Layer**: Implements a custom protocol layer (`CustomLayer`) to encapsulate file data, sequence numbers, and control flags.
- **Packet Handling**: Provides robust packet creation, validation, and transmission mechanisms.
- **Chunked File Transfer**: Splits large files into smaller chunks for efficient transmission.
- **Checksum Validation**: Ensures data integrity by validating packet checksums.
- **Retransmission Mechanism**: Automatically retransmits packets if acknowledgments are not received.
- **Multiprocessing Support**: Uses multiprocessing to handle packet retransmission and sniffing concurrently.
- **Logging**: Includes a logging service to track events, errors, and debug information.

---

## Project Structure

The project is divided into several modules, each responsible for specific functionality:

1. **Custom Protocol Layer (`control_layer.py`)**:
   - Defines the `CustomLayer` class, which encapsulates file data, sequence numbers, and control flags.

2. **Packet Handling (`utills.py`)**:
   - Contains the `PacketHandler`, `PacketService`, and `LoggerService` classes for packet creation, validation, and logging.

3. **Client (`client.py`)**:
   - Implements the `Client` class, which reads a file, splits it into chunks, and sends the chunks to the server.

4. **Server (`server.py`)**:
   - Implements the `Server` class, which listens for incoming packets, processes them, and sends acknowledgments.

---

## Code Overview

### Custom Protocol Layer (`control_layer.py`)

The `CustomLayer` class defines the custom protocol layer used to encapsulate file data, sequence numbers, and control flags.

```python
from scapy.all import Packet, IntField
from scapy.fields import StrField

class CustomLayer(Packet):
    name = "ControlLayer"
    fields_desc = [
        IntField("more_chunk", 0),  # Flag to indicate if more chunks are coming
        IntField("seq_number", 0),  # Sequence number for packet ordering
        StrField("load", b"")       # Field for the raw file data (string type)
    ]
```

---

### Packet Handling (`utills.py`)

This module contains utility classes for packet creation, validation, and logging.

#### `PacketHandler`
- Reads file data and creates packets.

#### `PacketService`
- Handles packet creation, validation, and transmission.

#### `LoggerService`
- Provides logging functionality for debugging and tracking events.

```python
import logging
import os
import struct
from scapy.layers.inet import IP
from scapy.sendrecv import send
from utils.control_layer import CustomLayer

class PacketHandler:
    @staticmethod
    def read_file(file_path):
        # Reads file data from the specified path.

    @staticmethod
    def create_packet(src_ip, dst_ip, ttl, file_data, identifier, more_chunk, seq_number):
        # Creates a packet with the custom protocol layer.

class LoggerService:
    def __init__(self, name=__name__):
        # Initializes the logger.

    def log_info(self, message):
        # Logs informational messages.

    def log_error(self, message):
        # Logs error messages.

    def log_debug(self, message):
        # Logs debug messages.

class PacketService:
    def __init__(self, logger_service):
        # Initializes the packet service.

    @staticmethod
    def create_outer_packet(src_ip, dst_ip, ttl, file_data, identifier, more_chunk, seq_number):
        # Creates an outer packet with the custom protocol layer.

    def validate_checksum(self, packet, raw_ip_header):
        # Validates the packet checksum.

    def send_packet(self, packet):
        # Sends the packet over the network.

def checksum(data):
    # Calculates the checksum for the packet.
```

---

### Client (`client.py`)

The `Client` class reads a file, splits it into chunks, and sends the chunks to the server. It also handles retransmission and acknowledgment.

```python
import multiprocessing
import time
from scapy.layers.inet import IP
from scapy.sendrecv import sniff, send
from utils.control_layer import CustomLayer
from utils.utills import LoggerService, PacketService, PacketHandler

class Client:
    def __init__(self, file_path, identifier, dst_ip="127.0.0.1", src_ip="127.0.0.1", ttl=64, logger_service=None, packet_service=None, chunks_length=20, seq_number=1):
        # Initializes the client.

    @staticmethod
    def time_exceeded(self, dict):
        # Handles packet retransmission if no acknowledgment is received.

    def send_packet(self):
        # Reads the file, splits it into chunks, and sends the first chunk.

    def start_sniffing(self):
        # Starts sniffing for incoming packets.

    def get_inner_packet(self, packet):
        # Processes received packets.

    def _process_received_packet(self, packet):
        # Processes and validates received packets.

    def should_stop_sniffing(self, packet):
        # Determines when to stop sniffing.

    def _chunk_file_data(self, file_data):
        # Splits file data into chunks.

    def _create_and_send_packet(self, chunk_data, more_chunks_flag):
        # Creates and sends a packet.

if __name__ == "__main__":
    # Example usage of the Client class.
```

---

### Server (`server.py`)

The `Server` class listens for incoming packets, processes them, and sends acknowledgments.

```python
import multiprocessing
import time
from scapy.all import sniff
from scapy.layers.inet import IP
from utils.control_layer import CustomLayer
from utils.utills import LoggerService, PacketService, PacketHandler

class Server:
    def __init__(self, id, src_ip="127.0.0.1", dst_ip="127.0.0.1", iface=r"\Device\NPF_Loopback", logger_service=None, packet_service=None, seq_number=1):
        # Initializes the server.

    @staticmethod
    def time_exceeded(self, dict):
        # Handles packet retransmission if no acknowledgment is received.

    def process_packet(self, packet):
        # Processes incoming packets.

    def start_sniffing(self):
        # Starts sniffing for incoming packets.

    def should_stop_sniffing(self, packet):
        # Determines when to stop sniffing.

    def stop_condition(self, packet):
        # Checks if sniffing should stop.

if __name__ == "__main__":
    # Example usage of the Server class.
```

---

## How to Use

1. **Run the Server**:
   - Start the server by running `server.py`. It will listen for incoming packets.

2. **Run the Client**:
   - Start the client by running `client.py`. It will read the specified file, split it into chunks, and send the chunks to the server.

3. **Monitor Logs**:
   - Both the client and server log their activities. Check the logs for debugging and status updates.

---

## Dependencies

- **Python 3.x**
- **Scapy**: Install using `pip install scapy`.
- **Multiprocessing**: Built-in Python library.

---

## Conclusion

This project demonstrates a custom packet transmission system with features like chunked file transfer, checksum validation, and retransmission. It is a robust solution for sending and receiving data over a network using a custom protocol layer. The use of Scapy and multiprocessing makes it efficient and scalable for various use cases.

---

## License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.  

---

## Authors  

- Sayyed Hossein Hosseini DolatAbadi
- Mohammad Hossein Rangraz
