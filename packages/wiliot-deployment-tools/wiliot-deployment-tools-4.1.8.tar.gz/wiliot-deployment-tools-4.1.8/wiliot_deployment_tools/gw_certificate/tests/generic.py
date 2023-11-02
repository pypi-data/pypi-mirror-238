import datetime
import os
from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.interface.if_defines import SEP
from wiliot_deployment_tools.interface.mqtt import MqttClient

PASS_STATUS = {True: 'PASS', False: 'FAIL'}

class GenericTest:
    def __init__(self, mqttc: MqttClient, ble_sim: BLESimulator, edge: ExtendedEdgeClient, gw_id, owner_id, test_name, **kwargs):
        # Clients
        self.mqttc = mqttc
        self.ble_sim = ble_sim
        self.edge = edge
        
        # Test-Related
        self.report = ''
        self.test_pass = False
        self.start_time = None
        self.test_name = test_name
        self.test_dir = os.path.join(self.certificate_dir, self.test_name)
        self.env_dirs.create_dir(self.test_dir)
        
    def run(self):
        self.start_time = datetime.datetime.now()
        debug_print(f"Starting Test {self.test_name} : {self.start_time}")
        
    def runtime(self):
        return datetime.datetime.now() - self.start_time
    
    def add_to_test_report(self, report):
        self.report += '\n' + report
    
    def end_test(self):
        debug_print(f'\n{SEP}')
        debug_print(f'{self.test_name} {PASS_STATUS[self.test_pass]}, Running time {self.runtime()}')
        debug_print(self.report)

class GenericStage():
    def __init__(self, stage_name, **kwargs):
        #Stage Params
        self.stage_name = stage_name
        self.stage_pass = False
        self.report = ''
        self.start_time = None
        self.csv_path = os.path.join(self.test_dir, f'{self.stage_name}.csv')
        
    def prepare_stage(self):
        debug_print(f'### Starting Stage: {self.stage_name}')

    def add_to_stage_report(self, report):
        self.report += '\n' + report
    
    def generate_stage_report(self):
        return self.report
