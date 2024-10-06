import json


class File:
    def __init__(self, path):
        self._file = None
        self._path = path

    def get_contend(self) -> dict:
        _contend = {}
        with open(self._path, 'r') as file:
            _contend = json.loads(file.read())
        return _contend


class Controller:

    def __init__(self, **kwargs):
        try:
            self.serial_port_config_file = File(kwargs['config_file'])
            self.serial_port_config = self.serial_port_config_file.get_contend()
        except KeyError:
            pass

if __name__ == '__main__':
    Controller(config_file='configuration/config.json')