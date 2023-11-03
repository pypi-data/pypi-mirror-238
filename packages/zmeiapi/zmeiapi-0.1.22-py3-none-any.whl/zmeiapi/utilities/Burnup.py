import msgpack
import bz2


def read_burnup_concentrations(filename: str) -> list:
    if filename.endswith('.mpbz'):
        with bz2.open(filename, 'rb') as file:
            _concentrations = file.read()

        concentrations = msgpack.unpackb(_concentrations)
        return concentrations
