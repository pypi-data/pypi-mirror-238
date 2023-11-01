"""MDFU protocol
"""
from enum import Enum
from logging import getLogger
from .transport import Transport, TransportError

class MdfuStatus(Enum):
    """MDFU status codes
    """
    SUCCESS = 1
    NOT_SUPPORTED = 2
    NOT_AUTHORIZED = 3
    PACKET_TRANSPORT_FAILURE = 4
    ABORT_FILE_TRANSFER = 5

class MdfuCmd(Enum):
    """MDFU command codes
    """
    GET_TRANSFER_PARAMETERS = 1
    START_TRANSFER = 2
    WRITE_CHUNK = 3
    GET_IMAGE_STATE = 4
    END_TRANSFER = 5

def chunkify(data: bytes, chunk_size: int, padding=None):
    """Split data up into chunks

    :param data: Data for chunking.
    :type data: Bytes like object
    :param chunk_size: Chunks size
    :type chunk_size: int
    :param padding: Byte value to pad in last chunk if data is not a multiple
    of chunk_size, optional, default None = do not pad
    :type padding: int
    :return: Chunks of data
    :rtype: List object with chunks of data
    """
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    if padding:
        padding_byte_count = len(data) % chunk_size
        chunks[-1] += bytes([padding] * padding_byte_count)
    return chunks

class MdfuProtocolError(Exception):
    """Generic MDFU exception
    """

class MdfuCmdNotSupportedError(MdfuProtocolError):
    """MDFU exception if command is not supported on client
    """

class MdfuStatusInvalidError(MdfuProtocolError):
    """MDFU exception for an invalid MDFU packet status
    """

class MdfuUpdateError(MdfuProtocolError):
    """MDFU exception for a failed firmware update
    """
class MdfuPacket():
    """MDFU packet class
    """

class MdfuCmdPacket(MdfuPacket):
    """MDFU command packet
    """
    def __init__(self, sequence_number: int, command: int, data: bytes, sync=False):
        """MDFU command packet initialization

        :param sequence_number: Sequence number for this packet, valid numbers are from 0 to 31
        :type sequence_number: int
        :param command: Command to execute
        :type command: int
        :param data: Packet data
        :type data: bytes
        :param sync: Whether or not this packet should initiate a synchronization of
        the sequence number, defaults to False
        :type sync: bool, optional
        """
        self.sync = sync
        self.command = command
        self.data = data
        if sequence_number > 31 or sequence_number < 0:
            raise ValueError("Valid values for MDFU packet sequence number are 0...31", sequence_number)
        self.sequence_number = sequence_number
        cmd_values = set(item.value for item in MdfuCmd)
        if command not in cmd_values:
            raise MdfuCmdNotSupportedError(f"{hex(command)} is not a valid MDFU command")


    def __repr__(self) -> str:
        return f"""\
Command:         {MdfuCmd(self.command).name} ({hex(self.command)})
Sequence Number: {self.sequence_number}
Sync:            {self.sync}
Data:            {self.data}
"""

    @staticmethod
    def decode_packet(packet: bytes) -> tuple:
        """ Decode a MDFU packet

        :param packet: MDFU packet
        :type packet: Bytes
        :return: Fields of the packet (Sequence number, command, data, sync)
        :rtype: Tuple(Int, Int, Bytes, Bool)
        """
        sequence_field = packet[0]
        sequence_number = sequence_field & 0x1f
        sync = bool(sequence_field & 0x80)
        command = int.from_bytes(packet[1:2], byteorder="little")
        data = packet[2:]
        return sequence_number, command, data, sync

    @classmethod
    def from_binary(cls, packet: bytes):
        """Create MDFU command packet from binary data.

        :param packet: MDFU packet in binary form
        :type packet: Bytes like object
        :return: Command packet object
        :rtype: MdfuCmdPacket
        """
        sequence_number, command, data, sync = cls.decode_packet(packet)
        pack = cls(sequence_number, command, data, sync=sync)
        return pack

    def to_binary(self):
        """Create binary MDFU packet

        :return: MDFU packet in binary form
        :rtype: Bytes
        """
        sequence_field = self.sequence_number | ((1 << 7) if self.sync else 0x00)
        packet =  sequence_field.to_bytes(1, byteorder="little") \
            + self.command.to_bytes(1, byteorder="little") \
            + self.data
        return packet

