"""MAC layer for simulating host and client
"""
import socket
import selectors
import types
import threading
from logging import getLogger
from collections import deque
from serial import Serial, SerialException
from .timeout import Timer

class Mac():
    """Base class for MAC layer
    """
    def __init__(self):
        """Class initialization"""

    def open(self):
        """Open MAC layer"""

    def close(self):
        """Close MAC layer"""

class MacError(Exception):
    """Generic MAC error"""

class MacPacket(Mac):
    """Packet based MAC
    """
    def __init__(self, buffer_in: deque, buffer_out: deque, timeout=5):
        self.buffer_in = buffer_in
        self.buffer_out = buffer_out
        self.timeout = timeout

    def write(self, packet):
        """Write a packet to MAC layer

        :param packet: Packet to send to MAC layer
        :type packet: any
        """
        self.buffer_in.appendleft(packet)

    def read(self):
        """Read a packet from MAC layer

        :raises TimeoutError: Raised when timeout is not None and read timeout expired
        :return: Packet from MAC layer
        :rtype: any
        """
        timer = Timer(self.timeout)
        while len(self.buffer_out) == 0 and not timer.expired():
            pass
        if timer.expired():
            raise TimeoutError("Read timeout")
        return self.buffer_out.pop()

    def __len__(self):
        """Number of packets in read queue"""
        return len(self.buffer_out)

class MacBytes(Mac):
    """Bytes based MAC
    """
    def __init__(self, buffer_in: deque, buffer_out: deque, timeout=5):
        """Class initialization

        :param buffer_in: MAC layer input buffer
        :type buffer_in: deque
        :param buffer_out: MAC layer output buffer
        :type buffer_out: deque
        :param timeout: Read timeout in seconds, defaults to 5
        :type timeout: int, optional
        """
        self.buffer_in = buffer_in
        self.buffer_out = buffer_out
        self.timeout = timeout

    def write(self, data):
        """Write to MAC layer

        :param data: Data to write.
        :type data: bytes, bytearray
        """
        self.buffer_in.extendleft(data)

    def read(self, size):
        """Read from MAC layer
        
        Read size bytes from the MAC layer. If no timeout is set (None) it is a blocking
        read. With a timeout set it will raise a TimeoutError exception when it expires.
        
        :param size: Number of bytes to read
        :type size: int
        """
        if size > len(self.buffer_out):
            if self.timeout:
                timer = Timer(self.timeout)
                while not timer.expired() and (size > len(self.buffer_out)):
                    pass
                if timer.expired():
                    raise TimeoutError()
            else:
                while size > len(self.buffer_out):
                    pass

        data = bytearray()
        for _ in range(size):
            data.append(self.buffer_out.pop())
        return data

    def __len__(self):
        """Get number of bytes available to read from MAC

        :return: Number of bytes
        :rtype: int
        """
        return len(self.buffer_out)

class MacSocketHost(threading.Thread):
    """Host MAC layer for a network connection"""
    def __init__(self, host, port, timeout=3):
        """Class initialization

        :param host: Host interface to listen on
        :type host: str
        :param port: Port to listen on for connections
        :type port: int
        """
        self.logger = getLogger("mac.MacSocketHost")
        self.host = host
        self.port = port
        self.timeout = timeout
        self.rx_buf = deque()
        self.tx_buf = deque()
        self.stop_event = threading.Event()
        self.sel = selectors.DefaultSelector()
        self.conn = None
        self.opened = False
        self.sock = None

        super().__init__(name="Socket connection manager")

    def run(self):
        """Thread main loop
        """
        while True:
            events = self.sel.select(timeout=1)
            for key, mask in events:
                # if we have not attached any data to this thread it is
                # a new thread
                if key.data is None:
                    self.accept()
                else:
                    self.service_connection(key, mask)
            if self.stop_event.is_set():
                break

    def accept(self):
        """Accept and initialize new connection
        """
        self.conn, addr = self.sock.accept()
        self.logger.debug("Accepted connection from %s", addr)
        self.conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, connected=False)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(self.conn, events, data=data)

    def service_connection(self, key, mask):
        """Service connected client

        :param key: Selector key
        :type key: SelectorKey
        :param mask: Events bitmask
        :type mask: int
        """
        data = key.data
        if mask & selectors.EVENT_READ:
            try:
                recv_data = self.conn.recv(1024)
            except ConnectionError:
                recv_data = 0

            if recv_data:
                self.logger.debug("Received data %s from %s", str(recv_data), data.addr)
                self.rx_buf.extendleft(recv_data)
            else:
                self.logger.debug("Closing connection to %s", data.addr)
                self.sel.unregister(self.conn)
                self.conn.close()
        if mask & selectors.EVENT_WRITE:
            if len(self.tx_buf):
                buf = bytearray()
                for _ in range(len(self.tx_buf)):
                    buf.append(self.tx_buf.pop())
                self.logger.debug("Sending %s to %s", str(bytes(buf)), data.addr)
                self.conn.sendall(buf)

    def open(self):
        """Open MAC layer
        """
        if not self.opened:
            self.rx_buf.clear()
            self.tx_buf.clear()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen()
            self.sock.setblocking(False)
            # Register selector for listening socket
            self.sel.register(self.sock, selectors.EVENT_READ, data=None)
            self.start()
            self.opened = True
            self.logger.debug("Socket MAC started")

    def close(self):
        """Close MAC layer
        """
        if self.opened:
            self.stop_event.set()
            self.join()
            self.sel.unregister(self.sock)
            self.sock.close()
            self.logger.debug("Socket MAC stopped")
            self.opened = False

    def read(self, size):
        """Read received data

        :param size: Number of bytes to read
        :type size: int
        :raises TimeoutError: Raised when read timeout expires
        :return: Read data
        :rtype: bytearray
        """
        if size > len(self.rx_buf):
            if self.timeout:
                timer = Timer(self.timeout)
                while not timer.expired() and (size > len(self.rx_buf)):
                    pass
                if timer.expired():
                    raise TimeoutError()
            else:
                while size > len(self.rx_buf):
                    pass

        data = bytearray()
        for _ in range(size):
            data.append(self.rx_buf.pop())
        return data

    def write(self, data):
        """Write data to MAC

        :param data: Data to write
        :type data: Bytes like object
        """
        self.tx_buf.extendleft(data)

