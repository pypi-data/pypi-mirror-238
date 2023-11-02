from argparse import ArgumentParser
import time
from wiliot_deployment_tools.interface.ble_sniffer import BLESniffer
from wiliot_deployment_tools.interface.uart_if import UARTInterface

def main():
    parser = ArgumentParser(prog='wlt-sniffer',
                            description='BLE Sniffer - CLI Tool to Sniff BLE Packets')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-p', type=str, help="port", required=True)
    required.add_argument('-c', type=int, help="channel", required=True, choices=[37, 38, 39])

    
    args = parser.parse_args()
    uart = UARTInterface(args.p, update_fw=True)
    sniffer = BLESniffer(uart, print_pkt=True)
    sniffer.start_sniffer(args.c)
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            sniffer.stop_sniffer()
            break
        
def main_cli():
    main()


if __name__ == '__main__':
    main()
