from typing import List, Dict

class Device:
    def __init__(self, 
                 name: str, 
                 os_version: str, 
                 series: str, 
                 cpu: str, 
                 id: str):
        self.name = name
        self.os_version = os_version
        self.series = series
        self.cpu = cpu
        self.id = id

class Meta:
    def __init__(self,
                 fazpass_id: str,
                 is_active: bool,
                 scoring: float,
                 risk_level: str,
                 time_stamp: str,
                 platform: str,
                 is_rooted: bool,
                 is_emulator: bool,
                 is_gps_spoof: bool,
                 is_app_tempering: bool,
                 is_vpn: bool,
                 is_clone_app: bool,
                 is_screen_sharing: bool,
                 is_debug: bool,
                 application: str,
                 device_id: Device,
                 sim_serial: List[str],
                 sim_operator: List[str],
                 geolocation: Dict[str, str],
                 client_ip: str,
                 is_notifiable: bool,
                 notifiable_devices: List[Device]):
        self.fazpass_id = fazpass_id
        self.is_active = is_active
        self.scoring = scoring
        self.risk_level = risk_level
        self.time_stamp = time_stamp
        self.platform = platform
        self.is_rooted = is_rooted
        self.is_emulator = is_emulator
        self.is_gps_spoof = is_gps_spoof
        self.is_app_tempering = is_app_tempering
        self.is_vpn = is_vpn
        self.is_clone_app = is_clone_app
        self.is_screen_sharing = is_screen_sharing
        self.is_debug = is_debug
        self.application = application
        self.device_id = device_id
        self.sim_serial = sim_serial
        self.sim_operator = sim_operator
        self.geolocation = geolocation
        self.client_ip = client_ip
        self.is_notifiable = is_notifiable
        self.notifiable_devices = notifiable_devices
