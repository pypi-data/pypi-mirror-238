import pandas as pd
from wiliot_deployment_tools.interface.uart_if import UARTInterface
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.interface.if_defines import *
import time
import datetime
import threading
import binascii

class SnifferPkt():
    def __init__(self, raw_output, time_received, rx_channel):
        self.adva = raw_output[:12]
        self.packet = raw_output[12:74]
        self.rssi = int.from_bytes(binascii.unhexlify(raw_output[74:]), 'big') * -1
        self.time_received = time_received
        self.rx_channel = rx_channel
    
    def __repr__(self):
        return f'CH{self.rx_channel}|{self.adva}{self.packet} RSSI:{self.rssi} {self.time_received}'
    
    def to_dict(self):
        return {'adva': self.adva, 'packet': self.packet, 'rssi': self.rssi, 'time_received': self.time_received, 'rx_channel': self.rx_channel}

class SnifferPkts():
    def __init__(self, pkts=[]):
        self.pkts = pkts
    
    def __add__(self, other):
        return SnifferPkts(self.pkts + other.pkts)
        
    def __len__(self):
        return len(self.pkts)
    
    def __repr__(self):
        return self.pkts
    
    def process_pkt(self, raw_output, time_received, rx_channel, print_pkt=False):
        pkt = SnifferPkt(raw_output, time_received, rx_channel)
        self.pkts.append(pkt)
        if print_pkt:
            print(pkt)
        
    def filter_pkts(self, raw_packet=None, adva=None, time_range:tuple=None):
        result = []
        for pkt in self.pkts:
            if (raw_packet is not None) and (pkt.packet == raw_packet) or \
                (adva is not None) and (pkt.adva == adva) or \
                (time_range is not None) and (time_range[0] < pkt.time_received < time_range[1]):
                result.append(pkt)
        return SnifferPkts(result)
    
    def flush_pkts(self):
        self.pkts = []
        
    def to_list(self):
        return [p.to_dict() for p in self.pkts]
    
    def to_pandas(self):
        return pd.DataFrame().from_dict(self.to_list())

class BLESniffer():
    def __init__(self, uart:UARTInterface, print_pkt=False):
        self.uart = uart
        self.listener_thread = None
        self.sniffer_pkts = SnifferPkts()
        self.listening = False
        self.listener_lock = threading.Lock()
        self.print = print_pkt
        self.rx_channel = 0

    def packet_listener(self):
        while self.listening:
            line = self.uart.read_line()
            if line is not None and len(line) == 76:
                with self.listener_lock:
                    self.sniffer_pkts.process_pkt(line, datetime.datetime.now(), self.rx_channel, self.print)
    
    # Change sniffing modes
    def start_sniffer(self, rx_channel):
        self.uart.set_sniffer(rx_channel)
        self.rx_channel = rx_channel
        self.listener_thread = threading.Thread(target=self.packet_listener)
        self.listening = True
        self.listener_thread.start()
        
    def stop_sniffer(self):
        self.flush_pkts()
        self.listening = False
        if self.listener_thread is not None:
            self.listener_thread.join()
            self.listener_thread = None
            self.uart.cancel_sniffer()
    
    def reset_sniffer(self, rx_channel):
        self.stop_sniffer()
        self.start_sniffer(rx_channel)
        self.flush_pkts()
        
    # Data Handling
    def get_all_pkts(self):
        return self.sniffer_pkts
    
    def get_filtered_packets(self, raw_packet=None, adva=None, time_range:tuple=None):
        return self.sniffer_pkts.filter_pkts(raw_packet, adva, time_range)
    
    def flush_pkts(self):
        self.sniffer_pkts.flush_pkts()
        
    def to_pandas(self):
        return self.sniffer_pkts.to_pandas()

class BLESnifferContext():
    def __init__(self, ble_sniffer:BLESniffer, rx_channel):
        self.ble_sniffer = ble_sniffer
        self.rx_channel = rx_channel

    def __enter__(self):
        self.ble_sniffer.flush_pkts()
        self.ble_sniffer.start_sniffer(self.rx_channel)
        return self.ble_sniffer

    def __exit__(self, exc_type, exc_value, traceback):
        if self.ble_sniffer:
            self.ble_sniffer.stop_sniffer()