from pytdv2.TrustedDeviceImpl import TrustedDeviceImpl


class Fazpass:
    @staticmethod
    def initialize(path_key):
        if not path_key:
            raise ValueError("private keys must be non-null and not empty.")
        return TrustedDeviceImpl(path_key)
