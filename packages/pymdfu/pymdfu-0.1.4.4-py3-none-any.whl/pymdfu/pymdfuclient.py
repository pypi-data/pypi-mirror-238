
"""MDFU client"""
import threading
from logging import getLogger
from collections import deque
from .mdfu import MdfuCmd, MdfuCmdPacket, MdfuStatusPacket, MdfuStatus,\
                    MdfuCmdNotSupportedError
from .transport import TransportError

class MdfuClient(threading.Thread):
    """MDFU client

    This class can be used to simulate a MDFU client
    """
    def __init__(self, transport, chunk_size=128, buffer_count=1):
        """Class initialization

        :param chunk_size: Chunk size for Write Chunk commands, defaults to 128
        :type chunk_size: int, optional
        """
        self.chunk_size = chunk_size
        self.buffer_count = buffer_count
        self.queue = deque()
        self.sequence_number = 0
        self.logger = getLogger("pymdfu.MdfuClient")
        self.resend = False
        self.packet_error_rate = 5
        self.packet_error_countdown = self.packet_error_rate
        self.transport = transport
        self.stop_event = threading.Event()
        super().__init__(name="MDFU client")

    def stop(self):
        """Stop MDFU client
        """
        # Send event to stop the thread
        self.logger.debug("Stopping MDFU client")
        self.stop_event.set()
        # Wait for thread to end
        self.join()

    def run(self):
        self.transport.open()
        while True:
            data = None
            try:
                # TODO this could be non-blocking, right now we just time out and try again.
                # If we don't block we can service other tasks more often (right now just
                # thread termination)
                data = self.transport.read()
            except TimeoutError:
                pass
            except TransportError:
                # TODO what should we do on transport errors?
                # What should be sent to the host? Maybe a packet with last known good sequence number?
                pass
            if self.stop_event.is_set():
                break
            if data:
                try:
                    packet = MdfuCmdPacket.from_binary(data)
                except ValueError:
                    self.logger.warning("MDFU client got an invalid packet: 0x%x\n", data.hex())
                    # TODO What should we do here if the MDFU packet cannot be decoded without error?
                    # Sending back a status packed with last known good sequence number (+1)?
                    # what if the corrupted packet is the first packet with a sync?
                    status_packet = MdfuStatusPacket(self.sequence_number + 1,\
                                                    MdfuStatus.PACKET_TRANSPORT_FAILURE.value)
                    self.queue.appendleft(status_packet)
                    continue
                except MdfuCmdNotSupportedError:
                    status_packet = MdfuStatusPacket(self.sequence_number + 1, MdfuStatus.NOT_SUPPORTED.value)
                    self.queue.appendleft(status_packet)
                    continue
                self.logger.debug("MDFU Client got a packet\n%s\n", packet)

                if packet.sync:
                    self.sequence_number = packet.sequence_number
                else:
                    if not self.resend: # increment only when this is not a packet resend
                        self._increment_sequence_number()
                    if self.sequence_number != packet.sequence_number:
                        self.logger.warning("Wrong sequence number, expected " \
                                            "%d but got %d", self.sequence_number, packet.sequence_number)
                        # TODO what should we report to the host if the sequence number does not match?
                        # Create a new status code and send this? status code = ProtocolError?
                        status_packet = MdfuStatusPacket(self.sequence_number,\
                                        MdfuStatus.PACKET_TRANSPORT_FAILURE.value)
                        self.queue.appendleft(status_packet)
                        continue

                if packet.command == MdfuCmd.GET_TRANSFER_PARAMETERS.value:
                    self.cmd_get_transfer_parameters(packet)
                elif packet.command == MdfuCmd.WRITE_CHUNK.value:
                    self.cmd_write_chunk(packet)
                elif packet.command == MdfuCmd.START_TRANSFER.value:
                    self.cmd_start_transfer(packet)
                elif packet.command == MdfuCmd.END_TRANSFER.value:
                    self.cmd_end_transfer(packet)
                elif packet.command == MdfuCmd.GET_IMAGE_STATE.value:
                    self.cmd_get_image_state(packet)
                else:
                    self.logger.error("Command not supported %s", packet.command)
                    status_packet = MdfuStatusPacket(packet.sequence_number, MdfuStatus.NOT_SUPPORTED.value, data)
                    self.queue.appendleft(status_packet)
            if len(self.queue):
                self.transport.write(self.queue.pop().to_binary())
        self.transport.close()
        self.queue.clear()
        self.sequence_number = 0
        self.logger.debug("MDFU client stopped")

    def _increment_sequence_number(self):
        """Increment the sequence number
        """
        self.sequence_number = (self.sequence_number + 1) & 0x1f

    def cmd_get_transfer_parameters(self, packet):
        """Handle Get Transfer Parameters command

        :param packet: MDFU command packet
        :type packet: MdfuCmdPacket
        """
        data = self.chunk_size.to_bytes(2, byteorder="little")
        data += bytes([self.buffer_count])
        status_packet = MdfuStatusPacket(packet.sequence_number, MdfuStatus.SUCCESS.value, data)
        self.queue.appendleft(status_packet)

    def cmd_start_transfer(self, packet):
        """Handle Start Transfer command

        :param packet: MDFU command packet
        :type packet: MdfuCmdPacket
        """
        status_packet = MdfuStatusPacket(packet.sequence_number, MdfuStatus.SUCCESS.value)
        self.queue.appendleft(status_packet)

    def cmd_write_chunk(self, packet):
        """Handle Write Chunk command

        :param packet: MDFU command packet
        :type packet: MdfuCmdPacket
        """
        status_packet = MdfuStatusPacket(packet.sequence_number, MdfuStatus.SUCCESS.value)
        self.queue.appendleft(status_packet)

    def cmd_get_image_state(self, packet):
        """Handle Get image state command

        :param packet: MDFU command packet
        :type packet: MdfuCmdPacket
        """
        status_packet = MdfuStatusPacket(packet.sequence_number, MdfuStatus.SUCCESS.value)
        self.queue.appendleft(status_packet)

    def cmd_end_transfer(self, packet):
        """Handle End Transfer command

        :param packet: MDFU command packet
        :type packet: MdfuCmdPacket
        """
        status_packet = MdfuStatusPacket(packet.sequence_number, MdfuStatus.SUCCESS.value)
        self.queue.appendleft(status_packet)


if __name__ == "__main__":
    from .mac import MacFactory
    from .mdfu import Mdfu
    from .uart_transport import UartTransport
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.root.setLevel(logging.DEBUG)
    upgrade_image = bytes(512 * [0xff])

    mac_host, mac_client = MacFactory.get_bytes_based_mac()
    transport_client = UartTransport(mac=mac_client)
    client = MdfuClient(transport_client)

    transport_host = UartTransport(mac=mac_host)
    host = Mdfu(transport_host)

    client.start()
    host.run_upgrade(upgrade_image)
    client.stop()
