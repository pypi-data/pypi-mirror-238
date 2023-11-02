import datetime
import sys
import time
from wiliot_deployment_tools.api.extended_api import BridgeThroughGatewayAction, ExtendedEdgeClient, GatewayType,ExtendedPlatformClient,EXCEPTIONS_TO_CATCH,BoardTypes
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.common.utils_defines import  SEC_TO_SEND,BROADCAST_DST_MAC


class GwHbActionClientError(Exception):
    pass
  
       
class GwHbActionClient(ExtendedEdgeClient):

    def __init__(self, edge_api_key, asset_api_key, owner,env='prod'):
        # Initialize objects
        self.edge = ExtendedEdgeClient(edge_api_key, owner, env)
        self.plat = ExtendedPlatformClient(asset_api_key, owner, env)


    def get_relevant_bridges(self, gateway_id):
        """
        Returns seen bridges by gateway that are associated to owner and have ble version with gw heat beat support
        :type gateway_id: str
        :param gateway_id: gateway ID
        :rtype: list
        :return: list of relevant bridge IDs
        """
        bridges = self.edge.get_seen_bridges(gateway_id)
        relevant_bridges = bridges
        for bridge in bridges:
            brg_ble = self.edge.get_brg_ble_version(bridge)
            if not self.check_ble_gw_hb_support(brg_ble):
                # debug_print(f'Bridge {bridge} does not support gw heat beat!')
                relevant_bridges.remove(bridge)
        return relevant_bridges


    @staticmethod
    def check_ble_gw_hb_support(ble_ver):
        """
        checks if gw_hb management is supported for BLE version
        :rtype: bool
        :return: True if supported, False otherwise
        """
        ble_ver = ble_ver.split('.')
        if not ((int(ble_ver[0]) > 3) or
                (int(ble_ver[0]) > 2 and int(ble_ver[1]) > 15) or \
                (int(ble_ver[0]) > 2 and int(ble_ver[1]) > 14 and int(ble_ver[2]) > 28)):
            return False
        else:
            return True


    def send_gw_hb_pkt(self, gateway_id,payload,silent=False, seconds_to_send=1):
        """
        send gw heat beat packet to bridge
        :type bridge_id: str
        :param bridge_id: Bridge ID
        :type packet: GwHbActionClientPacket
        :param packet: packet to send to bridge
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type silent: bool
        :param silent: print gw heat beat packet parameters
        :type seconds_to_send: int
        :param seconds_to_send: seconds to repeat packet
        :rtype: bool
        :return: True if sent, False otherwise
        """
        
        bridge_id = BROADCAST_DST_MAC
        via_gw = gateway_id
        reps = 8
        ms_to_send = 1200
        seconds_to_send = datetime.timedelta(seconds=seconds_to_send)
        # Check BRG Compatability
        brg_version = None
        # Check GW Compatability
        gw_type = self.edge.get_gateway_type(via_gw)
        if gw_type == GatewayType.WIFI:
            gw_version = self.edge.get_gw_ble_version(via_gw)
            rxtx = datetime.timedelta(milliseconds=
                                    self.edge.get_gateway(via_gw)['reportedConf']['additional']['rxTxPeriodMs'])
            reps = seconds_to_send // rxtx + 1
            if not silent:
                debug_print(f'Sending packet through WIFI GW {via_gw}')
        if gw_type == GatewayType.MOBILE:
            if not silent:
                debug_print(f'Sending packet through ANDROID GW {via_gw}')
            ms_to_send = int(seconds_to_send.total_seconds()*1000)
        try:
            res = self.edge.send_bridge_action_through_gw(gateway_id,
                                                 BridgeThroughGatewayAction.GW_HB,
                                                 payload, bridge_id, reps=reps)
        except EXCEPTIONS_TO_CATCH as e:
            debug_print('Exception caught when sending gw hb packet!')
            debug_print(e)
            return False
        return res

    
    def check_gw_hb_ack_received(self, gateway_id,payload, time_sent):
        """
        check if gw heat beat packet was received by bridge
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type payload: str
        :param payload containing gw_id
        :type time_sent: datetime
        :param time_sent: time packet was sent
        :rtype dict
        :return: dictionary with brg_id as key, rssi as value
        """
        hours_back = (datetime.datetime.now() - time_sent + datetime.timedelta(seconds=5)).total_seconds() / 3600
        acks = self.edge.get_acks(gateway_id, hours_back)
        rssi_dict = {}
        if acks is None:
            return None
        ack_ready = False
        for line in range(len(acks)):
            ack_payload  = acks['payload'].iloc[line]
            ack_gw_id = ack_payload[0:11]
            if  ack_gw_id == payload[:12] and acks['actionType'].iloc[line] == BridgeThroughGatewayAction.GW_HB:
                ack_ready = True
                brg_mac = acks['bridgeId'].iloc[line]
                rssi = int(ack_payload[12:14], 16)
                if brg_mac in rssi_dict:
                    # update rssi to max vaule received
                    if rssi > rssi_dict[brg_mac]:
                        rssi_dict[brg_mac] = rssi 
                else:
                    rssi_dict[brg_mac] = rssi  
        if ack_ready:
            return rssi_dict
        return None
   

    def send_gw_hb_packet_to_brgs_list(self,bridges,gateways,minutes_timeout=3,rssi_th = 76,brg_gw_dict = None,is_bridge_log = False):
        """
        send gw hb from all gateways and remove bridgese with good rssi
        :type bridges: list
        :param bridges: Bridges IDs list
        :type gateways: list
        :param gateways: Gateways IDs list
        :type minutes_timeout: int
        :param minutes_timeout: timeout
        :type rssi_th int
        :param rssi value threshold for OTA
        :return: List of bridges with low connection
        """
        gws_dict = {}
        gws_rssi_dict = {} #for bridge log option
        time_sent = datetime.datetime.now()
        for gw in gateways:
            payload = gw[2:13] 
            gws_dict[gw] = payload
        debug_print(f'Broadcasting GW HB throgh gws: {gateways} | Max Waiting time {minutes_timeout} minutes')
        # broadcast gw_hb through all gateways
        for gw in gateways:
            self.send_gw_hb_pkt(gw,gws_dict[gw], silent=False, seconds_to_send=SEC_TO_SEND)
        time_gw_stops = time_sent + datetime.timedelta(seconds=SEC_TO_SEND)
        time_end = time_sent + datetime.timedelta(minutes=minutes_timeout)
        curr_time = time_sent
        while curr_time < time_end and bridges != []:
            curr_time = datetime.datetime.now()
            if curr_time > time_gw_stops - datetime.timedelta(seconds=1):  # 1 second buffer
                # broadcast gw_hb through all gateways
                for gw in gateways:
                    self.send_gw_hb_pkt(gw,gws_dict[gw], silent=False, seconds_to_send=SEC_TO_SEND)
                time_gw_stops = datetime.datetime.now() + datetime.timedelta(seconds=SEC_TO_SEND)
            time.sleep(0.5)
            for gw in gateways:
                # check for acks of all gws
                rssi_dict = self.check_gw_hb_ack_received(gw,gws_dict[gw], time_sent)
                if rssi_dict: # key: brg value: rssi
                    if is_bridge_log:
                                gws_rssi_dict[gw] = rssi_dict[bridges[0]]
                                gateways.remove(gw)
                                continue
                    for brg_id in bridges:
                        if brg_id in rssi_dict and brg_id in brg_gw_dict and gw in brg_gw_dict[brg_id]:
                            gw_info = brg_gw_dict[brg_id][gw] # gws dict
                            # gw_info = gws_dict_for_brg[gw]
                            if rssi_dict[brg_id] > gw_info[1]: # update min rssi
                                gw_info[1] = rssi_dict[brg_id]
                            if gw_info[0] > 1 and curr_time < time_end: #check msg cnt
                                # in case of timeout, take current min rssi value
                                gw_info[0] = gw_info[0] - 1
                                continue
                            else: #check rssi th                                      
                                if gw_info[1] <= rssi_th and not is_bridge_log:
                                    # remove bridges with good connection 
                                    debug_print(f'got good connection for bridge:{brg_id} with rssi:{gw_info[1]}')
                                    bridges.remove(brg_id)
                                    if bridges != []:
                                        debug_print(f'continue to next bridges:{bridges}')
            if not gateways and is_bridge_log:
                return gws_rssi_dict
        return bridges
        
        

   
    def check_bridges_for_gw_hb_action(self,bridges):
        if not bridges:
            return None
        for bridge in bridges:
            try:
                brg_version = self.edge.get_brg_ble_version(bridge)
            except Exception as e:
                if "not owned" in str(e):
                    bridges.remove(bridge)
                    debug_print(f"Warning!! bridge {bridge} is not owned")
                    continue
            brg_status = self.edge.get_bridge_status(bridge)
            if brg_status == 'offline':
                bridges.remove(bridge)
                debug_print(f"Warning: bridge {bridge} is offline.")
                continue
            if not self.check_ble_gw_hb_support(brg_version):
                bridges.remove(bridge)
                debug_print(f"Warning: bridge {bridge} version doesn't support the check. Please update version.")
        return bridges

    def create_brg_gw_cnt_dict(self, bridges):
        '''
        create a dictionary, with brg_id as key
        value: a dictionary of gateways seeing this bridge (as a key)
        value: a list of counter and min rssi
        example for dictionary:
        brg_gw_cnt_dict[brg_x] -> gws_cnt_dict[gw] = [10,0]

        '''
        minew_rssi_msgs_cnt = 10  # count rssi packets before checking threshold
        bridge_rssi_msgs_cnt = 1
        min_rssi = 0
        brg_gw_cnt_dict = {}
        for brg in bridges:
            gws_of_brg = list(self.edge.get_gateways_from_bridges(brg))
            gws_cnt_dict = {}
            for gw in gws_of_brg:
                if self.edge.check_gw_compatible_for_action(gw):
                    if self.edge.get_bridge_board(brg) == BoardTypes.MINEW_DUAL.value:
                        gws_cnt_dict[gw] = [minew_rssi_msgs_cnt,min_rssi]
                    else:
                        gws_cnt_dict[gw] = [bridge_rssi_msgs_cnt,min_rssi]
            #add new tuple to current bridge list
            brg_gw_cnt_dict[brg] = gws_cnt_dict
        return brg_gw_cnt_dict

    def bridge_gw_downlink_analyzer(self, location, minutes_timeout=3,bridges_list = None,gws_list = None,is_bridge_log = False):
        """
        Get check rssi for OTA of all bridges by a given location
        :type location: str
        :param location: Location to check (ass written in platform)
        :type packet: PowerManagementPacket
        :param packet: packet to send
        :type minutes_timeout: int
        :param minutes_timeout: timeout
        :rtype: dict
        :return: dict of {bridgeID: ack status (bool)} pairs
        """
        rssi_th = 76
        bridges = []
        gateways = []
        # get all bridges in the given location/from cmd
        if bridges_list:
            bridges = bridges_list
            debug_print('got bridges list from cmd')
        elif location:
            debug_print(f'Getting bridges from {location}')
            bridges = self.plat.get_location_bridges(location)
        elif gws_list:
            debug_print(f'Getting bridges from given gateways')
            for gw in gws_list:
                gw_brgs = self.get_relevant_bridges(gw)
                for brg in gw_brgs:
                    if brg not in bridges:
                        bridges.append(brg)
        else:
            debug_print('Error!: must suplly Location, bridges or getways')
            return False   
                     
        bridges = self.check_bridges_for_gw_hb_action(bridges)

        if not bridges:
            debug_print('Error: no bridges found for analyzer tool')
            return False
        
        # get all gw that see thoes bridges
        if gws_list is not None:
            gateways = gws_list
            debug_print('got gateways list from cmd')
        else:
             for bridge in bridges:
                gws_of_brg = list(self.edge.get_gateways_from_bridges(bridge))
                for gw in gws_of_brg:
                    if gw not in gateways:
                        gateways.append(gw)
        for gw in gateways:
            if not self.edge.check_gw_compatible_for_action(gw):
                debug_print(f'Warning! gateway {gw} does not support Action!')
                gateways.remove(gw)
        if not gateways:
            debug_print('Error! no any valid gateways for check!')
            return False
        # in case of minew dual band bridge for each bridge,each gw
        #  holds a counter of rssi packet received to make sure receiving rssi of both antenas
        brg_gw_dict = self.create_brg_gw_cnt_dict(bridges)
        res = self.send_gw_hb_packet_to_brgs_list(bridges = bridges,minutes_timeout=minutes_timeout
                                                                      ,gateways=gateways,rssi_th=rssi_th,brg_gw_dict=brg_gw_dict,is_bridge_log=is_bridge_log)
        if not is_bridge_log:
            unconnected_bridges = res
            if unconnected_bridges:
                debug_print(f'Not all bridges have stable connection, check following bridge:{unconnected_bridges}')
                return False
            else:
                debug_print('Success! All bridges have stable downlink')
                return True
        else:
            gws_rssi_list = res
            debug_print(f'Printing bridge rssi log for bridge:{bridges_list}')
            for gateway, rssi in gws_rssi_list.items():
                debug_print(f"gateway: {gateway} with rssi {rssi}")
