"""Transport interface for MDFU
"""
import abc

class TransportError(Exception):
    """Generic transport exception"""

class Transport(object, metaclass=abc.ABCMeta):
    """Abstract class for transport interface definition

    :raises NotImplementedError: Exception when interface implementation does not
    follow interface specification
    """
    @abc.abstractmethod
    def open(self):
        raise NotImplementedError('users must define open to use this base class')
    @abc.abstractmethod
    def close(self):
        raise NotImplementedError('users must define close to use this base class')
    @abc.abstractmethod
    def read(self):
        raise NotImplementedError('users must define read to use this base class')
    @abc.abstractmethod
    def write(self, data):
        raise NotImplementedError('users must define write to use this base class')

class I2cTransport(Transport):
    def open(self, **kwargs):
        pass
    def close(self):
        pass
    def read(self):
        pass
    def write(self, data):
        pass
