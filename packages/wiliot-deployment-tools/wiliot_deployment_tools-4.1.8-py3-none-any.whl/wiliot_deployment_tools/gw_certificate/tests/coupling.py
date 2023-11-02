import datetime
import os
import time
import pandas as pd
import tabulate
from wiliot_deployment_tools.ag.ut_defines import BRIDGE_ID, NFPKT, PAYLOAD, RSSI
from wiliot_deployment_tools.api.extended_api import GatewayType
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.interface.if_defines import BRIDGES, DEFAULT_DELAY, DUPLICATIONS, MAX_NFPKT, MAX_RSSI, SEP, TIME_DELAYS
from wiliot_deployment_tools.interface.uart_if import UARTInterface
from wiliot_deployment_tools.gw_certificate.tests.static.coupling_defines import *
from wiliot_deployment_tools.interface.mqtt import MqttClient
from wiliot_deployment_tools.interface.pkt_generator import BrgPktGenerator, BrgPktGeneratorNetwork, TagPktGenerator
from wiliot_deployment_tools.gw_certificate.tests.static.generated_packet_table import TEST_COUPLING, CouplingRunData
from wiliot_deployment_tools.gw_certificate.tests.generic import PASS_STATUS, GenericTest, GenericStage
from wiliot_deployment_tools.interface.packet_error import PacketError


# TEST STAGES

class CouplingTestError(Exception):
    pass

