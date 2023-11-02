from argparse import ArgumentParser
import time
from wiliot_deployment_tools.interface.ble_simulator import BLESimulator

def main():
    parser = ArgumentParser(prog='wlt-ble-sim',
                            description='BLE Simulator - CLI Tool to use GW BLE Simulator')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-p', type=str, help="port", required=True)
    required.add_argument('-c', type=str, help="channel", required=True)
    required.add_argument('-dup', type=str, help="duplicates", required=True)
    required.add_argument('-delay', type=str, help="delay", required=True)
    required.add_argument('-output', type=str, help="output power", required=True)
    required.add_argument('-packet', type=str, help="packet", required=True)
    required.add_argument('-ts', type=float, help="time stamp") 

    
    args = parser.parse_args()
    b = BLESimulator(args.p)
    b.set_sim_mode(True)
    b.trigger_by_time_stamp(args.ts)
    b.send_packet(args.packet, args.dup, args.output, args.c, args.delay)
    b.set_sim_mode(False)
    
def main_cli():
    main()


if __name__ == '__main__':
    main()
