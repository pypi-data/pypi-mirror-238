from pytdv2.TrustedDevice import TrustedDevice
from pytdv2.utils import Utils


class TrustedDeviceImpl(TrustedDevice):
    def __init__(self, path_key):
        try:
            self.private_key = self.read_key_from_file(path_key)
        except IOError:
            raise IOError("Key not found")

    def read_key_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except IOError:
            print('File not accessible')
            return None

    def extract(self, meta):
        u = Utils(self.private_key)
        return u.decrypt_response(meta)
