from base64 import b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import json

from pytdv2.device import Device, Meta


def get_private_key(base64_private_key):
    try:
        # private_key_data = b64decode(base64_private_key)
        private_key = RSA.import_key(base64_private_key)
        return private_key
    except Exception as e:
        raise Exception("Error generating private key") from e


class Utils:
    def __init__(self, private_key):
        self.private_key = private_key

    def decrypt_response(self, encrypted_meta):
        try:
            encrypted_bytes = b64decode(encrypted_meta)
            private_key = get_private_key(self.private_key)
            cipher = PKCS1_v1_5.new(private_key)
            decrypted_bytes = cipher.decrypt(encrypted_bytes, Meta)
            print(decrypted_bytes)
            json_str = decrypted_bytes.decode("utf-8")

            # Langkah 2: Ubah string JSON menjadi dictionary
            data = json.loads(json_str)

            # Langkah 3: Buat objek Meta dari dictionary
            device = Device(**data["device_id"])
            meta_obj = Meta(
                fazpass_id=data.get("fazpass_id", None),
                scoring=data.get("scoring", None),
                risk_level=data.get("risk_level", None),
                is_active=data["is_active"],
                time_stamp=data["time_stamp"],
                platform=data["platform"],
                is_rooted=data["is_rooted"],
                is_emulator=data["is_emulator"],
                is_gps_spoof=data["is_gps_spoof"],
                is_app_tempering=data["is_app_tempering"],
                is_vpn=data["is_vpn"],
                is_clone_app=data["is_clone_app"],
                is_screen_sharing=data["is_screen_sharing"],
                is_debug=data["is_debug"],
                application=data["application"],
                device_id=device,
                sim_serial=data["sim_serial"],
                sim_operator=data["sim_operator"],
                geolocation=data["geolocation"],
                client_ip=data["client_ip"],
                is_notifiable=data.get("is_notifiable", None),
                notifiable_devices=None
            )
            return meta_obj
        except Exception as e:
            print(f"Error: {e}")
            return None
