import datetime
import json
import os
import time
import pandas as pd
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from wiliot_api.api_client import WiliotCloudError
from wiliot_deployment_tools.ag.ut_defines import TX_MAX_RETRIES
from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.interface.ble_sniffer import BLESniffer, BLESnifferContext
from wiliot_deployment_tools.interface.if_defines import DEFAULT_DELAY, SEP, RX_CHANNELS
from wiliot_deployment_tools.gw_certificate.tests.static.downlink_defines import LEGACY_TX_MAX_RETRIES, RETRIES, TX_MAX_DURATIONS
from wiliot_deployment_tools.interface.pkt_generator import BrgPktGenerator
from wiliot_deployment_tools.gw_certificate.tests.generic import PASS_STATUS, GenericTest, GenericStage

class GenericDownlinkStage(GenericStage):
    def __init__(self, sniffer:BLESniffer, edge:ExtendedEdgeClient, stage_name, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(stage_name=stage_name, **self.__dict__)        
        
        #Clients
        self.sniffer = sniffer
        self.edge = edge
        
        #Stage Params
        self.all_pkts = pd.DataFrame()
        
    def prepare_stage(self):
        super().prepare_stage()
        self.sniffer.flush_pkts()
    
    def generate_stage_report(self):
        self.all_pkts.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        return self.report
        
class InitStage(GenericDownlinkStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator()

    def graph_channel_measurements(self, channel, measurements):
        array = np.array(measurements)
        res = scipy.stats.linregress(array)
        plt.clf()
        plt.cla()
        plt.plot(array[:, 0], array[:, 1], 'o', label='original data')
        plt.plot(array[:, 0], res.intercept + res.slope*array[:, 0], 'r', label=f'fitted line; R={res.rvalue}')
        plt.legend()
        # TODO - Plotly
        # Todo - Labels for axis
        # TODO - write why test failed
        # TODO - Geolocation
        # TODO - Light version
        png_path = os.path.join(self.test_dir, f'{self.stage_name}_{channel}.png')
        plt.savefig(png_path)
        # Deteremine Pass/Fail
        channel_pass = True
        if self.legacy:
            if not ((res.rvalue > 0.8) and (0.9 < res.slope < 1.1)):
                channel_pass = False
        else:
            if not ((res.rvalue > 0.8) and (res.slope > 0)):
                channel_pass = False
        if not channel_pass:
            self.add_to_stage_report(f"Channel {channel}: FAIL!")
            self.stage_pass = False
        else:
            self.add_to_stage_report(f"**Channel {channel}: PASS!")
        # Generate report
        self.add_to_stage_report(f"- Total {len(array[:, 0])} MQTT Payloads sent")
        self.add_to_stage_report(f"- Total {sum(array[:, 1])} BLE Packets received by sniffer")
        self.add_to_stage_report(f"- R Value: {res.rvalue} | Slope: {res.slope}")
        self.add_to_stage_report(f"- Graph saved at {png_path}")

    def run(self):
        def run_tx_max_duration():
            sent_pkts = []
            for tx_max_duration in TX_MAX_DURATIONS:
                debug_print(f'Tx Max Duration {tx_max_duration}')
                for retry in RETRIES:
                    self.pkt_gen.increment_brg_seq_id()
                    self.pkt_gen.increment_hb_counters()
                    brg_hb = self.pkt_gen.get_brg_hb()
                    sent_payload = self.edge.send_packet_through_gw(self.gw_id, raw_packet=brg_hb, debug=True, return_payload=True, tx_max_duration=tx_max_duration)
                    sent_payload = json.dumps(sent_payload)
                    sent_pkts.append({'tx_max_duration': tx_max_duration, 'retry': retry, 'pkt': brg_hb[12:],
                                        'payload': sent_payload, 'time_sent': datetime.datetime.now()})
                    time.sleep(tx_max_duration/1000)
            return sent_pkts
        
        def run_tx_max_retries():
            sent_pkts = []
            for tx_max_retries in LEGACY_TX_MAX_RETRIES:
                debug_print(f'Tx Max Retries {tx_max_retries}')
                for retry in RETRIES:
                    self.pkt_gen.increment_brg_seq_id()
                    self.pkt_gen.increment_hb_counters()
                    brg_hb = self.pkt_gen.get_brg_hb()
                    sent_payload = self.edge.send_packet_through_gw(self.gw_id, raw_packet=brg_hb, debug=True, return_payload=True, repetitions=tx_max_retries)
                    sent_payload = json.dumps(sent_payload)
                    sent_pkts.append({'tx_max_retries': tx_max_retries, 'retry': retry, 'pkt': brg_hb[12:],
                                        'payload': sent_payload, 'time_sent': datetime.datetime.now()})
                    time.sleep(0.255)
            return sent_pkts
        
        self.start_time = datetime.datetime.now()
        now = datetime.datetime.now()
        self.stage_pass = True
        pkts_received_by_channel_dict = {}
        for channel in RX_CHANNELS:
            debug_print(f'RX Channel {channel}')
            pkts_received_by_channel = []
            self.pkt_gen.set_random_bridge_id()
            with BLESnifferContext(self.sniffer, channel) as sniffer:
                # Send the packets
                run_test = run_tx_max_retries if self.legacy else run_tx_max_duration
                sent_pkts = run_test()
                # Process sniffed packets
                time.sleep(10)
                for pkt in sent_pkts:
                    # Get vars from dict
                    raw_packet = pkt['pkt']
                    payload = pkt['payload']
                    tx_max_duration = pkt['tx_max_duration'] if not self.legacy else pkt['tx_max_retries']
                    retry = pkt['retry']
                    time_sent = pkt['time_sent']
                    # Get packets from sniffer
                    sniffed_pkts = sniffer.get_filtered_packets(raw_packet=raw_packet)
                    pkts_received_by_channel.append((tx_max_duration, len(sniffed_pkts)))
                    pkt_df = sniffed_pkts.to_pandas()
                    # Add variables to dataframe
                    if self.legacy:
                        pkt_df['tx_max_retries'] = tx_max_duration
                    else:
                        pkt_df['tx_max_duration'] = tx_max_duration
                    pkt_df['mqtt_payload'] = payload
                    pkt_df['retry'] = retry
                    pkt_df['time_sent'] = time_sent
                    if self.legacy:
                        debug_print(f'Retry {pkt["retry"]} | TxMaxRetries {tx_max_duration} | {len(sniffed_pkts)} pkts received')
                    else:
                        debug_print(f'Retry {pkt["retry"]} | TxMaxDuration {tx_max_duration} | {len(sniffed_pkts)} pkts received')
                    self.all_pkts = pd.concat([self.all_pkts, pkt_df])
            pkts_received_by_channel_dict[channel] = pkts_received_by_channel
            self.graph_channel_measurements(channel, pkts_received_by_channel)
"""
for each rx channel:
    for each tx max duration (100->2000):
        10 times - avg of num packets got
            check that 
+ ADD consecutive TX packet check
"""
    
STAGES = [InitStage]

class DownlinkTest(GenericTest):
    def __init__(self, **kwargs):        
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        self.stages = [stage(**self.__dict__) for stage in STAGES]
    
    def run(self):
        super().run()
        self.test_pass = True
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            if stage.stage_pass == False:
                self.test_pass = False
        self.end_test()