import json
import time

import serial
from serial import Serial

queries_and_responses = [
    [b'QPI', 'PI<NN>'],
    [b'QID', 'ABCDEEFFGXXXXX'],
    [b'QVFW', 'VERFW:<NNNNN.NN>'],
    [b'QVFW2', 'VERFW2:<NNNNN.NN>'],
    [b'QMD', 'TTTTTTTTTTTTTTTWWWWWWW KK P/P MMM NNN RR BB.B'],
    [b'QPIRI', 'BBB.B FF.F III.I EEE.E DDD.D AA.A GGG.G R MM T'],
    [b'QPIGS', 'MMM.M CBBBBB HH.H CZZZ.Z LLL.L MMMMM NN.N QQQ.Q DDD KKK.K VVV.V SSS.S RRR.R XXX PPPPP EEEEE OOOOO UUU.U WWW.W YYY.Y TTT.T b7b6b5b4b3b2b1b0a0a1'],
    [b'QMOD', 'M'],
    [b'QPIWS', 'a0a1.....a62a127'],
    [b'QFLAG', 'ExxxDxxx'],
    [b'QT', 'YYYYMMDDHHMMSS'],
    [b'QET', 'NNNNNNNN'],
    [b'QEY', 'NNNNNNNN'],
    [b'QEM', 'NNNNNN'],
    [b'QED', 'NNNNNN'],
    [b'QEH', 'NNNNN'],
    [b'QGOV', 'HHH.H LLL.L'],
    [b'QGOF', 'FF.F GG.G'],
    [b'QOPMP', 'LLLLL'],
    [b'QMPPTV', 'HHH LLL'],
    [b'QPVIPV', 'HHH LLL'],
    [b'QLST', 'LL'],
    [b'QTPR', 'LLL.L SSS.S TTT.T'],
    [b'QDI2', 'HH.H LL.L NNN'],
    [b'QDI', 'BBB.B CCC.C DD.D EE.E FFF.F GGG.G HH.H II.I JJJ KKK LLL MMM NNNNN OOO PP QQ RRR SS'],
    [b'QGLTV', 'HHH LLL'],
    [b'QCHGS', 'AA.A BB.B CC.C DD.D'],
    [b'QVFTR', 'HHH.H MMM.M LLL.L NNN.N ZZ.Z XX.X WW.W YY.Y AAA BBB'],
    [b'QPIHF', 'KK YYYYMMDDHHMMSS AAA.A BBB.B CCC.C DDD.D EEE.E FFF.F GGG.G HHH.H III.I JJ.J CKKK.K LLL MMM.M NNN.N OO.O PPP.P QQQ.Q <bn><cr>'],
    [b'QPICF', 'KK NN']
]

class SerialPort:
    BAUD_RATE = {'110': 110, '300': 300, '600': 600, '1200': 1200, '2400': 2400, '4800': 4800, '9600': 9600,
                 '14400': 14400,
                 '19200': 19200, '38400': 38400, '57600': 57600, '115200': 115200, '128000': 128000, '256000': 256000}
    PARITY = {'none': serial.PARITY_NONE, 'even': serial.PARITY_EVEN, 'odd': serial.PARITY_ODD,
              'mark': serial.PARITY_MARK, 'space': serial.PARITY_SPACE}
    STOP_BIT = {'1': serial.STOPBITS_ONE, '1.5': serial.STOPBITS_ONE_POINT_FIVE, '2': serial.STOPBITS_TWO}
    BITE_SIZE = {'5': serial.FIVEBITS, '6': serial.SIXBITS, '7': serial.SEVENBITS, '8': serial.EIGHTBITS}
    MESSAGE = b'QPIGS'

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
        return self._serial_port.readline().decode('utf-8', errors='ignore')

    def write(self, command):
        self._serial_port.write(command + b'\r')

    def close(self):
        self._serial_port.close()

    def open(self):
        try:
            print(f'Trying open serial port.')
            self._serial_port = Serial(self._port_device, baudrate=self._baud_rate, timeout=self._timeout)
            print(f'Serial port opened.', self._serial_port.is_open)

        except serial.serialutil.SerialException as e:
            print(f'Unable to open serial port: \n{str(e)}')


class RS232Protocol:

    def __init__(self, question, data):
        self._question = question
        self._data = data

    def _convert_int_number(self, bit_list, pointer, unit):
        binary_string = ''.join(map(str, bit_list))
        integer_value = int(binary_string, 2)
        integer_value = round(integer_value/10**pointer,pointer)
        print(integer_value)


class DecoderQ:
    def __init__(self, inverter_path):
        self.answer = None
        self._inverter = {}
        self.open_file_inverter(inverter_path)


    def open_file_inverter(self, fila_path) -> None:
        with open(fila_path, 'r') as file:
            self._inverter = json.loads(file.read())

    def convert(self, sentence: str, answer: str):
        _list_of_keys = []
        _converted_values = {}
        for key in self._inverter[sentence].keys():
            _list_of_keys.append(key)
        self.answer = answer.split(' ').copy()
        try:
            for number, value in enumerate(self.answer):
                _converted_values[_list_of_keys[number]] = value + ' ' + self._inverter[sentence][_list_of_keys[number]]['unit']
                print(_converted_values)
        except IndexError:
            pass



if __name__ == '__main__':
    decoder = DecoderQ('configuration/easun.json')
    decoder.convert('QDI','230.0 50.0 0030 44.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 1 0 1 0 54.0 0 1 224')
    port = SerialPort({
        "name": "serial port",
        "port": "/dev/ttyUSB0",
        "baudrate": 2400,
        "timeout": 3
    })

    port.open()
    port.write(b'QDI')
    print(port.readline())
    for task in queries_and_responses:
        print(task[0])

        port.write(task[0])
        print(task[1])
        print(port.readline())
        time.sleep(0.2)


    port.close()
