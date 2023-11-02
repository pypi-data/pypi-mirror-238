import copy
import datetime
from enum import Enum
import json
import logging
import time
import paho.mqtt.client as mqtt
import ssl
from wiliot_deployment_tools.ag.ut_defines import PACKETS, PAYLOAD, MGMT_PKT, SIDE_INFO_PKT, GW_ID, NFPKT
from wiliot_deployment_tools.ag.wlt_types_ag import GROUP_ID_BRG2GW, GROUP_ID_SIDE_INFO
from wiliot_deployment_tools.ag.wlt_types_data import DATA_DEFAULT_GROUP_ID, DataPacket
from wiliot_deployment_tools.common.debug import debug_print

#TODO - implement logging

DATA_PKT = 'data_pkt'

class GwAction(Enum):
    DISABLE_DEV_MODE = "DevModeDisable"
    REBOOT_GW ="rebootGw"
    GET_GW_INFO ="getGwInfo"

class WltMqttPkt:
    def __init__(self, body, topic):
        self.body = body
        self.mqtt_topic = topic
        self.mqtt_timestamp = datetime.datetime.now()
        self.body_ex = {}
        if "data" in self.mqtt_topic:
            self.body_ex = copy.deepcopy(body)
            for pkt in self.body_ex[PACKETS]:
                data_pkt = DataPacket()
                data_pkt.set(pkt[PAYLOAD])
                if data_pkt.pkt != None:
                    if data_pkt.hdr.group_id == GROUP_ID_BRG2GW:
                        pkt[MGMT_PKT] = copy.deepcopy(data_pkt)
                if data_pkt.hdr.group_id == GROUP_ID_SIDE_INFO:
                    pkt[SIDE_INFO_PKT] = copy.deepcopy(data_pkt)
                if data_pkt.hdr.group_id == DATA_DEFAULT_GROUP_ID:
                    pkt[DATA_PKT] = copy.deepcopy(data_pkt)
                    pass

    def __repr__(self) -> str:
        if self.body_ex != {}:
            return str(self.body_ex)
        return str(self.body)


class WltMqttPkts:
    def __init__(self):
        self.data = []
        self.status = []
        self.update = []
        self.all = []

    def insert(self, pkt):
        self.all.append(pkt)
        if "data" in pkt.mqtt_topic:
            self.data.append(pkt)
        elif "status" in pkt.mqtt_topic:
            self.status.append(pkt)
        elif "update" in pkt.mqtt_topic:
            self.update.append(pkt)
            
    def __repr__(self) -> str:
        return f'Data {self.data} \n Status {self.status} \n Update {self.update}'
            
