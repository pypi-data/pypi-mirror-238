"""UART transport layer
"""
from logging import getLogger
from .transport import Transport, TransportError
from .timeout import Timer
from .mac import MacError

FRAME_START_CODE = 0x56
FRAME_END_CODE = 0x9E
ESCAPE_SEQ_CODE = 0xCC
FRAME_START_ESC_SEQ = bytes([ESCAPE_SEQ_CODE, ~FRAME_START_CODE & 0xff])
FRAME_END_ESC_SEQ = bytes([ESCAPE_SEQ_CODE, ~FRAME_END_CODE & 0xff])
ESCAPE_SEQ_ESC_SEQ = bytes([ESCAPE_SEQ_CODE, ~ESCAPE_SEQ_CODE & 0xff])

class Frame():
    """UART transport frame
    
    frame = <FRAME_START_CODE> <frame payload> <FRAME_END_CODE>
    frame payload =  encode_payload(<packet> + <frame check sequence>)
    """
    def __init__(self, packet):
        """Frame initialization

        :param packet: Data to be sent in the frame
        :type packet: bytes, bytearray
        """
        self.packet = packet

    @staticmethod
    def calculate_checksum(data):
        """Calculate checksum for transport frame

        The checksum is a two's complement addition (integer addition)
        of 16-bit values in little-endian byte oder.

        :param data: Input data for checksum calculation
        :type data: Bytes like object
        :return: 16bit checksum
        :rtype: int
        """
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i + 1] << 8) | data[i]
        return (~checksum) & 0xffff

    @staticmethod
    def decode_payload(data):
        """Decode frame payload

        Replaces escape codes in payload with corresponding data.

        :param data: Raw frame payload
        :type data: bytes, bytearray
        :raises ValueError: If unknown escape sequences are detected.
        :return: Decoded payload
        :rtype: bytearray
        """
        decoded_data = bytearray()
        escape_code = False
        for byte in data:
            if not escape_code:
                if byte == ESCAPE_SEQ_CODE:
                    escape_code = True
                else:
                    decoded_data.append(byte)
            else:
                if byte == (~FRAME_START_CODE & 0xFF):
                    decoded_data.append(FRAME_START_CODE)
                elif byte == (~FRAME_END_CODE & 0xFF):
                    decoded_data.append(FRAME_END_CODE)
                elif byte == (~ESCAPE_SEQ_CODE & 0xFF):
                    decoded_data.append(ESCAPE_SEQ_CODE)
                else:
                    raise ValueError(f"Decoding of escape sequence failed: "
                            f"Got unkown escape sequence 0x{ESCAPE_SEQ_CODE:02x}{byte:02x}")
                escape_code = False
        return decoded_data

    @staticmethod
    def encode_payload(data):
        """Encode frame payload

        Inserts escape sequences for reserved codes.

        :param data: Frame payload
        :type data: bytes, bytearray
        :return: Encoded frame payload
        :rtype: bytearray
        """
        encoded_data = bytearray()
        for byte in data:
            if byte == FRAME_START_CODE:
                encoded_data += FRAME_START_ESC_SEQ
            elif byte == FRAME_END_CODE:
                encoded_data += FRAME_END_ESC_SEQ
            elif byte == ESCAPE_SEQ_CODE:
                encoded_data += ESCAPE_SEQ_ESC_SEQ
            else:
                encoded_data.append(byte)
        return encoded_data

    def to_bytes(self):
        """Convert frame into bytes

        :return: Bytes representation of the frame
        :rtype: bytes
        """
        padded_packet = self.packet + bytes(1) if len(self.packet) % 2 else self.packet
        check_sequence = self.calculate_checksum(padded_packet).to_bytes(2, byteorder="little")
        frame_payload = self.encode_payload(self.packet + check_sequence)
        frame = bytes([FRAME_START_CODE]) + frame_payload + bytes([FRAME_END_CODE])
        return frame

    @classmethod
    def from_bytes(cls, frame):
        """Create a frame from bytes

        :param frame: Frame in bytes
        :type frame: bytes, bytearray
        :return: Frame instance
        :rtype: Frame
        """
        start_code = frame[0]
        end_code = frame[-1]
        if start_code != FRAME_START_CODE:
            raise ValueError(f"Invalid frame start code: {hex(start_code)}")
        if end_code != FRAME_END_CODE:
            raise ValueError(f"Invalid frame end code: {hex(end_code)}")
        payload = cls.decode_payload(frame[1:-1])
        check_sequence = payload[-2:]
        data = payload[0:-2]
        padded_payload = data + bytes(1) if len(data) % 2 else data
        if cls.calculate_checksum(padded_payload + check_sequence):
            raise ValueError("Frame check sequence error")
        return cls(data)

class UartTransport(Transport):
    """ Transport layer for a generic serial port through USB CDC ACM driver
    """
    def __init__(self, mac, timeout=5):
        """ Class initialization

        :param mac: MAC layer
        :type mac: Instance of a class that implements the Mac interface
        :param timeout: Communication timeout in seconds, defaults to 5
        :type timeout: int, optional
        """
        self.timeout = timeout
        self.com = mac
        self.logger = getLogger(__name__)

    def __del__(self):
        if self.com:
            self.com.close()

    # Support 'with ... as ...' construct
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.com:
            self.com.close()

    def open(self):
        """Open transport
        """
        try:
            self.com.open()
        except MacError as exc:
            self.logger.error("Opening Mac failed: %s", exc)
            raise TransportError(exc) from exc

    def close(self):
        """Close transport
        """
        self.com.close()

    def write(self, data):
        """Send MDFU command packet to client

        :param data: MDFU packet
        :type data: bytes
        """
        frame = Frame(data)
        frame_bytes = frame.to_bytes()
        self.logger.debug("Sending frame -> %s", frame_bytes.hex())
        self.com.write(frame_bytes)

    def read(self):
        """Receive a MDFU status packet

        :raises ValueError: Upon checksum error
        :return: MDFU status packet
        :rtype: bytes
        """
        try:
            frame = bytearray([FRAME_START_CODE])
            # Discard everything until we get the start code
            self.read_until([FRAME_START_CODE])
            # Read everything until we get the end code
            data = self.read_until([FRAME_END_CODE])
            frame.extend(data)
        except TimeoutError:
            self.logger.debug("Timeout while waiting for new frame")
            raise TransportError("Timeout while waiting for new frame") from TimeoutError

        self.logger.debug("Received a frame <- 0x%s", frame.hex())
        try:
            frame = Frame.from_bytes(frame)
        except ValueError as exc:
            self.logger.error("Invalid frame: %s", exc)
            raise TransportError(exc) from exc
        return frame.packet

    def read_until(self, pattern):
        """Read from interface until pattern is detected

        Reads data until the provided pattern is detected. All data, including the
        pattern will be returned.

        :param pattern: Pattern to detect
        :type pattern: Bytes like object
        :raises TimeoutError: When pattern is not detected within timeout
        :return: Data read including the pattern
        :rtype: bytearray
        """
        pattern_detected = False
        timer = Timer(self.timeout)
        data = bytearray()
        while not pattern_detected and not timer.expired():
            for i, pattern_piece in enumerate(pattern):
                buf = self.com.read(1)
                if len(buf) == 0:
                    # timeout in MAC layer, let's try again
                    continue
                data.append(buf[0])
                if buf[0] != pattern_piece:
                    break
                if i == (len(pattern) - 1):
                    pattern_detected = True

        if timer.expired():
            raise TimeoutError("Timeout while waiting for frame start pattern")
        return data
