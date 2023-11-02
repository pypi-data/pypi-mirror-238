from wiliot_deployment_tools.connectivity_analyzer.connectivity_analyzer import GwHbActionClient
from wiliot_core import check_user_config_is_ok
from wiliot_deployment_tools.common.utils_defines import *
from argparse import ArgumentParser
import sys
import bitstruct


def main():
    # parser
    parser = ArgumentParser(prog='wlt-connectivity-analyzer',
                            usage='%(prog)s -o OwnerID -brg BridgeID (-t) [mode]',
                            description='CLI Tool for using Wiliot Bridge calibration management functionality')
    parser.add_argument('-owner', type=str, help="Owner ID", required=True)
    parser.add_argument('-t', action='store_true',
                        help='if flag used, use test environment (prod is used by default)')
    parser.add_argument('-gws', nargs='+', type=str, help="gateways id list to check connectivity", required=False)
    parser.add_argument('-brgs', nargs='+', type=str, help="bridges id list to check connectivity", required=False)
    parser.add_argument('-location', type=str, help="Location/Zone to search bridges", required=False)
    parser.add_argument('-bridge_log', action='store_true', help="print all rssi from all seen gw for a given bridge", required=False)
    parser.add_argument('-m', type=int, help="Minutes timeout (not required, defaults to 5 minutes)", required=False, default=5)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args, unknown = parser.parse_known_args()
    if not args.location and not args.gws and not args.brgs:
        print('Error: must insert location, bridges list or gateways list')
        return False
    if (args.location and args.gws) or (args.location and args.brgs) or (args.brgs and args.gws):
        print('Error: too many arguments, Choose: Location, bridges or gateways')
        return False
    if args.t:
        env = 'test'
    else:
        env = 'prod'
    owner_id = args.owner
    conf_env = env if env == 'prod' else 'non-prod'

    if args.bridge_log:
        bridge_log = True
    else:
        bridge_log = False

    user_config_file_path, asset_api_key, is_success = check_user_config_is_ok(owner_id, conf_env, 'asset')
    if is_success:
        print('Asset Management credentials saved/upload from {}'.format(user_config_file_path))
    else:
        raise Exception('invalid Asset Management credentials - please try again to login')
    user_config_file_path, edge_api_key, is_success = check_user_config_is_ok(owner_id, conf_env, 'edge')
    if is_success:
        print('Edge Management credentials saved/upload from {}'.format(user_config_file_path))
    else:
        raise Exception('invalid Edge Management credentials - please try again to login')

    
    client = GwHbActionClient(edge_api_key,asset_api_key, owner_id, env)
    client.bridge_gw_downlink_analyzer(location=args.location, minutes_timeout=args.m,
                                       bridges_list=args.brgs,gws_list = args.gws,is_bridge_log = bridge_log)


def main_cli():
    main()
if __name__ == '__main__':
    main()