class MqttClient:

    def __init__(self, gw_id, owner_id, logger_filepath):
        # Set variables
        self.gw_id = gw_id
        self.owner_id = owner_id
        
        # Configure logger
        logger = logging.getLogger('mqtt')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(logger_filepath)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        self.logger = logger
        debug_print(f'MQTT Logger initialized at {logger_filepath}')
        
        # Configure Paho MQTT Client
        client_id = '{}-republish'.format('gw_id')
        self.userdata = {'packets': WltMqttPkts(), 'gw_seen': False , 'logger': self.logger
            }
        self.client = mqtt.Client(client_id, userdata=self.userdata)
        self.client.on_message = on_message
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_subscribe = on_subscribe
        self.client.on_unsubscribe = on_unsubscribe
        self.client.on_log = on_log
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.connect("broker.hivemq.com", port=8883, keepalive=60)
        # Set Topics
        self.update_topic = f"update-test/{owner_id}/{gw_id}"
        self.client.subscribe(self.update_topic)
        self.data_topic = f"data-test/{owner_id}/{gw_id}"
        self.client.subscribe(self.data_topic)
        self.status_topic = f"status-test/{owner_id}/{gw_id}"
        self.client.subscribe(self.status_topic)
        time.sleep(2)    
        self.client.loop_start()
    
    # Downstream Interface
    def send_action(self, action:GwAction):
        assert isinstance(action, GwAction), 'Action Must be a GWAction!'
        self.client.publish(self.update_topic, payload=json.dumps({"action": action.value}))
    
    def get_gw_info(self):
        self.flash_pkts()
        self.send_action(GwAction.GET_GW_INFO)
        time.sleep(5)
        debug_print('---GW INFO---')
        try:
            gw_info = self.userdata['packets'].status[0]
            debug_print(gw_info)
            self.flash_pkts()
            return gw_info
        except IndexError:
            debug_print('No GW INFO')
            self.flash_pkts()
            return False
        
    def get_gw_configuration(self):
        self.flash_pkts()
        self.send_action(GwAction.REBOOT_GW)
        debug_print('---GW CONFIG---')
        try:
            debug_print(self.userdata['packets'].status)
            return True
        except KeyError:
            return False
            
    def exit_dev_mode(self, legacy=False):
        if legacy:
            return self.send_action(GwAction.DISABLE_DEV_MODE)
        dev_mode = {
                "custom-mqtt": False,
                "broker_url": "broker.hivemq.com",
                "port": 8883,
                "username": "",
                "password": "",
                "update-topic": f"update/{self.owner_id}/{self.gw_id}",
                "status-topic": f"status/{self.owner_id}/{self.gw_id}",
                "data-topic": f"data/{self.owner_id}/{self.gw_id}"
                }
        return self.client.publish(self.update_topic, payload=json.dumps(dev_mode))
    
    # Packet Handling
    def flash_pkts(self):
        self.userdata = {'packets': WltMqttPkts(), 'gw_seen': False , 'logger': self.logger
            }
        self.client.user_data_set(self.userdata)

    def get_all_pkts_from_topic(self, topic):
        assert (topic in ['status', 'data', 'update']), 'Invalid Topic'
        pkts = []
        for p in eval(f'self.userdata["packets"].{topic}'):
            gw_id = p.body_ex[GW_ID] if GW_ID in p.body_ex else ""
            if PACKETS in p.body_ex:
                for pkt in p.body_ex[PACKETS]:
                    pkt[GW_ID] = gw_id
                    pkts += [pkt]
        return pkts
    
    def get_coupled_tags_pkts(self):
        return [p for p in self.get_all_pkts_from_topic('data') if NFPKT in p]


# MQTT Client callbacks

def on_connect(mqttc, userdata, flags, rc):
    rc_dict = {0: 'MQTT: Connection successful',
               1: 'MQTT: Connection refused - incorrect protocol version',
               2: 'MQTT: Connection refused - invalid client identifier',
               3: 'MQTT: Connection refused - server unavailable',
               4: 'MQTT: Connection refused - bad username or password',
               5: 'MQTT: Connection refused - not authorised'}
    try:
        message = rc_dict[rc]
    except KeyError:
        message = f'MQTT: Cannot connect, RC:{rc}'
    userdata['logger'].info(message)


def on_disconnect(mqttc, userdata, rc):
    if rc != 0:
        userdata['logger'].info(f"MQTT: Unexpected disconnection. {rc}")
    else:
        userdata['logger'].info('MQTT: Disconnect')


def on_subscribe(mqttc, userdata, mid, granted_qos):
    userdata['logger'].info(f"MQTT: Subscribe, MessageID {mid}, QoS {granted_qos}")


def on_unsubscribe(mqttc, userdata, mid):
    userdata['logger'].info(f"MQTT: Unsubscribe, MessageID {mid}")

def on_message(mqttc, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    userdata['packets'].insert(WltMqttPkt(data, message.topic))
    userdata['logger'].debug(f'{message.topic}: {data}')
    if(userdata['gw_seen'] is False):
        userdata['gw_seen'] = True
    
def on_log(client, userdata, level, buf):
    # MQTT_LOG_INFO = 0x01
    # MQTT_LOG_NOTICE = 0x02
    # MQTT_LOG_WARNING = 0x04
    # MQTT_LOG_ERR = 0x08
    # MQTT_LOG_DEBUG = 0x10
    if (level < mqtt.MQTT_LOG_DEBUG):
        userdata['logger'].info(f"mqtt_log: level={level}, msg={buf}")