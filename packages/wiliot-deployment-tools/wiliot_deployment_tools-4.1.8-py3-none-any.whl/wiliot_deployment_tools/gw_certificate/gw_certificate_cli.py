from argparse import ArgumentParser
from wiliot_core import check_user_config_is_ok

from wiliot_deployment_tools.gw_certificate.gw_certificate import GWCertificate

def main():
    parser = ArgumentParser(prog='wlt-gw-certificate',
                            description='Gateway Certificate - CLI Tool to test Wiliot GWs')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-owner', type=str, help="Owner ID", required=True)
    required.add_argument('-gw', type=str, help="Gateway ID", required=True)
    parser.add_argument('-test', action='store_true',
                    help='If flag used, use test environment (prod is used by default)')
    parser.add_argument('-random', action='store_true', help='randomize packets payload sent')
    parser.add_argument('-legacy', action='store_true', help='use legacy DevMode')
    parser.add_argument('-gcp', action='store_true', help='use GCP Cloud')
    
    args = parser.parse_args()
    if args.test:
        env = 'test'
    else:
        env = 'prod'

    if args.gcp:
        cloud = 'gcp'
    else:
        cloud = 'aws'
    
    owner_id = args.owner
    conf_env = env if env == 'prod' else 'non-prod'
    user_config_file_path, api_key, is_success = check_user_config_is_ok(owner_id, conf_env, 'edge')
    if is_success:
        print('credentials saved/upload from {}'.format(user_config_file_path))
    else:
        raise Exception('invalid credentials - please try again to login')


    gwc = GWCertificate(gw_id=args.gw, api_key=api_key, owner_id=args.owner, env=env, cloud=cloud,
                        random=args.random, legacy=args.legacy)
    gwc.run_tests()
    
def main_cli():
    main()

if __name__ == '__main__':
    main()