class MdfuStatusPacket(MdfuPacket):
    """MDFU status packet
    """
    def __init__(self, sequence_number, status, data=bytes(), resend=False):
        """MDFU packet initialization

        :param sequence_number: Sequence number for the packet, valid numbers are from 0 to 31
        :type sequence_number: Int
        :param status: Status code
        :type status: Int
        :param data: Data, defaults to bytes()
        :type data: Bytes like object, optional
        :param resend: Resend flag for the packet, defaults to False
        :type resend: bool, optional
        """
        if sequence_number > 31 or sequence_number < 0:
            raise ValueError("Valid values for MDFU packet sequence number are 0...31")
        self.sequence_number = sequence_number

        status_values = set(item.value for item in MdfuStatus)
        if status not in status_values:
            raise MdfuStatusInvalidError(f"{hex(status)} is not a valid MDFU status")
        self.status = status
        self.resend = resend
        self.data = data

    def __repr__(self) -> str:
        return f"""\
Sequence Number: {self.sequence_number}
Status:          {MdfuStatus(self.status).name} ({hex(self.status)})
Resend:          {self.resend}
Data:            {self.data}
"""
    @staticmethod
    def decode_packet(packet):
        """Decode a status packet

        :param packet: Packet
        :type packet: Bytes like object
        :return: packet sequence number (int), status (int), data (bytes), resend (bool)
        :rtype: tuple(int, int, bytes, bool)
        """
        sequence_field = packet[0]
        sequence_number = sequence_field & 0x1f
        resend = bool(sequence_field & 0x40)
        status = int.from_bytes(packet[1:2], byteorder="little")
        data = packet[2:]
        return sequence_number, status, data, resend

    @classmethod
    def from_binary(cls, packet):
        """Create MDFU status packet from binary data.

        :param packet: MDFU packet in binary form
        :type packet: Bytes like object
        :return: Status packet object
        :rtype: MdfuStatusPacket
        """
        sequence_number, status, data, resend = cls.decode_packet(packet)
        pack = cls(sequence_number, status, data, resend=resend)
        return pack

    def to_binary(self):
        """Create binary MDFU packet

        :return: MDFU packet in binary form
        :rtype: Bytes
        """
        sequence_field = self.sequence_number | ((1 << 6) if self.resend else 0x00)
        packet =  sequence_field.to_bytes(1, byteorder="little") \
            + self.status.to_bytes(1, byteorder="little") \
            + self.data
        return packet