class GenericCouplingStage(GenericStage):
    def __init__(self, mqttc:MqttClient, ble_sim:BLESimulator, stage_name, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(stage_name=stage_name, **self.__dict__)
        
        #Clients
        self.mqttc = mqttc
        self.ble_sim = ble_sim

        # Packets list
        self.local_pkts = []
        self.mqtt_pkts = []
        
        # Packet Error / Run data
        self.packet_error = PacketError()
        self.run_data = CouplingRunData
    
    def prepare_stage(self):
        super().prepare_stage()
        self.mqttc.flash_pkts()
        self.ble_sim.set_sim_mode(True)
        
    def fetch_mqtt_from_stage(self):
        def process_payload(packet:dict):
            payload = packet[PAYLOAD]
            payload = payload.upper()
            if len(payload) == 62:
                if payload[:4] == '1E16':
                    payload = payload [4:]
            # big2little endian
            if payload[:4] == 'FCC6':
                payload = 'C6FC' + payload[4:]
            packet[PAYLOAD] = payload
            return packet
        mqtt_pkts = self.mqttc.get_coupled_tags_pkts()
        self.mqtt_pkts = list(map(lambda p: process_payload(p), mqtt_pkts))

    def compare_local_mqtt(self):
        self.fetch_mqtt_from_stage()
        local_pkts_df = pd.DataFrame(self.local_pkts)
        mqtt_pkts_df = pd.DataFrame(self.mqtt_pkts)
        if not set(SHARED_COLUMNS) <= set(mqtt_pkts_df.columns):
            missing_columns = list(set(SHARED_COLUMNS) - set(mqtt_pkts_df.columns))
            for missing_column in missing_columns:
                if missing_column in OBJECT_COLUMNS:
                    mqtt_pkts_df[missing_column] = ''
                if missing_column in INT64_COLUMNS:
                    mqtt_pkts_df[missing_column] = 0
        comparison = local_pkts_df
        received_pkts_df = pd.merge(local_pkts_df[SHARED_COLUMNS], mqtt_pkts_df[SHARED_COLUMNS], how='inner')
        received_pkts = set(received_pkts_df[PAYLOAD])
        comparison[RECEIVED] = comparison[PAYLOAD].isin(received_pkts)
        comparison['pkt_id'] = comparison['payload'].apply(lambda x: x[-8:])
        self.comparison = comparison
                
    def generate_stage_report(self):
        self.compare_local_mqtt()
        report = []
        num_pkts_sent = len(self.comparison)
        num_pkts_received = self.comparison['received'].eq(True).sum()
        self.stage_pass = num_pkts_sent == num_pkts_received
        report.append((('Number of coupled packets sent'), num_pkts_sent))
        report.append((('Number of coupled packets received'), num_pkts_received))
        self.add_to_stage_report(f'---Stage {self.stage_name} {PASS_STATUS[self.stage_pass]}, Running time {datetime.datetime.now() - self.start_time}')
        self.add_to_stage_report(tabulate.tabulate(pd.DataFrame(report), showindex=False))
        not_received = self.comparison[self.comparison[RECEIVED]==False][REPORT_COLUMNS]
        if len(not_received)>0:
            self.add_to_stage_report('Packets not received:')
            self.add_to_stage_report(tabulate.tabulate(not_received, headers='keys', showindex=False))
        self.comparison.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        return self.report
    
class InitStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for idx, duplication in enumerate(INIT_STAGES_DUPLICATIONS):
            new_pkt = self.pkt_gen.get_new_data_si()
            # First 2 runs generate smallest RSSI/NFPKT
            # Last 2 runs generate biggest RSSI/NFPKT
            if idx < 2:
                self.pkt_gen.set_rssi_nfpkt(rssi=idx, nfpkt=idx)
            else:
                self.pkt_gen.set_rssi_nfpkt(rssi=MAX_RSSI-idx+2, nfpkt=MAX_NFPKT-idx+2)
            new_pkt = self.pkt_gen.get_existing_data_si()
            expected_pkt = self.pkt_gen.get_expected_coupled_mqtt()
            data = new_pkt['data_packet']
            si = new_pkt['si_packet']
            expected_pkt.update({'duplication': duplication, 'time_delay': DEFAULT_DELAY,
            'si_rawpacket': si, 'data_rawpacket': data})
            self.local_pkts.append(expected_pkt)
            self.ble_sim.send_data_si_pair(data, si, duplication, delay=DEFAULT_DELAY)
        time.sleep(5)

class OneBrgStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in DUPLICATIONS: #tqdm(duplications, desc='Duplications', position=1, leave=True):
            debug_print(f'Duplication {duplication}')
            for time_delay in TIME_DELAYS: #tqdm(time_delays, desc='Time Delays', position=2, leave=True):
                debug_print(f'Time Delay {time_delay}')
                if self.randomize:
                    new_pkt = self.pkt_gen.get_new_data_si()
                    data = new_pkt['data_packet']
                    si = new_pkt['si_packet']
                    expected_pkt = self.pkt_gen.get_expected_coupled_mqtt()
                    packet_error = self.packet_error._generate_packet_error(duplication)
                    expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                        'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data})
                    self.local_pkts.append(expected_pkt)
                else:
                    run_data = self.run_data.get_data(TEST_COUPLING, duplication, time_delay, BRIDGES[0])
                    data = run_data.data
                    si = run_data.si
                    packet_error = run_data.packet_error
                    self.local_pkts.append(run_data.expected_mqtt)
                self.ble_sim.send_data_si_pair(data, si, duplication, delay=time_delay, packet_error=packet_error)
        time.sleep(5)

class ThreeBrgInitStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.brg_network = BrgPktGeneratorNetwork()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        duplication = DUPLICATIONS[3]
        time_delay = TIME_DELAYS[2]
        if self.randomize:
            # Generate new random packet
            pkts = self.brg_network.get_scattered_pkt_pairs(time_delay)
            for brg_idx, pkt in enumerate(pkts):
                packet_error = self.packet_error._generate_packet_error(duplication)
                # Dump packets
                data = pkt['data_packet']
                pkt['data_packet'] = data
                si = pkt['si_packet']
                pkt['si_packet'] = si
                pkt['packet_error'] = packet_error
                bridge_id = pkt['bridge_id']
                scattered_time_delay = pkt['time_delay']
                # log the sent packet with relevant info from run
                expected_pkt = self.brg_network.brg_list[brg_idx].get_expected_coupled_mqtt()
                expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                                    'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data, 'brg_idx': brg_idx,
                                    'bridge_id': bridge_id, 'scattered_time_delay': scattered_time_delay})
                self.local_pkts.append(expected_pkt)
            self.ble_sim.send_brg_network_pkts(pkts, duplication)
        else:
            # Construct packet list from data
            pkts = []
            for brg_idx in BRIDGES:
                pkt = {}
                run_data = self.run_data.get_data(TEST_COUPLING, duplication, time_delay, brg_idx)
                pkt['data_packet'] = run_data.data
                pkt['si_packet'] = run_data.si
                pkt['time_delay'] = run_data.scattered_time_delay
                pkt['packet_error'] = run_data.packet_error
                pkt['bridge_id'] = run_data.bridge_id
                self.local_pkts.append(run_data.expected_mqtt)
                pkts.append(pkt)
            # Send scattered packets
            self.ble_sim.send_brg_network_pkts(pkts, duplication)
        time.sleep(5)
        


class ThreeBrgStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.brg_network = BrgPktGeneratorNetwork()

    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            # Time delays from 30 -> 255
            for time_delay in TIME_DELAYS[1:]:
                debug_print(f'Time Delay {time_delay}')
                if self.randomize:
                    # Generate new random packet
                    pkts = self.brg_network.get_scattered_pkt_pairs(time_delay)
                    for brg_idx, pkt in enumerate(pkts):
                        packet_error = self.packet_error._generate_packet_error(duplication)
                        # Dump packets
                        data = pkt['data_packet']
                        pkt['data_packet'] = data
                        si = pkt['si_packet']
                        pkt['si_packet'] = si
                        pkt['packet_error'] = packet_error
                        bridge_id = pkt['bridge_id']
                        scattered_time_delay = pkt['time_delay']
                        # log the sent packet with relevant info from run
                        expected_pkt = self.brg_network.brg_list[brg_idx].get_expected_coupled_mqtt()
                        expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                                            'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data, 'brg_idx': brg_idx,
                                            'bridge_id': bridge_id, 'scattered_time_delay': scattered_time_delay})
                        self.local_pkts.append(expected_pkt)
                    self.ble_sim.send_brg_network_pkts(pkts, duplication)
                else:
                    # Construct packet list from data
                    pkts = []
                    for brg_idx in BRIDGES:
                        pkt = {}
                        run_data = self.run_data.get_data(TEST_COUPLING, duplication, time_delay, brg_idx)
                        pkt['data_packet'] = run_data.data
                        pkt['si_packet'] = run_data.si
                        pkt['time_delay'] = run_data.scattered_time_delay
                        pkt['packet_error'] = run_data.packet_error
                        pkt['bridge_id'] = run_data.bridge_id
                        self.local_pkts.append(run_data.expected_mqtt)
                        pkts.append(pkt)
                    # Send scattered packets
                    self.ble_sim.send_brg_network_pkts(pkts, duplication)
        time.sleep(5)

class IncrementalStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = TagPktGenerator(adva=INCREMENTAL_STAGE_ADVA)
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for time_delay in INCREMENTAL_TIME_DELAYS:
            for pkt in INCREMENTAL_PACKETS:
                data = self.pkt_gen.get_packet()
                # expected_pkt = self.pkt_gen.get_expected_mqtt()
                # expected_pkt.update({'duplication': duplication, 'time_delay': DEFAULT_DELAY,
                # 'si_rawpacket': si, 'data_rawpacket': data})
                # self.local_pkts.append(expected_pkt)
                self.ble_sim.send_packet(raw_packet=data, duplicates=1, delay=time_delay)
                self.pkt_gen.set_pkt_id(self.pkt_gen.get_pkt_id() + 1)
        time.sleep(5)



# TEST CLASS

# STAGES = [IncrementalStage]
STAGES = [InitStage, OneBrgStage, ThreeBrgInitStage, ThreeBrgStage]
# STAGES = [InitStage]

class CouplingTest(GenericTest):
    def __init__(self, **kwargs):        
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        self.stages = [stage(**self.__dict__) for stage in STAGES]

    def enter_dev_mode(self):
        gw_type = self.edge.get_gateway_type(self.gw_id)
        if gw_type == GatewayType.MOBILE:
            debug_print('Android DevMode needs to be enabled manually! Choose HIVE env')
        else:
            self.edge.enter_dev_mode(self.gw_id, legacy=self.legacy)
        gw_info = self.mqttc.get_gw_info()
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        while datetime.datetime.now() < timeout:
            debug_print('Waiting to see GW in DevMode...')
            gw_seen = self.mqttc.userdata['gw_seen']
            if gw_seen is True or gw_info is not False:
                debug_print(f'GW {self.gw_id} In DevMode')
                return True
            time.sleep(10)
        raise CouplingTestError('Cannot enter GW DevMode!')
    
    def run(self):
        super().run()
        self.enter_dev_mode()
        self.test_pass = True
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            if stage.stage_pass == False:
                self.test_pass = False
        self.end_test()
        self.exit_dev_mode()
    
    def exit_dev_mode(self):
        self.mqttc.exit_dev_mode(legacy=self.legacy)
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        while datetime.datetime.now() < timeout:
            online_status = self.edge.check_gw_online([self.gw_id])
            if online_status is not False:
                debug_print(f'GW {self.gw_id} Out Of DevMode')
                return True
            time.sleep(10)
        raise CouplingTestError('Cannot exit GW DevMode!')

# TODO - make sure everything is running non-randomized
