import time

import serial
import json
from serial.tools.list_ports import comports
from serial import Serial

from datetime import datetime


class SerialPort:
    BAUD_RATE = {'110': 110, '300': 300, '600': 600, '1200': 1200, '2400': 2400, '4800': 4800, '9600': 9600,
                 '14400': 14400,
                 '19200': 19200, '38400': 38400, '57600': 57600, '115200': 115200, '128000': 128000, '256000': 256000}
    PARITY = {'none': serial.PARITY_NONE, 'even': serial.PARITY_EVEN, 'odd': serial.PARITY_ODD,
              'mark': serial.PARITY_MARK, 'space': serial.PARITY_SPACE}
    STOP_BIT = {'1': serial.STOPBITS_ONE, '1.5': serial.STOPBITS_ONE_POINT_FIVE, '2': serial.STOPBITS_TWO}
    BITE_SIZE = {'5': serial.FIVEBITS, '6': serial.SIXBITS, '7': serial.SEVENBITS, '8': serial.EIGHTBITS}
    MESSAGE = b'QPIWS'

    def __init__(self, config_file):
        self._config_file = config_file
        self._serial_port_config = config_file
        self._serial_port = None
        self.__list_of_serial_device = {}

        try:
            self._name = self._serial_port_config['name']
        except KeyError:
            self._name = self._serial_port_config['port']
        self._port_device = self._serial_port_config['port']
        try:
            self._baud_rate = self._serial_port_config['baudrate']
            self._timeout = self._serial_port_config['timeout']
        except serial.SerialException as e:
            print(f'Serial port error: {str(e)}.\n'
                  f'Please check config file.')

    def __str__(self):
        _message = f'Device: {self._port_device}   |   '
        _message += f'Status: open' if self._serial_port.isOpen() else f'Status: Close'
        return _message

    def get_name(self) -> str:
        return self._name

    def get_port(self):
        return self._serial_port

    def readline(self):
        return self._serial_port.readline()

    def write(self, command):
        self._serial_port.write(self.MESSAGE + b'\r')

    def close(self):
        self._serial_port.close()

    def open(self):
        try:
            print(f'Trying open serial port.')
            self._serial_port = Serial(self._port_device, baudrate=self._baud_rate, timeout=self._timeout)
            print(f'Serial port opened.', self._serial_port.is_open)

        except serial.serialutil.SerialException as e:
            print(f'Unable to open serial port: \n{str(e)}')


if __name__ == '__main__':
    port = SerialPort({
        "name": "serial port",
        "port": "/dev/ttyUSB0",
        "baudrate": 9600,
        "timeout": 3
    })
    port.open()
    port.write(b'QPIWS')
    print(port.readline())
    print(port.readline())
    port.close()