class Mdfu():
    """MDFU protocol
    """
    def __init__(self, transport: Transport, timeout=5, retries=5):
        """Class initialization

        :param transport: Defines wich transport layer the MDFU protocol uses
        :type transport: Transport
        :param timeout: Communication timeout in seconds
        :type timeout: Int, defaults to 5
        :param retries: How often a failed command should be retried.
        :type retries: Int, defaults to 5
        :type chunk_size: int, optional
        """
        self.transport = transport
        self.sequence_number = 0
        self.retries = retries
        self.timeout_s = timeout
        self.chunk_size = 0
        self.client_packet_buffer_cnt = 1
        self.logger = getLogger("pymdfu.MdfuHost")

    def run_upgrade(self, image):
        """Executes the upgrade process

        :param image: File image
        :type image: Bytes like object
        :raises MdfuUpdateError: For an unsucessfull update
        """
        try:
            self.transport.open()
            # Start session by:
            # - resetting sequence number to zero
            # - sync sequence number with target (in get_transfer_parameters command)
            # - getting transfer parameters
            self.sequence_number = 0
            self.get_transfer_parameters(sync=True)

            chunks = chunkify(image, self.chunk_size)

            self.start_transfer()
            for chunk in chunks:
                self.write_chunk(chunk)
            self.get_image_state()
            self.end_transfer()

        except MdfuProtocolError as err:
            raise MdfuUpdateError from err
        except TransportError as err:
            raise MdfuUpdateError from err
        finally:
            self.transport.close()

    def get_transfer_parameters(self, sync=False):
        """Executes the GetTransferParameter command

            Stores transfer parameters as class attributes.
        """
        response = self.send_cmd(MdfuCmd.GET_TRANSFER_PARAMETERS, sync=sync)
        try:
            # Default conversion for from_bytes is not two's complement = unsigned
            self.chunk_size = int.from_bytes(response.data[0:2], byteorder="little")
            self.client_packet_buffer_cnt = response.data[2]
        except IndexError as err:
            self.logger.error("Received invalid MDFU transfer parameters 0x%x", response.data.hex())
            raise MdfuProtocolError from err
        self.logger.debug("MDFU client transfer parameters are: Chunk size=%s, buffer count=%i",\
                           self.chunk_size, self.client_packet_buffer_cnt)

    def start_transfer(self, sync=False):
        """Executes Start Transfer command
        """
        self.logger.debug("Starting MDFU file transfer")
        self.send_cmd(MdfuCmd.START_TRANSFER, sync=sync)

    def write_chunk(self, chunk):
        """Executes Write Chunk command

        :param chunk: Piece of the upgrade image file
        :type chunk: Bytes like object
        """
        self.send_cmd(MdfuCmd.WRITE_CHUNK, data=chunk)

    def get_image_state(self):
        """Executes Get Image State command
        """
        self.send_cmd(MdfuCmd.GET_IMAGE_STATE)

    def end_transfer(self):
        """Executes End Transfer command
        """
        self.logger.debug("Ending MDFU file transfer")
        self.send_cmd(MdfuCmd.END_TRANSFER)

    def send_cmd(self, command: MdfuCmd, data=bytes(), sync=False) -> MdfuStatusPacket:
        """Send a command packet to MDFU client

        :param command: Command to send
        :type command: MdfuCmd
        :param data: Data to send, defaults to None
        :type data: Bytes like object, optional
        :param sync: Synchronize packet sequence number with client. When set the client
        will set its sequence number to the one received in this command packet.
        :type sync: Bool
        :return: MDFU status packet
        :rtype: MdfuStatusPacket
        """
        cmd_packet = MdfuCmdPacket(self.sequence_number, command.value, data, sync=sync)
        self.logger.debug("Sending MDFU command packet:\n%s\n", cmd_packet)
        retries = self.retries
        while retries:
            try:
                retries -= 1
                self.transport.write(cmd_packet.to_binary())
                status_packet = self.transport.read()
                status_packet = MdfuStatusPacket.from_binary(status_packet)
                self.logger.debug("Received a MDFU status packet\n%s\n", status_packet)

                if status_packet.resend:
                    self.logger.debug("Resending MDFU packet. Packet status was %s",\
                            MdfuStatus(status_packet.status).name)
                    continue
                elif status_packet.status == MdfuStatus.SUCCESS.value:
                    self._increment_sequence_number()
                    break
                else:
                    self.logger.error("Received MDFU status packet with %s", MdfuStatus(status_packet.status).name)
                    self._increment_sequence_number()
                    raise MdfuProtocolError()

            except TransportError as exc:
                self.logger.error(exc)
            except (MdfuStatusInvalidError, MdfuCmdNotSupportedError) as exc:
                self.logger.error(exc)
                raise MdfuProtocolError(exc) from exc
        if retries == 0:
            msg = f"Tried {self.retries} times to send command " + \
                    f"{MdfuCmd(cmd_packet.command).name} without success"
            self.logger.error(msg)
            raise MdfuProtocolError(msg)

        return status_packet

    def _increment_sequence_number(self):
        self.sequence_number = (self.sequence_number + 1) & 0x1f