class MacSocketClient(Mac):
    """Socket based transport
    """
    def __init__(self, port, host='localhost', timeout=5):
        """Class initialization

        :param buffer_in: MAC layer input buffer
        :type buffer_in: deque
        :param buffer_out: MAC layer output buffer
        :type buffer_out: deque
        :param timeout: Read timeout in seconds, defaults to 5
        :type timeout: int, optional
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.buf = bytearray()
        self.opened = False
        self.sock = None

    def open(self):
        if not self.opened:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.host, self.port))
            self.opened = True

    def close(self):
        if self.opened:
            self.sock.close()
            self.opened = False

    def write(self, data):
        """Write to MAC layer

        :param data: Data to write.
        :type data: bytes, bytearray
        """
        self.sock.sendall(data)

    def read(self, size):
        """Read from MAC layer

        Read size bytes from the MAC layer. If no timeout is set (None) it is a blocking
        read. With a timeout set it will raise a TimeoutError exception when it expires.

        :param size: Number of bytes to read
        :type size: int
        """
        if size > len(self.buf):
            if self.timeout:
                timer = Timer(self.timeout)
                while not timer.expired() and (size > len(self.buf)):
                    self.buf.extend(self.sock.recv(size - len(self.buf)))
                if timer.expired():
                    raise TimeoutError()
            else:
                while size > len(self.buf):
                    self.buf.extend(self.sock.recv(size - len(self.buf)))
        data = self.buf[:size]
        self.buf = self.buf[size:]
        return data

    def __len__(self):
        """Get number of bytes available to read from MAC

        :return: Number of bytes
        :rtype: int
        """
        return len(self.buf)

class MacSocketPair(Mac):
    """Socket based MAC
    """
    def __init__(self, sock, timeout=5):
        """Class initialization

        :param sock: One of the sockets from the socket pair
        :type: socket
        :param timeout: Read timeout in seconds, defaults to 5
        :type timeout: int, optional
        """
        self.sock = sock
        self.timeout = timeout
        self.sock.settimeout(0)
        self.buf = bytearray()

    def write(self, data):
        """Write to MAC layer

        :param data: Data to write.
        :type data: bytes, bytearray
        """
        self.sock.sendall(data)

    def read(self, size):
        """Read from MAC layer

        Read size bytes from the MAC layer. If no timeout is set (None) it is a blocking
        read. With a timeout set it will raise a TimeoutError exception when it expires.

        :param size: Number of bytes to read
        :type size: int
        """
        if size > len(self.buf):
            if self.timeout:
                timer = Timer(self.timeout)
                while not timer.expired() and (size > len(self.buf)):
                    try:
                        self.buf.extend(self.sock.recv(size - len(self.buf)))
                    except BlockingIOError:
                        pass
                if timer.expired():
                    raise TimeoutError()
            else:
                while size > len(self.buf):
                    self.buf.extend(self.sock.recv(size - len(self.buf)))
        data = self.buf[:size]
        self.buf = self.buf[size:]
        return data

    def __len__(self):
        """Get number of bytes available to read from MAC

        :return: Number of bytes
        :rtype: int
        """
        try:
            self.buf.extend(self.sock.recv(256))
        except BlockingIOError:
            pass
        return len(self.buf)

class MacSerialPort(Serial):
    """MAC wrapper for a serial port based on pySerial
    """
    def __init__(self, port, baudrate, timeout=5, bytesize=8, parity='N', stopbits=1):
        """Class initialization

        :param port: Serial port e.g. COM11 or /dev/ttyACMS0
        :type port: str
        :param baudrate: Baudrate
        :type baudrate: int
        :param timeout: Read timeout for MAC in seconds, defaults to 5
        timeout = None -> blocking read without timeout
        timeout = 0 -> non-blocking read, return immediately with zero or up to the requested number of bytes
        timeout > 0 -> set timeout to the specified number of seconds
        :type timeout: int or None, optional
        """
        # Initialize serial port but don't open yet (=we do not pass port as argument)
        super().__init__(baudrate=baudrate, timeout=timeout, bytesize=bytesize, parity=parity, stopbits=stopbits)
        # store port in instance for opening the port later
        self.port = port

    def open(self):
        try:
            super().open()
        except SerialException as exc:
            raise MacError(exc) from exc

class MacFactory():
    """MAC layer factory
    """
    def __init__(self):
        pass

    @staticmethod
    def get_serial_port_mac(port, baudrate, timeout=5):
        """Create a MAC layer for serial port access

        :return: MAC layer
        :rtype: MacSerialPort
        """
        mac = MacSerialPort(port, baudrate=baudrate, timeout=timeout)
        return mac

    @classmethod
    def get_packet_based_mac(cls, timeout=5):
        """Create a packet based MAC layer

        :param timeout: Read timeout for MAC, defaults to 5 seconds
        :type timeout: int, optional
        :return: Linked MAC objects that can be injected into host/client transport layer
        :rtype: (MacPacket, MacPacket)
        """
        host_in = deque()
        client_in = deque()
        host = MacPacket(host_in, client_in, timeout=timeout)
        client = MacPacket(client_in, host_in, timeout=timeout)
        return host, client

    @classmethod
    def get_bytes_based_mac(cls, timeout=5):
        """Create a bytes based MAC layer

        :param timeout:  Read timeout for MAC, defaults to 5 seconds
        :type timeout: int, optional
        :return: Linked MAC objects that can be injected into host/client transport layer
        :rtype: (MacPacket, MacPacket)
        """
        host_in = deque()
        client_in = deque()
        host = MacBytes(host_in, client_in, timeout=timeout)
        client = MacBytes(client_in, host_in, timeout=timeout)
        return host, client

    @classmethod
    def get_socketpair_based_mac(cls, timeout=5):
        """Create a socketpair based MAC layer

        :param timeout: Read timeout for MAC, defaults to 5
        :type timeout: int, optional
        :return: Host and client socketpair
        :rtype: tuple(MacSocketPair, MacSocketpair)
        """
        if hasattr(socket, "AF_UNIX"):
            family = socket.AF_UNIX
        else:
            family = socket.AF_INET
        sock1, sock2 = socket.socketpair(family, type=socket.SOCK_STREAM)

        sock1.settimeout(timeout)
        sock2.settimeout(timeout)
        host = MacSocketPair(sock1)
        client = MacSocketPair(sock2)
        return host, client

    @classmethod
    def get_socket_client_mac(cls, timeout=5, host="localhost", port=5557):
        """Create a client socket based MAC (MDFU host)

        From a socket connection point of view this is a client socket but
        for the MDFU protocol it is the MAC layer for the host application.

        :param timeout: Read timeout on MAC layer, defaults to 5
        :type timeout: int, optional
        :param host: Socket host to connect to, defaults to "localhost"
        :type host: str, optional
        :param port: Host port, defaults to 5557
        :type port: int, optional
        :return: MAC layer
        :rtype: MacSocketClient
        """
        client = MacSocketClient(port, host=host, timeout=timeout)
        return client

    @classmethod
    def get_socket_host_mac(cls, host="localhost", port=5557, timeout=3):
        """Create a host socket based MAC (MDFU client)

        From a socket connection point of view this is a host socket but
        for the MDFU protocol it is the MAC layer for the client.

        :param timeout: Timeout for host socket read, defaults to 3.
        A value of None or zero will be a blocking read.
        :type timeout: int, optional
        :param host: Host interface, defaults to "localhost"
        :type host: str, optional
        :param port: Port to listen on for connections, defaults to 5557
        :type port: int, optional
        :return: Mac layer
        :rtype: MacSocketHost
        """
        server = MacSocketHost(host, port, timeout=timeout)
        return server
