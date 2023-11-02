import datetime
import os
from typing import Literal
from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient
from wiliot_deployment_tools.common.analysis_data_bricks import initialize_logger
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_core.utils.utils import WiliotDir
from wiliot_deployment_tools.interface.ble_sniffer import BLESniffer
from wiliot_deployment_tools.interface.uart_if import UARTError, UARTInterface
from wiliot_deployment_tools.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.interface.mqtt import MqttClient
from wiliot_deployment_tools.gw_certificate.tests import *
from wiliot_deployment_tools.interface.uart_ports import get_uart_ports

class GWCertificateError(Exception):
    pass

class GWCertificate:
    def __init__(self, gw_id, api_key, owner_id, env='prod', cloud:Literal['aws', 'gcp']='aws', random=False, legacy=False):
        self.env_dirs = WiliotDir()
        current_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        self.certificate_dir = os.path.join(self.env_dirs.get_wiliot_root_app_dir(), 'gw-certificate', current_datetime)
        self.env_dirs.create_dir(self.certificate_dir)
        self.start_timestamp = initialize_logger(self.certificate_dir)
        self.gw_id = gw_id
        self.owner_id = owner_id
        if cloud == 'gcp':
            self.edge = ExtendedEdgeClient(api_key=api_key, owner_id=owner_id, env=env, region='us-central1', cloud='gcp')
        else:
            self.edge = ExtendedEdgeClient(api_key, owner_id, env=env,)
        self.mqttc = MqttClient(gw_id, owner_id, f'{self.certificate_dir}/{self.start_timestamp}_mqtt.log')
        self.uart_comports = get_uart_ports()
        if random:
            debug_print('Randomizing Test!')
        self.randomize = random
        if legacy:
            debug_print('Working in LEGACY DevMode!')
        self.legacy = legacy
        debug_print(f'UART Ports:{self.uart_comports}')
        if len(self.uart_comports) < 1:
            raise GWCertificateError('A Wiliot GW needs to be connected to USB!')
        self.uart = None
        for port in self.uart_comports:
            try:
                self.uart = UARTInterface(port)
                break
            except UARTError as e:
                debug_print(f'Port: {port} - {e}')
        if type(self.uart) is not UARTInterface:
            raise GWCertificateError("Cannot initialize any port!")
        self.ble_sim = BLESimulator(self.uart)
        self.sniffer = BLESniffer(self.uart)
        self.tests = [t(**self.__dict__) for t in TESTS]

    
    def run_tests(self, skip_online_check=False):
        if not skip_online_check:
            assert self.edge.check_gw_online([self.gw_id]) is True, 'GW Not online!'
        for test in self.tests:
            test.run()
        for test in self.tests:
            test.end_test()
            
if __name__ == "__main__":
    # gwc = GWCertificate('GW0CDC7EDB2000', 'OTRiZmExNDQtYzBiYi00NDcyLTk1N2MtNGU3OTkxZGViYjE2OkREV3dTYjExQXFuclhVNmZHdHl0ZTJSeW82VmFkMGZ6Q2xHZFZUMUhfS0k=', '832742983939', legacy=True)
    gwc = GWCertificate('GW0CDC7EDB2000', 'MDc5NjNlZGMtYjZlMS00MjZjLTk0NjUtNjRmMWE1NDYzOWVlOmtteFFGNEdOMExTSEMwdW9iTDFTUWdMSUdJUjRIdEY3bU1TMm96SHNiLTg=', '575908782189', legacy=True, cloud='gcp')
    gwc.run_tests()