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

    def __init__(self, config_file):
        self._config_file = config_file
        self._serial_port_config = {}
        self._load_config()
        self._serial_port = None
        self.__list_of_serial_device = {}

        try:
            self._name = self._serial_port_config['name']
        except KeyError:
            self._name = self._serial_port_config['port']
        self._port_device = self._serial_port_config['port']
        try:
            self._baud_rate = self._serial_port_config['baudrate']
            self._parity = self._serial_port_config['parity']
            self._stop_bit = self._serial_port_config['stop_bit']
            self._bite_size = self._serial_port_config['bit_size']
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

    def close(self):
        self._serial_port.close()

    def _load_config(self) -> None:
        print(self._config_file)
        with open(self._config_file, 'r') as file:
            self._serial_port_config = json.loads(file.read())

    def _set_dict_of_serial_ports(self):
        self.dict_of_serial_ports = {}
        for port in comports():
            self.dict_of_serial_ports[port.name] = {'device': port.device,
                                                    'description': port.description,
                                                    'hwid': port.hwid,
                                                    'interface': port.interface}
            print(self.dict_of_serial_ports)

    def get_dict_of_serial_port(self):
        self._set_dict_of_serial_ports()
        __list_serial_ports = {}
        for counter, item in enumerate(self.dict_of_serial_ports.keys(), start=1):
            __list_serial_ports[str(counter)] = self.dict_of_serial_ports[item]["device"]
        self.__list_of_serial_device = __list_serial_ports
        return __list_serial_ports

    def open(self):
        try:
            print(f'Trying open serial port.')
            self._serial_port = Serial(self._port_device, baudrate=self._baud_rate, parity=self._parity,
                                       stopbits=self._stop_bit, bytesize=self._bite_size, timeout=self._timeout)
            print(f'Serial port opened.', self._serial_port.is_open)

        except serial.serialutil.SerialException as e:
            print(f'Unable to open serial port: \n{str(e)}')


