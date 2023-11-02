import bitstruct
import binascii

# This is auto generated file! Don't edit this file manually!!!

GROUP_ID_SIDE_INFO_SENSOR = 0xEB
GROUP_ID_SIDE_INFO = 0xEC
GROUP_ID_GW2BRG = 0xED
GROUP_ID_BRG2GW = 0xEE

SENSOR_ACTION_IGNORE = 0
SENSOR_ACTION_ADD = 1
SENSOR_ACTION_REMOVE = 2

ACTION_EMPTY = 0
ACTION_REBOOT = 1
ACTION_BLINK = 2
ACTION_GET_MODULE = 3
ACTION_RESTORE_DEFAULTS = 4
ACTION_SEND_HB = 5
ACTION_EXT_SENSOR = 6
ACTION_SPARSE_37_DEPRECATED = 7
ACTION_GW_HB = 8

API_VERSION_V0 = 0
API_VERSION_V1 = 1
API_VERSION_V2 = 2
API_VERSION_V5 = 5 # Because of backward compatabilty issue we jumped from V2 to V5
API_VERSION_V6 = 6
API_VERSION_V7 = 7
API_VERSION_LATEST = 7

API_VERSION_SENSOR_V0 = 0

MODULE_EMPTY = 0
MODULE_GLOBAL = 0
MODULE_IF = 1
MODULE_DATAPATH = 2
MODULE_ENERGY_2400 = 3
MODULE_ENERGY_SUB1G = 4
MODULE_CALIBRATION = 5
MODULE_PWR_MGMT = 6
MODULE_SENSORS = 7
MODULE_PERIPH = 8

ENERGY_PATTERN_IDX_17 = 17
ENERGY_PATTERN_IDX_18 = 18
ENERGY_PATTERN_IDX_20 = 20
ENERGY_PATTERN_IDX_24 = 24
ENERGY_PATTERN_IDX_25 = 25
ENERGY_PATTERN_IDX_26 = 26
ENERGY_PATTERN_IDX_27 = 27
ENERGY_PATTERN_IDX_DYNAMIC = ENERGY_PATTERN_IDX_27
ENERGY_PATTERN_IDX_29 = 29
ENERGY_PATTERN_IDX_36 = 36
ENERGY_PATTERN_IDX_37 = 37
ENERGY_PATTERN_IDX_50 = 50
ENERGY_PATTERN_IDX_51 = 51
ENERGY_PATTERN_IDX_52 = 52
ENERGY_PATTERN_IDX_55 = 55
ENERGY_PATTERN_IDX_56 = 56
ENERGY_PATTERN_IDX_57 = 57
ENERGY_PATTERN_IDX_61 = 61
ENERGY_PATTERN_IDX_62 = 62
ENERGY_PATTERN_IDX_63 = 63
ENERGY_PATTERN_IDX_64 = 64
ENERGY_PATTERN_IDX_65 = 65
ENERGY_PATTERN_IDX_66 = 66
ENERGY_PATTERN_IDX_67 = 67
ENERGY_PATTERN_IDX_68 = 68
ENERGY_PATTERN_IDX_71 = 71
ENERGY_PATTERN_IDX_72 = 72
ENERGY_PATTERN_IDX_73 = 73
ENERGY_PATTERN_IDX_99 = 99
ENERGY_PATTERN_IDX_LAST = ENERGY_PATTERN_IDX_99

CHANNEL_FREQ_37 = 2402
CHANNEL_FREQ_38 = 2426
CHANNEL_FREQ_39 = 2480

CHANNEL_37 = 37
CHANNEL_38 = 38
CHANNEL_39 = 39

FREQUENCY_BAND_EDGE_2480 = 2480
FREQUENCY_BAND_EDGE_2475 = 2475

RADIO_TX_POWER_POS_2_DBM = 2
RADIO_TX_POWER_POS_3_DBM = 3
RADIO_TX_POWER_POS_6_DBM = 6

SUB1G_FREQ_865700 = 865700
SUB1G_FREQ_915000 = 915000
SUB1G_FREQ_916300 = 916300
SUB1G_FREQ_917500 = 917500
SUB1G_FREQ_918000 = 918000
SUB1G_FREQ_919100 = 919100

SUB1G_FREQ_PROFILE_915000 = 0
SUB1G_FREQ_PROFILE_865700 = 1
SUB1G_FREQ_PROFILE_916300 = 2
SUB1G_FREQ_PROFILE_917500 = 3
SUB1G_FREQ_PROFILE_918000 = 4
SUB1G_FREQ_PROFILE_919100 = 5

SUB1G_OUTPUT_POWER_9 = 9
SUB1G_OUTPUT_POWER_14 = 14
SUB1G_OUTPUT_POWER_17 = 17
SUB1G_OUTPUT_POWER_20 = 20
SUB1G_OUTPUT_POWER_23 = 23
SUB1G_OUTPUT_POWER_26 = 26
SUB1G_OUTPUT_POWER_29 = 29
SUB1G_OUTPUT_POWER_32 = 32

SUB1G_OUTPUT_POWER_PROFILE_14 = 0
SUB1G_OUTPUT_POWER_PROFILE_17 = 1
SUB1G_OUTPUT_POWER_PROFILE_20 = 2
SUB1G_OUTPUT_POWER_PROFILE_23 = 3
SUB1G_OUTPUT_POWER_PROFILE_26 = 4
SUB1G_OUTPUT_POWER_PROFILE_29 = 5
SUB1G_OUTPUT_POWER_PROFILE_32 = 6

HDR_DEFAULT_PKT_SIZE = 0x1E
HDR_DEFAULT_AD_TYPE = 0x16
HDR_DEFAULT_BRG_UUID_MSB = 0xC6
HDR_DEFAULT_BRG_UUID_LSB = 0xFC
HDR_DEFAULT_TAG_UUID_MSB = 0xAF
HDR_DEFAULT_TAG_UUID_LSB = 0xFD

BRG_DEFAULT_GLOBAL_PACING_GROUP = 0
BRG_DEFAULT_SCAN_CH = CHANNEL_37
BRG_DEFAULT_BRG_ENERGOUS_V1_OUTPUT_POWER_SUB_1_GHZ = SUB1G_OUTPUT_POWER_29
BRG_DEFAULT_OUTPUT_POWER_SUB_1_GHZ = SUB1G_OUTPUT_POWER_32
BRG_DEFAULT_BRG_ENERGOUS_V1_OUTPUT_POWER_SUB_1_GHZ_PROFILE = SUB1G_OUTPUT_POWER_PROFILE_29
BRG_DEFAULT_OUTPUT_POWER_SUB_1_GHZ_PROFILE = SUB1G_OUTPUT_POWER_PROFILE_32
BRG_DEFAULT_BRG_ENERGOUS_V1_RXTX_PERIOD = 100
BRG_DEFAULT_RXTX_PERIOD = 15
BRG_DEFAULT_BRG_ENERGOUS_V1_TX_PERIOD = 40
BRG_DEFAULT_TX_PERIOD = 5
BRG_DEFAULT_BRG_ENERGOUS_V1_ENERGY_PATTERN_IDX = ENERGY_PATTERN_IDX_71
BRG_DEFAULT_ENERGY_PATTERN_IDX = ENERGY_PATTERN_IDX_50
BRG_DEFAULT_SB_ENERGY_PATTERN_IDX = ENERGY_PATTERN_IDX_18
BRG_DEFAULT_ENERGIZE_FREQUENCY_2_4 = FREQUENCY_BAND_EDGE_2480
BRG_DEFAULT_BRG_ENERGOUS_V0_OUTPUT_POWER_2_4 = RADIO_TX_POWER_POS_3_DBM
BRG_DEFAULT_BRG_ENERGOUS_V1_OUTPUT_POWER_2_4 = RADIO_TX_POWER_POS_6_DBM
BRG_DEFAULT_BRG_ENERGOUS_V2_OUTPUT_POWER_2_4 = RADIO_TX_POWER_POS_3_DBM
BRG_DEFAULT_OUTPUT_POWER_2_4 = RADIO_TX_POWER_POS_2_DBM
BRG_DEFAULT_PACER_INTERVAL = 15
BRG_DEFAULT_PKT_TYPES_MASK = 0
BRG_DEFAULT_TX_PROB = 50
BRG_DEFAULT_TX_REPETITION = 0
BRG_DEFAULT_TRANSMIT_TIME_SUB_1_GHZ = 0
BRG_DEFAULT_SUB1G_FREQ = SUB1G_FREQ_915000
BRG_DEFAULT_SUB1G_FREQ_PROFILE = SUB1G_FREQ_PROFILE_915000

BRG_MGMT_MSG_TYPE_CFG_INFO = 1
BRG_MGMT_MSG_TYPE_OTA_UPDATE = 1
BRG_MGMT_MSG_TYPE_HB = 2
BRG_MGMT_MSG_TYPE_REBOOT = 3
BRG_MGMT_MSG_TYPE_LED_BLINK = 4
BRG_MGMT_MSG_TYPE_CFG_SET = 5
BRG_MGMT_MSG_TYPE_CFG_GET = 6
BRG_MGMT_MSG_TYPE_ACTION = 7

PWR_MGMT_DEFAULTS_LEDS_ON = 1
PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD = 20
PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN = 300
PWR_MGMT_DEFAULTS_ON_DURATION = 0
PWR_MGMT_DEFAULTS_SLEEP_DURATION = 0

PERIPH_ID_EMPTY = 0x00
PERIPH_ID_LIS2DW12_ACCELEROMETER = 0x01
PERIPH_ID_MAX_NUM = 0x02

LIS2DW12_ACCEL_CFG_VERSION_V0 = 0
LIS2DW12_ACCEL_CFG_VERSION_LATEST = 0

LIS2DW12_ACCEL_DEFAULTS_CFG_PACKET_LENGTH = 3
LIS2DW12_ACCEL_DEFAULTS_CFG_PACKET_VERSION = LIS2DW12_ACCEL_CFG_VERSION_LATEST
LIS2DW12_ACCEL_DEFAULTS_STATE_THRESHOLD = 65
LIS2DW12_ACCEL_DEFAULTS_WAKE_UP_DURATION = 91
LIS2DW12_ACCEL_DEFAULTS_SLEEP_DURATION = 26

class Hdr():
    def __init__(self, pkt_size=HDR_DEFAULT_PKT_SIZE, ad_type=HDR_DEFAULT_AD_TYPE, uuid_msb=HDR_DEFAULT_BRG_UUID_MSB, uuid_lsb=HDR_DEFAULT_BRG_UUID_LSB, group_id=0):
        self.pkt_size = pkt_size
        self.ad_type = ad_type
        self.uuid_msb = uuid_msb
        self.uuid_lsb = uuid_lsb
        self.group_id = group_id

    def __eq__(self, other):
        if isinstance(other, Hdr):
            return (
                self.pkt_size == other.pkt_size and
                self.ad_type == other.ad_type and
                self.uuid_msb == other.uuid_msb and
                self.uuid_lsb == other.uuid_lsb and
                self.group_id == other.group_id
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u8u24", self.pkt_size, self.ad_type, self.uuid_msb, self.uuid_lsb, self.group_id)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u8u24", binascii.unhexlify(string))
        self.pkt_size = d[0]
        self.ad_type = d[1]
        self.uuid_msb = d[2]
        self.uuid_lsb = d[3]
        self.group_id = d[4]

class GenericV7():
    def __init__(self, module_type=0, msg_type=0, api_version=7, seq_id=0, brg_mac=0, unused=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.unused = unused

    def __eq__(self, other):
        if isinstance(other, GenericV7):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u120", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.unused)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u120", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.unused = d[5]

class GenericV1():
    def __init__(self, msg_type=0, unused0=0, seq_id=0, unused1=0, brg_mac=0, unused2=0):
        self.msg_type = msg_type
        self.unused0 = unused0
        self.seq_id = seq_id
        self.unused1 = unused1
        self.brg_mac = brg_mac
        self.unused2 = unused2

    def __eq__(self, other):
        if isinstance(other, GenericV1):
            return (
                self.msg_type == other.msg_type and
                self.brg_mac == other.brg_mac
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u48u72", self.msg_type, self.unused0, self.seq_id, self.unused1, self.brg_mac, self.unused2)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u48u72", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.unused0 = d[1]
        self.seq_id = d[2]
        self.unused1 = d[3]
        self.brg_mac = d[4]
        self.unused2 = d[5]

class ActionV7():
    def __init__(self, msg_type=0, api_version=7, seq_id=0, brg_mac=0, action_id=0, action_params=0):
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.action_id = action_id
        self.action_params = action_params

    def __eq__(self, other):
        if isinstance(other, ActionV7):
            return (
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.action_id == other.action_id and
                self.action_params == other.action_params
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u8u112", self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.action_id, self.action_params)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u8u112", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.api_version = d[1]
        self.seq_id = d[2]
        self.brg_mac = d[3]
        self.action_id = d[4]
        self.action_params = d[5]

GW2BRG_CFG_V7_OUTPUT_POWER_SUB_1_GHZ_ENC = {SUB1G_OUTPUT_POWER_14:SUB1G_OUTPUT_POWER_PROFILE_14, SUB1G_OUTPUT_POWER_17:SUB1G_OUTPUT_POWER_PROFILE_17, SUB1G_OUTPUT_POWER_20:SUB1G_OUTPUT_POWER_PROFILE_20, SUB1G_OUTPUT_POWER_23:SUB1G_OUTPUT_POWER_PROFILE_23, SUB1G_OUTPUT_POWER_26:SUB1G_OUTPUT_POWER_PROFILE_26, SUB1G_OUTPUT_POWER_29:SUB1G_OUTPUT_POWER_PROFILE_29, SUB1G_OUTPUT_POWER_32:SUB1G_OUTPUT_POWER_PROFILE_32}
GW2BRG_CFG_V7_OUTPUT_POWER_SUB_1_GHZ_DEC = {SUB1G_OUTPUT_POWER_PROFILE_14:SUB1G_OUTPUT_POWER_14, SUB1G_OUTPUT_POWER_PROFILE_17:SUB1G_OUTPUT_POWER_17, SUB1G_OUTPUT_POWER_PROFILE_20:SUB1G_OUTPUT_POWER_20, SUB1G_OUTPUT_POWER_PROFILE_23:SUB1G_OUTPUT_POWER_23, SUB1G_OUTPUT_POWER_PROFILE_26:SUB1G_OUTPUT_POWER_26, SUB1G_OUTPUT_POWER_PROFILE_29:SUB1G_OUTPUT_POWER_29, SUB1G_OUTPUT_POWER_PROFILE_32:SUB1G_OUTPUT_POWER_32}
GW2BRG_CFG_V7_SUB1G_FREQ_PROFILE_ENC = {SUB1G_FREQ_915000:SUB1G_FREQ_PROFILE_915000, SUB1G_FREQ_865700:SUB1G_FREQ_PROFILE_865700, SUB1G_FREQ_916300:SUB1G_FREQ_PROFILE_916300, SUB1G_FREQ_917500:SUB1G_FREQ_PROFILE_917500, SUB1G_FREQ_918000:SUB1G_FREQ_PROFILE_918000, SUB1G_FREQ_919100:SUB1G_FREQ_PROFILE_919100}
GW2BRG_CFG_V7_SUB1G_FREQ_PROFILE_DEC = {SUB1G_FREQ_PROFILE_915000:SUB1G_FREQ_915000, SUB1G_FREQ_PROFILE_865700:SUB1G_FREQ_865700, SUB1G_FREQ_PROFILE_916300:SUB1G_FREQ_916300, SUB1G_FREQ_PROFILE_917500:SUB1G_FREQ_917500, SUB1G_FREQ_PROFILE_918000:SUB1G_FREQ_918000, SUB1G_FREQ_PROFILE_919100:SUB1G_FREQ_919100}
class Gw2BrgCfgV7():
    def __init__(self, msg_type=0, global_pacing_group=BRG_DEFAULT_GLOBAL_PACING_GROUP, output_power_sub_1_ghz=BRG_DEFAULT_OUTPUT_POWER_SUB_1_GHZ, seq_id=0, brg_mac=0, unused0=0, pkt_types_mask=BRG_DEFAULT_PKT_TYPES_MASK, unused1=0, rxtx_period=BRG_DEFAULT_RXTX_PERIOD, tx_period=BRG_DEFAULT_TX_PERIOD, energy_pattern_idx=BRG_DEFAULT_ENERGY_PATTERN_IDX, output_power_2_4=BRG_DEFAULT_OUTPUT_POWER_2_4, pacer_interval=BRG_DEFAULT_PACER_INTERVAL, unused2=0, tx_prob=BRG_DEFAULT_TX_PROB, tx_repetition=BRG_DEFAULT_TX_REPETITION, transmit_time_sub_1_ghz=BRG_DEFAULT_TRANSMIT_TIME_SUB_1_GHZ, sub1g_freq_profile=BRG_DEFAULT_SUB1G_FREQ):
        self.msg_type = msg_type
        self.global_pacing_group = global_pacing_group
        self.output_power_sub_1_ghz = output_power_sub_1_ghz
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.unused0 = unused0
        self.pkt_types_mask = pkt_types_mask
        self.unused1 = unused1
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power_2_4 = output_power_2_4
        self.pacer_interval = pacer_interval
        self.unused2 = unused2
        self.tx_prob = tx_prob
        self.tx_repetition = tx_repetition
        self.transmit_time_sub_1_ghz = transmit_time_sub_1_ghz
        self.sub1g_freq_profile = sub1g_freq_profile

    def __eq__(self, other):
        if isinstance(other, (Gw2BrgCfgV7, Brg2GwCfgV7)):
            return (
                self.msg_type == other.msg_type and
                self.global_pacing_group == other.global_pacing_group and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.brg_mac == other.brg_mac and
                self.pkt_types_mask == other.pkt_types_mask and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval and
                self.tx_prob == other.tx_prob and
                self.tx_repetition == other.tx_repetition and
                self.sub1g_freq_profile == other.sub1g_freq_profile
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u4u4u8u48u3u5u48u8u8u8s8u16u1u3u4u4u4", self.msg_type, self.global_pacing_group, GW2BRG_CFG_V7_OUTPUT_POWER_SUB_1_GHZ_ENC[self.output_power_sub_1_ghz], self.seq_id, self.brg_mac, self.unused0, self.pkt_types_mask, self.unused1, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power_2_4, self.pacer_interval, self.unused2, ((self.tx_prob-30)//10), self.tx_repetition, self.transmit_time_sub_1_ghz, GW2BRG_CFG_V7_SUB1G_FREQ_PROFILE_ENC[self.sub1g_freq_profile])
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u4u4u8u48u3u5u48u8u8u8s8u16u1u3u4u4u4", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.global_pacing_group = d[1]
        self.output_power_sub_1_ghz = GW2BRG_CFG_V7_OUTPUT_POWER_SUB_1_GHZ_DEC[d[2]]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.unused0 = d[5]
        self.pkt_types_mask = d[6]
        self.unused1 = d[7]
        self.rxtx_period = d[8]
        self.tx_period = d[9]
        self.energy_pattern_idx = d[10]
        self.output_power_2_4 = d[11]
        self.pacer_interval = d[12]
        self.unused2 = d[13]
        self.tx_prob = ((d[14]*10)+30)
        self.tx_repetition = d[15]
        self.transmit_time_sub_1_ghz = d[16]
        self.sub1g_freq_profile = GW2BRG_CFG_V7_SUB1G_FREQ_PROFILE_DEC[d[17]]

class Gw2BrgCfgV6():
    def __init__(self, msg_type=0, global_pacing_group=0, output_power_sub_1_ghz=0, seq_id=0, brg_mac=0, unused0=0, unused1=0, rxtx_period=0, tx_period=0, energy_pattern_idx=0, output_power_2_4=0, pacer_interval=0, unused2=0, tx_prob=0, tx_repetition=0, transmit_time_sub_1_ghz=0, sub1g_freq_profile=0):
        self.msg_type = msg_type
        self.global_pacing_group = global_pacing_group
        self.output_power_sub_1_ghz = output_power_sub_1_ghz
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.unused0 = unused0
        self.unused1 = unused1
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power_2_4 = output_power_2_4
        self.pacer_interval = pacer_interval
        self.unused2 = unused2
        self.tx_prob = tx_prob
        self.tx_repetition = tx_repetition
        self.transmit_time_sub_1_ghz = transmit_time_sub_1_ghz
        self.sub1g_freq_profile = sub1g_freq_profile

    def __eq__(self, other):
        if isinstance(other, (Gw2BrgCfgV6, Brg2GwCfgV6)):
            return (
                self.msg_type == other.msg_type and
                self.global_pacing_group == other.global_pacing_group and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.brg_mac == other.brg_mac and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval and
                self.tx_prob == other.tx_prob and
                self.tx_repetition == other.tx_repetition and
                self.sub1g_freq_profile == other.sub1g_freq_profile
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u4u4u8u48u8u48u8u8u8s8u16u1u3u4u4u4", self.msg_type, self.global_pacing_group, self.output_power_sub_1_ghz, self.seq_id, self.brg_mac, self.unused0, self.unused1, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power_2_4, self.pacer_interval, self.unused2, self.tx_prob, self.tx_repetition, self.transmit_time_sub_1_ghz, self.sub1g_freq_profile)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u4u4u8u48u8u48u8u8u8s8u16u1u3u4u4u4", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.global_pacing_group = d[1]
        self.output_power_sub_1_ghz = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.unused0 = d[5]
        self.unused1 = d[6]
        self.rxtx_period = d[7]
        self.tx_period = d[8]
        self.energy_pattern_idx = d[9]
        self.output_power_2_4 = d[10]
        self.pacer_interval = d[11]
        self.unused2 = d[12]
        self.tx_prob = d[13]
        self.tx_repetition = d[14]
        self.transmit_time_sub_1_ghz = d[15]
        self.sub1g_freq_profile = d[16]

class Gw2BrgCfgV5():
    def __init__(self, msg_type=0, unused0=0, output_power_sub_1_ghz=0, seq_id=0, brg_mac=0, unused1=0, rxtx_period=0, tx_period=0, energy_pattern_idx=0, output_power_2_4=0, pacer_interval=0, global_pacing=0, tx_prob=0, stat_freq=0, transmit_time_sub_1_ghz=0, sub1g_freq_profile=0):
        self.msg_type = msg_type
        self.unused0 = unused0
        self.output_power_sub_1_ghz = output_power_sub_1_ghz
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.unused1 = unused1
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power_2_4 = output_power_2_4
        self.pacer_interval = pacer_interval
        self.global_pacing = global_pacing
        self.tx_prob = tx_prob
        self.stat_freq = stat_freq
        self.transmit_time_sub_1_ghz = transmit_time_sub_1_ghz
        self.sub1g_freq_profile = sub1g_freq_profile

    def __eq__(self, other):
        if isinstance(other, (Gw2BrgCfgV5, Brg2GwCfgV5)):
            return (
                self.msg_type == other.msg_type and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.brg_mac == other.brg_mac and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval and
                self.global_pacing == other.global_pacing and
                self.tx_prob == other.tx_prob and
                self.stat_freq == other.stat_freq and
                self.sub1g_freq_profile == other.sub1g_freq_profile
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u4u4u8u48u56u8u8u8s8u16u1u3u4u4u4", self.msg_type, self.unused0, self.output_power_sub_1_ghz, self.seq_id, self.brg_mac, self.unused1, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power_2_4, self.pacer_interval, self.global_pacing, self.tx_prob, self.stat_freq, self.transmit_time_sub_1_ghz, self.sub1g_freq_profile)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u4u4u8u48u56u8u8u8s8u16u1u3u4u4u4", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.unused0 = d[1]
        self.output_power_sub_1_ghz = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.unused1 = d[5]
        self.rxtx_period = d[6]
        self.tx_period = d[7]
        self.energy_pattern_idx = d[8]
        self.output_power_2_4 = d[9]
        self.pacer_interval = d[10]
        self.global_pacing = d[11]
        self.tx_prob = d[12]
        self.stat_freq = d[13]
        self.transmit_time_sub_1_ghz = d[14]
        self.sub1g_freq_profile = d[15]

class Gw2BrgCfgV2():
    def __init__(self, msg_type=0, unused=0, output_power_sub_1_ghz=0, seq_id=0, brg_mac=0, gw_mac=0, rx_rssi=0, rxtx_period=0, tx_period=0, energy_pattern_idx=0, output_power_2_4=0, pacer_interval=0, global_pacing=0, tx_prob=0, stat_freq=0, transmit_time_sub_1_ghz=0, sub1g_freq_profile=0):
        self.msg_type = msg_type
        self.unused = unused
        self.output_power_sub_1_ghz = output_power_sub_1_ghz
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.gw_mac = gw_mac
        self.rx_rssi = rx_rssi
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power_2_4 = output_power_2_4
        self.pacer_interval = pacer_interval
        self.global_pacing = global_pacing
        self.tx_prob = tx_prob
        self.stat_freq = stat_freq
        self.transmit_time_sub_1_ghz = transmit_time_sub_1_ghz
        self.sub1g_freq_profile = sub1g_freq_profile

    def __eq__(self, other):
        if isinstance(other, (Gw2BrgCfgV2, Brg2GwCfgV2)):
            return (
                self.msg_type == other.msg_type and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.brg_mac == other.brg_mac and
                self.gw_mac == other.gw_mac and
                self.rx_rssi == other.rx_rssi and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval and
                self.global_pacing == other.global_pacing and
                self.tx_prob == other.tx_prob and
                self.stat_freq == other.stat_freq and
                self.sub1g_freq_profile == other.sub1g_freq_profile
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u4u4u8u48u48u8u8u8u8s8u16u1u3u4u4u4", self.msg_type, self.unused, self.output_power_sub_1_ghz, self.seq_id, self.brg_mac, self.gw_mac, self.rx_rssi, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power_2_4, self.pacer_interval, self.global_pacing, self.tx_prob, self.stat_freq, self.transmit_time_sub_1_ghz, self.sub1g_freq_profile)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u4u4u8u48u48u8u8u8u8s8u16u1u3u4u4u4", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.unused = d[1]
        self.output_power_sub_1_ghz = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.gw_mac = d[5]
        self.rx_rssi = d[6]
        self.rxtx_period = d[7]
        self.tx_period = d[8]
        self.energy_pattern_idx = d[9]
        self.output_power_2_4 = d[10]
        self.pacer_interval = d[11]
        self.global_pacing = d[12]
        self.tx_prob = d[13]
        self.stat_freq = d[14]
        self.transmit_time_sub_1_ghz = d[15]
        self.sub1g_freq_profile = d[16]

class Gw2BrgCfgV1():
    def __init__(self, msg_type=0, unused0=0, seq_id=0, brg_mac=0, gw_mac=0, rx_rssi=0, rxtx_period=0, tx_period=0, energy_pattern_idx=0, output_power=0, pacer_interval=0, tx_prob=0, unused1=0):
        self.msg_type = msg_type
        self.unused0 = unused0
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.gw_mac = gw_mac
        self.rx_rssi = rx_rssi
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power = output_power
        self.pacer_interval = pacer_interval
        self.tx_prob = tx_prob
        self.unused1 = unused1

    def __eq__(self, other):
        if isinstance(other, (Gw2BrgCfgV1, Brg2GwCfgV1)):
            return (
                self.msg_type == other.msg_type and
                self.brg_mac == other.brg_mac and
                self.gw_mac == other.gw_mac and
                self.rx_rssi == other.rx_rssi and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power == other.output_power and
                self.pacer_interval == other.pacer_interval and
                self.tx_prob == other.tx_prob
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u48u8u8u8u8s8u16u8u8", self.msg_type, self.unused0, self.seq_id, self.brg_mac, self.gw_mac, self.rx_rssi, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power, self.pacer_interval, self.tx_prob, self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u48u8u8u8u8s8u16u8u8", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.unused0 = d[1]
        self.seq_id = d[2]
        self.brg_mac = d[3]
        self.gw_mac = d[4]
        self.rx_rssi = d[5]
        self.rxtx_period = d[6]
        self.tx_period = d[7]
        self.energy_pattern_idx = d[8]
        self.output_power = d[9]
        self.pacer_interval = d[10]
        self.tx_prob = d[11]
        self.unused1 = d[12]

BRG2GW_CFG_V7_OUTPUT_POWER_SUB_1_GHZ_ENC = {SUB1G_OUTPUT_POWER_14:SUB1G_OUTPUT_POWER_PROFILE_14, SUB1G_OUTPUT_POWER_17:SUB1G_OUTPUT_POWER_PROFILE_17, SUB1G_OUTPUT_POWER_20:SUB1G_OUTPUT_POWER_PROFILE_20, SUB1G_OUTPUT_POWER_23:SUB1G_OUTPUT_POWER_PROFILE_23, SUB1G_OUTPUT_POWER_26:SUB1G_OUTPUT_POWER_PROFILE_26, SUB1G_OUTPUT_POWER_29:SUB1G_OUTPUT_POWER_PROFILE_29, SUB1G_OUTPUT_POWER_32:SUB1G_OUTPUT_POWER_PROFILE_32}
BRG2GW_CFG_V7_OUTPUT_POWER_SUB_1_GHZ_DEC = {SUB1G_OUTPUT_POWER_PROFILE_14:SUB1G_OUTPUT_POWER_14, SUB1G_OUTPUT_POWER_PROFILE_17:SUB1G_OUTPUT_POWER_17, SUB1G_OUTPUT_POWER_PROFILE_20:SUB1G_OUTPUT_POWER_20, SUB1G_OUTPUT_POWER_PROFILE_23:SUB1G_OUTPUT_POWER_23, SUB1G_OUTPUT_POWER_PROFILE_26:SUB1G_OUTPUT_POWER_26, SUB1G_OUTPUT_POWER_PROFILE_29:SUB1G_OUTPUT_POWER_29, SUB1G_OUTPUT_POWER_PROFILE_32:SUB1G_OUTPUT_POWER_32}
BRG2GW_CFG_V7_SUB1G_FREQ_PROFILE_ENC = {SUB1G_FREQ_915000:SUB1G_FREQ_PROFILE_915000, SUB1G_FREQ_865700:SUB1G_FREQ_PROFILE_865700, SUB1G_FREQ_916300:SUB1G_FREQ_PROFILE_916300, SUB1G_FREQ_917500:SUB1G_FREQ_PROFILE_917500, SUB1G_FREQ_918000:SUB1G_FREQ_PROFILE_918000, SUB1G_FREQ_919100:SUB1G_FREQ_PROFILE_919100}
BRG2GW_CFG_V7_SUB1G_FREQ_PROFILE_DEC = {SUB1G_FREQ_PROFILE_915000:SUB1G_FREQ_915000, SUB1G_FREQ_PROFILE_865700:SUB1G_FREQ_865700, SUB1G_FREQ_PROFILE_916300:SUB1G_FREQ_916300, SUB1G_FREQ_PROFILE_917500:SUB1G_FREQ_917500, SUB1G_FREQ_PROFILE_918000:SUB1G_FREQ_918000, SUB1G_FREQ_PROFILE_919100:SUB1G_FREQ_919100}
class Brg2GwCfgV7():
    def __init__(self, msg_type=0, api_version=7, seq_id=0, unused0=0, tx_prob=BRG_DEFAULT_TX_PROB, tx_repetition=BRG_DEFAULT_TX_REPETITION, global_pacing_group=BRG_DEFAULT_GLOBAL_PACING_GROUP, output_power_sub_1_ghz=BRG_DEFAULT_OUTPUT_POWER_SUB_1_GHZ, transmit_time_sub_1_ghz=BRG_DEFAULT_TRANSMIT_TIME_SUB_1_GHZ, sub1g_freq_profile=BRG_DEFAULT_SUB1G_FREQ, bl_version=0, board_type=0, unused1=0, pkt_types_mask=BRG_DEFAULT_PKT_TYPES_MASK, brg_mac=0, major_ver=0, minor_ver=0, build_ver=0, rxtx_period=BRG_DEFAULT_RXTX_PERIOD, tx_period=BRG_DEFAULT_TX_PERIOD, energy_pattern_idx=BRG_DEFAULT_ENERGY_PATTERN_IDX, output_power_2_4=BRG_DEFAULT_OUTPUT_POWER_2_4, pacer_interval=BRG_DEFAULT_PACER_INTERVAL):
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.unused0 = unused0
        self.tx_prob = tx_prob
        self.tx_repetition = tx_repetition
        self.global_pacing_group = global_pacing_group
        self.output_power_sub_1_ghz = output_power_sub_1_ghz
        self.transmit_time_sub_1_ghz = transmit_time_sub_1_ghz
        self.sub1g_freq_profile = sub1g_freq_profile
        self.bl_version = bl_version
        self.board_type = board_type
        self.unused1 = unused1
        self.pkt_types_mask = pkt_types_mask
        self.brg_mac = brg_mac
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.build_ver = build_ver
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power_2_4 = output_power_2_4
        self.pacer_interval = pacer_interval

    def __eq__(self, other):
        if isinstance(other, Brg2GwCfgV7):
            return (
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.tx_prob == other.tx_prob and
                self.tx_repetition == other.tx_repetition and
                self.global_pacing_group == other.global_pacing_group and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.sub1g_freq_profile == other.sub1g_freq_profile and
                self.bl_version == other.bl_version and
                self.board_type == other.board_type and
                self.pkt_types_mask == other.pkt_types_mask and
                self.brg_mac == other.brg_mac and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.build_ver == other.build_ver and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval
            )
        if isinstance(other, Gw2BrgCfgV7):
            return (
                self.msg_type == other.msg_type and
                self.tx_prob == other.tx_prob and
                self.tx_repetition == other.tx_repetition and
                self.global_pacing_group == other.global_pacing_group and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.sub1g_freq_profile == other.sub1g_freq_profile and
                self.pkt_types_mask == other.pkt_types_mask and
                self.brg_mac == other.brg_mac and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u1u3u4u4u4u4u4u8u8u3u5u48u8u8u8u8u8u8s8u16", self.msg_type, self.api_version, self.seq_id, self.unused0, ((self.tx_prob-30)//10), self.tx_repetition, self.global_pacing_group, BRG2GW_CFG_V7_OUTPUT_POWER_SUB_1_GHZ_ENC[self.output_power_sub_1_ghz], self.transmit_time_sub_1_ghz, BRG2GW_CFG_V7_SUB1G_FREQ_PROFILE_ENC[self.sub1g_freq_profile], self.bl_version, self.board_type, self.unused1, self.pkt_types_mask, self.brg_mac, self.major_ver, self.minor_ver, self.build_ver, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power_2_4, self.pacer_interval)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u1u3u4u4u4u4u4u8u8u3u5u48u8u8u8u8u8u8s8u16", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.api_version = d[1]
        self.seq_id = d[2]
        self.unused0 = d[3]
        self.tx_prob = ((d[4]*10)+30)
        self.tx_repetition = d[5]
        self.global_pacing_group = d[6]
        self.output_power_sub_1_ghz = BRG2GW_CFG_V7_OUTPUT_POWER_SUB_1_GHZ_DEC[d[7]]
        self.transmit_time_sub_1_ghz = d[8]
        self.sub1g_freq_profile = BRG2GW_CFG_V7_SUB1G_FREQ_PROFILE_DEC[d[9]]
        self.bl_version = d[10]
        self.board_type = d[11]
        self.unused1 = d[12]
        self.pkt_types_mask = d[13]
        self.brg_mac = d[14]
        self.major_ver = d[15]
        self.minor_ver = d[16]
        self.build_ver = d[17]
        self.rxtx_period = d[18]
        self.tx_period = d[19]
        self.energy_pattern_idx = d[20]
        self.output_power_2_4 = d[21]
        self.pacer_interval = d[22]

class Brg2GwCfgV6():
    def __init__(self, msg_type=0, api_version=6, seq_id=0, unused0=0, tx_prob=0, tx_repetition=0, global_pacing_group=0, output_power_sub_1_ghz=0, transmit_time_sub_1_ghz=0, sub1g_freq_profile=0, bl_version=0, board_type=0, unused1=0, brg_mac=0, major_ver=0, minor_ver=0, build_ver=0, cycle_time=0, transmit_time_2_4=0, energy_pattern_idx=0, output_power_2_4=0, pacer_interval=0):
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.unused0 = unused0
        self.tx_prob = tx_prob
        self.tx_repetition = tx_repetition
        self.global_pacing_group = global_pacing_group
        self.output_power_sub_1_ghz = output_power_sub_1_ghz
        self.transmit_time_sub_1_ghz = transmit_time_sub_1_ghz
        self.sub1g_freq_profile = sub1g_freq_profile
        self.bl_version = bl_version
        self.board_type = board_type
        self.unused1 = unused1
        self.brg_mac = brg_mac
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.build_ver = build_ver
        self.cycle_time = cycle_time
        self.transmit_time_2_4 = transmit_time_2_4
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power_2_4 = output_power_2_4
        self.pacer_interval = pacer_interval

    def __eq__(self, other):
        if isinstance(other, Brg2GwCfgV6):
            return (
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.tx_prob == other.tx_prob and
                self.tx_repetition == other.tx_repetition and
                self.global_pacing_group == other.global_pacing_group and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.sub1g_freq_profile == other.sub1g_freq_profile and
                self.bl_version == other.bl_version and
                self.board_type == other.board_type and
                self.brg_mac == other.brg_mac and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.build_ver == other.build_ver and
                self.cycle_time == other.cycle_time and
                self.transmit_time_2_4 == other.transmit_time_2_4 and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval
            )
        if isinstance(other, Gw2BrgCfgV6):
            return (
                self.msg_type == other.msg_type and
                self.tx_prob == other.tx_prob and
                self.tx_repetition == other.tx_repetition and
                self.global_pacing_group == other.global_pacing_group and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.sub1g_freq_profile == other.sub1g_freq_profile and
                self.brg_mac == other.brg_mac and
                self.cycle_time == other.cycle_time and
                self.transmit_time_2_4 == other.transmit_time_2_4 and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u1u3u4u4u4u4u4u8u8u8u48u8u8u8u8u8u8s8u16", self.msg_type, self.api_version, self.seq_id, self.unused0, self.tx_prob, self.tx_repetition, self.global_pacing_group, self.output_power_sub_1_ghz, self.transmit_time_sub_1_ghz, self.sub1g_freq_profile, self.bl_version, self.board_type, self.unused1, self.brg_mac, self.major_ver, self.minor_ver, self.build_ver, self.cycle_time, self.transmit_time_2_4, self.energy_pattern_idx, self.output_power_2_4, self.pacer_interval)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u1u3u4u4u4u4u4u8u8u8u48u8u8u8u8u8u8s8u16", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.api_version = d[1]
        self.seq_id = d[2]
        self.unused0 = d[3]
        self.tx_prob = d[4]
        self.tx_repetition = d[5]
        self.global_pacing_group = d[6]
        self.output_power_sub_1_ghz = d[7]
        self.transmit_time_sub_1_ghz = d[8]
        self.sub1g_freq_profile = d[9]
        self.bl_version = d[10]
        self.board_type = d[11]
        self.unused1 = d[12]
        self.brg_mac = d[13]
        self.major_ver = d[14]
        self.minor_ver = d[15]
        self.build_ver = d[16]
        self.cycle_time = d[17]
        self.transmit_time_2_4 = d[18]
        self.energy_pattern_idx = d[19]
        self.output_power_2_4 = d[20]
        self.pacer_interval = d[21]

class Brg2GwCfgV5():
    def __init__(self, msg_type=0, api_version=5, seq_id=0, global_pacing=0, tx_prob=0, stat_freq=0, unused0=0, output_power_sub_1_ghz=0, transmit_time_sub_1_ghz=0, sub1g_freq_profile=0, bl_version=0, board_type=0, unused1=0, brg_mac=0, major_ver=0, minor_ver=0, build_ver=0, rxtx_period=0, tx_period=0, energy_pattern_idx=0, output_power_2_4=0, pacer_interval=0):
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.global_pacing = global_pacing
        self.tx_prob = tx_prob
        self.stat_freq = stat_freq
        self.unused0 = unused0
        self.output_power_sub_1_ghz = output_power_sub_1_ghz
        self.transmit_time_sub_1_ghz = transmit_time_sub_1_ghz
        self.sub1g_freq_profile = sub1g_freq_profile
        self.bl_version = bl_version
        self.board_type = board_type
        self.unused1 = unused1
        self.brg_mac = brg_mac
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.build_ver = build_ver
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power_2_4 = output_power_2_4
        self.pacer_interval = pacer_interval

    def __eq__(self, other):
        if isinstance(other, Brg2GwCfgV5):
            return (
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.global_pacing == other.global_pacing and
                self.tx_prob == other.tx_prob and
                self.stat_freq == other.stat_freq and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.sub1g_freq_profile == other.sub1g_freq_profile and
                self.bl_version == other.bl_version and
                self.board_type == other.board_type and
                self.brg_mac == other.brg_mac and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.build_ver == other.build_ver and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval
            )
        if isinstance(other, Gw2BrgCfgV5):
            return (
                self.msg_type == other.msg_type and
                self.global_pacing == other.global_pacing and
                self.tx_prob == other.tx_prob and
                self.stat_freq == other.stat_freq and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.sub1g_freq_profile == other.sub1g_freq_profile and
                self.brg_mac == other.brg_mac and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u1u3u4u4u4u4u4u8u8u8u48u8u8u8u8u8u8s8u16", self.msg_type, self.api_version, self.seq_id, self.global_pacing, self.tx_prob, self.stat_freq, self.unused0, self.output_power_sub_1_ghz, self.transmit_time_sub_1_ghz, self.sub1g_freq_profile, self.bl_version, self.board_type, self.unused1, self.brg_mac, self.major_ver, self.minor_ver, self.build_ver, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power_2_4, self.pacer_interval)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u1u3u4u4u4u4u4u8u8u8u48u8u8u8u8u8u8s8u16", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.api_version = d[1]
        self.seq_id = d[2]
        self.global_pacing = d[3]
        self.tx_prob = d[4]
        self.stat_freq = d[5]
        self.unused0 = d[6]
        self.output_power_sub_1_ghz = d[7]
        self.transmit_time_sub_1_ghz = d[8]
        self.sub1g_freq_profile = d[9]
        self.bl_version = d[10]
        self.board_type = d[11]
        self.unused1 = d[12]
        self.brg_mac = d[13]
        self.major_ver = d[14]
        self.minor_ver = d[15]
        self.build_ver = d[16]
        self.rxtx_period = d[17]
        self.tx_period = d[18]
        self.energy_pattern_idx = d[19]
        self.output_power_2_4 = d[20]
        self.pacer_interval = d[21]

class Brg2GwCfgV2():
    def __init__(self, msg_type=0, board_type=0, seq_id=0, global_pacing=0, tx_prob=0, stat_freq=0, unused0=0, output_power_sub_1_ghz=0, transmit_time_sub_1_ghz=0, sub1g_freq_profile=0, bl_version=0, unused1=0, brg_mac=0, major_ver=0, minor_ver=0, build_ver=0, rxtx_period=0, tx_period=0, energy_pattern_idx=0, output_power_2_4=0, pacer_interval=0):
        self.msg_type = msg_type
        self.board_type = board_type
        self.seq_id = seq_id
        self.global_pacing = global_pacing
        self.tx_prob = tx_prob
        self.stat_freq = stat_freq
        self.unused0 = unused0
        self.output_power_sub_1_ghz = output_power_sub_1_ghz
        self.transmit_time_sub_1_ghz = transmit_time_sub_1_ghz
        self.sub1g_freq_profile = sub1g_freq_profile
        self.bl_version = bl_version
        self.unused1 = unused1
        self.brg_mac = brg_mac
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.build_ver = build_ver
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power_2_4 = output_power_2_4
        self.pacer_interval = pacer_interval

    def __eq__(self, other):
        if isinstance(other, Brg2GwCfgV2):
            return (
                self.msg_type == other.msg_type and
                self.board_type == other.board_type and
                self.global_pacing == other.global_pacing and
                self.tx_prob == other.tx_prob and
                self.stat_freq == other.stat_freq and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.sub1g_freq_profile == other.sub1g_freq_profile and
                self.bl_version == other.bl_version and
                self.brg_mac == other.brg_mac and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.build_ver == other.build_ver and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval
            )
        if isinstance(other, Gw2BrgCfgV2):
            return (
                self.msg_type == other.msg_type and
                self.global_pacing == other.global_pacing and
                self.tx_prob == other.tx_prob and
                self.stat_freq == other.stat_freq and
                self.output_power_sub_1_ghz == other.output_power_sub_1_ghz and
                self.sub1g_freq_profile == other.sub1g_freq_profile and
                self.brg_mac == other.brg_mac and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power_2_4 == other.output_power_2_4 and
                self.pacer_interval == other.pacer_interval
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u1u3u4u4u4u4u4u8u16u48u8u8u8u8u8u8s8u16", self.msg_type, self.board_type, self.seq_id, self.global_pacing, self.tx_prob, self.stat_freq, self.unused0, self.output_power_sub_1_ghz, self.transmit_time_sub_1_ghz, self.sub1g_freq_profile, self.bl_version, self.unused1, self.brg_mac, self.major_ver, self.minor_ver, self.build_ver, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power_2_4, self.pacer_interval)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u1u3u4u4u4u4u4u8u16u48u8u8u8u8u8u8s8u16", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.board_type = d[1]
        self.seq_id = d[2]
        self.global_pacing = d[3]
        self.tx_prob = d[4]
        self.stat_freq = d[5]
        self.unused0 = d[6]
        self.output_power_sub_1_ghz = d[7]
        self.transmit_time_sub_1_ghz = d[8]
        self.sub1g_freq_profile = d[9]
        self.bl_version = d[10]
        self.unused1 = d[11]
        self.brg_mac = d[12]
        self.major_ver = d[13]
        self.minor_ver = d[14]
        self.build_ver = d[15]
        self.rxtx_period = d[16]
        self.tx_period = d[17]
        self.energy_pattern_idx = d[18]
        self.output_power_2_4 = d[19]
        self.pacer_interval = d[20]

class Brg2GwCfgV1():
    def __init__(self, msg_type=0, unused0=0, seq_id=0, gw_mac=0, brg_mac=0, major_ver=0, minor_ver=0, build_ver=0, unused1=0, tx_prob=0, is_dual_band=0, rxtx_period=0, tx_period=0, energy_pattern_idx=0, output_power=0, pacer_interval=0):
        self.msg_type = msg_type
        self.unused0 = unused0
        self.seq_id = seq_id
        self.gw_mac = gw_mac
        self.brg_mac = brg_mac
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.build_ver = build_ver
        self.unused1 = unused1
        self.tx_prob = tx_prob
        self.is_dual_band = is_dual_band
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power = output_power
        self.pacer_interval = pacer_interval

    def __eq__(self, other):
        if isinstance(other, Brg2GwCfgV1):
            return (
                self.msg_type == other.msg_type and
                self.gw_mac == other.gw_mac and
                self.brg_mac == other.brg_mac and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.build_ver == other.build_ver and
                self.tx_prob == other.tx_prob and
                self.is_dual_band == other.is_dual_band and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power == other.output_power and
                self.pacer_interval == other.pacer_interval
            )
        if isinstance(other, Gw2BrgCfgV1):
            return (
                self.msg_type == other.msg_type and
                self.gw_mac == other.gw_mac and
                self.brg_mac == other.brg_mac and
                self.tx_prob == other.tx_prob and
                self.is_dual_band == other.is_dual_band and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power == other.output_power and
                self.pacer_interval == other.pacer_interval
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u48u4u4u4u4u7u1u8u8u8s8u16", self.msg_type, self.unused0, self.seq_id, self.gw_mac, self.brg_mac, self.major_ver, self.minor_ver, self.build_ver, self.unused1, self.tx_prob, self.is_dual_band, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power, self.pacer_interval)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u48u4u4u4u4u7u1u8u8u8s8u16", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.unused0 = d[1]
        self.seq_id = d[2]
        self.gw_mac = d[3]
        self.brg_mac = d[4]
        self.major_ver = d[5]
        self.minor_ver = d[6]
        self.build_ver = d[7]
        self.unused1 = d[8]
        self.tx_prob = d[9]
        self.is_dual_band = d[10]
        self.rxtx_period = d[11]
        self.tx_period = d[12]
        self.energy_pattern_idx = d[13]
        self.output_power = d[14]
        self.pacer_interval = d[15]

class Brg2GwCfgV0():
    def __init__(self, msg_type=0, bridge_id=0, seq_id=0, gw_mac=0, brg_mac=0, major_ver=0, minor_ver=0, build_ver=0, rxtx_period=0, tx_period=0, energy_pattern_idx=0, output_power=0, pacer_interval=0):
        self.msg_type = msg_type
        self.bridge_id = bridge_id
        self.seq_id = seq_id
        self.gw_mac = gw_mac
        self.brg_mac = brg_mac
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.build_ver = build_ver
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern_idx = energy_pattern_idx
        self.output_power = output_power
        self.pacer_interval = pacer_interval

    def __eq__(self, other):
        if isinstance(other, Brg2GwCfgV0):
            return (
                self.msg_type == other.msg_type and
                self.bridge_id == other.bridge_id and
                self.gw_mac == other.gw_mac and
                self.brg_mac == other.brg_mac and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.build_ver == other.build_ver and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power == other.output_power and
                self.pacer_interval == other.pacer_interval
            )
        if isinstance(other, Gw2BrgCfgV0):
            return (
                self.msg_type == other.msg_type and
                self.bridge_id == other.bridge_id and
                self.gw_mac == other.gw_mac and
                self.brg_mac == other.brg_mac and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern_idx == other.energy_pattern_idx and
                self.output_power == other.output_power and
                self.pacer_interval == other.pacer_interval
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u48u8u8u8u8u8u8s8u16", self.msg_type, self.bridge_id, self.seq_id, self.gw_mac, self.brg_mac, self.major_ver, self.minor_ver, self.build_ver, self.rxtx_period, self.tx_period, self.energy_pattern_idx, self.output_power, self.pacer_interval)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u48u8u8u8u8u8u8s8u16", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.bridge_id = d[1]
        self.seq_id = d[2]
        self.gw_mac = d[3]
        self.brg_mac = d[4]
        self.major_ver = d[5]
        self.minor_ver = d[6]
        self.build_ver = d[7]
        self.rxtx_period = d[8]
        self.tx_period = d[9]
        self.energy_pattern_idx = d[10]
        self.output_power = d[11]
        self.pacer_interval = d[12]

class Gw2BrgHbV1():
    def __init__(self, msg_type=0, unused0=0, seq_id=0, brg_mac=0, gw_mac=0, rx_rssi=0, unused1=0):
        self.msg_type = msg_type
        self.unused0 = unused0
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.gw_mac = gw_mac
        self.rx_rssi = rx_rssi
        self.unused1 = unused1

    def __eq__(self, other):
        if isinstance(other, Gw2BrgHbV1):
            return (
                self.msg_type == other.msg_type and
                self.brg_mac == other.brg_mac and
                self.gw_mac == other.gw_mac and
                self.rx_rssi == other.rx_rssi
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u48u8u64", self.msg_type, self.unused0, self.seq_id, self.brg_mac, self.gw_mac, self.rx_rssi, self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u48u8u64", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.unused0 = d[1]
        self.seq_id = d[2]
        self.brg_mac = d[3]
        self.gw_mac = d[4]
        self.rx_rssi = d[5]
        self.unused1 = d[6]

class Brg2GwHbV7():
    def __init__(self, msg_type=0, api_version=7, seq_id=0, brg_mac=0, non_wlt_rx_pkts_ctr=0, bad_crc_pkts_ctr=0, wlt_rx_pkts_ctr=0, wlt_tx_pkts_ctr=0, tags_ctr=0, unused=0):
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.non_wlt_rx_pkts_ctr = non_wlt_rx_pkts_ctr
        self.bad_crc_pkts_ctr = bad_crc_pkts_ctr
        self.wlt_rx_pkts_ctr = wlt_rx_pkts_ctr
        self.wlt_tx_pkts_ctr = wlt_tx_pkts_ctr
        self.tags_ctr = tags_ctr
        self.unused = unused

    def __eq__(self, other):
        if isinstance(other, Brg2GwHbV7):
            return (
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.non_wlt_rx_pkts_ctr == other.non_wlt_rx_pkts_ctr and
                self.bad_crc_pkts_ctr == other.bad_crc_pkts_ctr and
                self.wlt_rx_pkts_ctr == other.wlt_rx_pkts_ctr and
                self.wlt_tx_pkts_ctr == other.wlt_tx_pkts_ctr and
                self.tags_ctr == other.tags_ctr
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u24u24u24u16u16u16", self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.non_wlt_rx_pkts_ctr, self.bad_crc_pkts_ctr, self.wlt_rx_pkts_ctr, self.wlt_tx_pkts_ctr, self.tags_ctr, self.unused)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u24u24u24u16u16u16", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.api_version = d[1]
        self.seq_id = d[2]
        self.brg_mac = d[3]
        self.non_wlt_rx_pkts_ctr = d[4]
        self.bad_crc_pkts_ctr = d[5]
        self.wlt_rx_pkts_ctr = d[6]
        self.wlt_tx_pkts_ctr = d[7]
        self.tags_ctr = d[8]
        self.unused = d[9]

class Brg2GwHbV6():
    def __init__(self, msg_type=0, api_version=6, seq_id=0, brg_mac=0, non_wlt_rx_pkts_ctr=0, bad_crc_pkts_ctr=0, wlt_rx_pkts_ctr=0, wlt_tx_pkts_ctr=0, tags_ctr=0, unused=0):
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.non_wlt_rx_pkts_ctr = non_wlt_rx_pkts_ctr
        self.bad_crc_pkts_ctr = bad_crc_pkts_ctr
        self.wlt_rx_pkts_ctr = wlt_rx_pkts_ctr
        self.wlt_tx_pkts_ctr = wlt_tx_pkts_ctr
        self.tags_ctr = tags_ctr
        self.unused = unused

    def __eq__(self, other):
        if isinstance(other, Brg2GwHbV6):
            return (
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.non_wlt_rx_pkts_ctr == other.non_wlt_rx_pkts_ctr and
                self.bad_crc_pkts_ctr == other.bad_crc_pkts_ctr and
                self.wlt_rx_pkts_ctr == other.wlt_rx_pkts_ctr and
                self.wlt_tx_pkts_ctr == other.wlt_tx_pkts_ctr and
                self.tags_ctr == other.tags_ctr
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u24u24u24u16u16u16", self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.non_wlt_rx_pkts_ctr, self.bad_crc_pkts_ctr, self.wlt_rx_pkts_ctr, self.wlt_tx_pkts_ctr, self.tags_ctr, self.unused)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u24u24u24u16u16u16", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.api_version = d[1]
        self.seq_id = d[2]
        self.brg_mac = d[3]
        self.non_wlt_rx_pkts_ctr = d[4]
        self.bad_crc_pkts_ctr = d[5]
        self.wlt_rx_pkts_ctr = d[6]
        self.wlt_tx_pkts_ctr = d[7]
        self.tags_ctr = d[8]
        self.unused = d[9]

class Brg2GwHbV1():
    def __init__(self, msg_type=0, api_version=1, seq_id=0, gw_mac=0, brg_mac=0, sent_pkts_ctr=0, non_wlt_pkts_ctr=0, tags_ctr=0, unused1=0):
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.gw_mac = gw_mac
        self.brg_mac = brg_mac
        self.sent_pkts_ctr = sent_pkts_ctr
        self.non_wlt_pkts_ctr = non_wlt_pkts_ctr
        self.tags_ctr = tags_ctr
        self.unused1 = unused1

    def __eq__(self, other):
        if isinstance(other, Brg2GwHbV1):
            return (
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.gw_mac == other.gw_mac and
                self.brg_mac == other.brg_mac and
                self.sent_pkts_ctr == other.sent_pkts_ctr and
                self.non_wlt_pkts_ctr == other.non_wlt_pkts_ctr and
                self.tags_ctr == other.tags_ctr
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u8u48u48u16u16u16u24", self.msg_type, self.api_version, self.seq_id, self.gw_mac, self.brg_mac, self.sent_pkts_ctr, self.non_wlt_pkts_ctr, self.tags_ctr, self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u8u48u48u16u16u16u24", binascii.unhexlify(string))
        self.msg_type = d[0]
        self.api_version = d[1]
        self.seq_id = d[2]
        self.gw_mac = d[3]
        self.brg_mac = d[4]
        self.sent_pkts_ctr = d[5]
        self.non_wlt_pkts_ctr = d[6]
        self.tags_ctr = d[7]
        self.unused1 = d[8]

class SideInfo():
    def __init__(self, brg_mac=0, nfpkt=0, rssi=0, global_pacing_group=0, unused0=0, unused1=0, pkt_id=0):
        self.brg_mac = brg_mac
        self.nfpkt = nfpkt
        self.rssi = rssi
        self.global_pacing_group = global_pacing_group
        self.unused0 = unused0
        self.unused1 = unused1
        self.pkt_id = pkt_id

    def __eq__(self, other):
        if isinstance(other, SideInfo):
            return (
                self.brg_mac == other.brg_mac and
                self.nfpkt == other.nfpkt and
                self.rssi == other.rssi and
                self.global_pacing_group == other.global_pacing_group and
                self.pkt_id == other.pkt_id
            )
        return False

    def dump(self):
        string = bitstruct.pack("u48u16u8u4u4u80u32", self.brg_mac, self.nfpkt, self.rssi, self.global_pacing_group, self.unused0, self.unused1, self.pkt_id)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u48u16u8u4u4u80u32", binascii.unhexlify(string))
        self.brg_mac = d[0]
        self.nfpkt = d[1]
        self.rssi = d[2]
        self.global_pacing_group = d[3]
        self.unused0 = d[4]
        self.unused1 = d[5]
        self.pkt_id = d[6]

class SideInfoSensor():
    def __init__(self, brg_mac=0, nfpkt=0, rssi=0, global_pacing_group=0, unused0=0, sensor_mac=0, sensor_ad_type=0, sensor_uuid_msb=0, sensor_uuid_lsb=0, api_version=0, unused1=0, is_scrambled=0, is_sensor_embedded=0, is_sensor=0, pkt_id=0):
        self.brg_mac = brg_mac
        self.nfpkt = nfpkt
        self.rssi = rssi
        self.global_pacing_group = global_pacing_group
        self.unused0 = unused0
        self.sensor_mac = sensor_mac
        self.sensor_ad_type = sensor_ad_type
        self.sensor_uuid_msb = sensor_uuid_msb
        self.sensor_uuid_lsb = sensor_uuid_lsb
        self.api_version = api_version
        self.unused1 = unused1
        self.is_scrambled = is_scrambled
        self.is_sensor_embedded = is_sensor_embedded
        self.is_sensor = is_sensor
        self.pkt_id = pkt_id

    def __eq__(self, other):
        if isinstance(other, SideInfoSensor):
            return (
                self.brg_mac == other.brg_mac and
                self.nfpkt == other.nfpkt and
                self.rssi == other.rssi and
                self.global_pacing_group == other.global_pacing_group and
                self.sensor_mac == other.sensor_mac and
                self.sensor_ad_type == other.sensor_ad_type and
                self.sensor_uuid_msb == other.sensor_uuid_msb and
                self.sensor_uuid_lsb == other.sensor_uuid_lsb and
                self.api_version == other.api_version and
                self.is_scrambled == other.is_scrambled and
                self.is_sensor_embedded == other.is_sensor_embedded and
                self.is_sensor == other.is_sensor and
                self.pkt_id == other.pkt_id
            )
        return False

    def dump(self):
        string = bitstruct.pack("u48u16u8u4u4u48u8u8u8u4u1u1u1u1u32", self.brg_mac, self.nfpkt, self.rssi, self.global_pacing_group, self.unused0, self.sensor_mac, self.sensor_ad_type, self.sensor_uuid_msb, self.sensor_uuid_lsb, self.api_version, self.unused1, self.is_scrambled, self.is_sensor_embedded, self.is_sensor, self.pkt_id)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u48u16u8u4u4u48u8u8u8u4u1u1u1u1u32", binascii.unhexlify(string))
        self.brg_mac = d[0]
        self.nfpkt = d[1]
        self.rssi = d[2]
        self.global_pacing_group = d[3]
        self.unused0 = d[4]
        self.sensor_mac = d[5]
        self.sensor_ad_type = d[6]
        self.sensor_uuid_msb = d[7]
        self.sensor_uuid_lsb = d[8]
        self.api_version = d[9]
        self.unused1 = d[10]
        self.is_scrambled = d[11]
        self.is_sensor_embedded = d[12]
        self.is_sensor = d[13]
        self.pkt_id = d[14]

class ExtSensorParams():
    def __init__(self, sensor0_action=0, sensor1_action=0, sensor2_action=0, sensor3_action=0, ad_type0=0, uuid_msb0=0, uuid_lsb0=0, ad_type1=0, uuid_msb1=0, uuid_lsb1=0, ad_type2=0, uuid_msb2=0, uuid_lsb2=0, ad_type3=0, uuid_msb3=0, uuid_lsb3=0, sensor0_scramble=0, sensor1_scramble=0, sensor2_scramble=0, sensor3_scramble=0, unused1=0):
        self.sensor0_action = sensor0_action
        self.sensor1_action = sensor1_action
        self.sensor2_action = sensor2_action
        self.sensor3_action = sensor3_action
        self.ad_type0 = ad_type0
        self.uuid_msb0 = uuid_msb0
        self.uuid_lsb0 = uuid_lsb0
        self.ad_type1 = ad_type1
        self.uuid_msb1 = uuid_msb1
        self.uuid_lsb1 = uuid_lsb1
        self.ad_type2 = ad_type2
        self.uuid_msb2 = uuid_msb2
        self.uuid_lsb2 = uuid_lsb2
        self.ad_type3 = ad_type3
        self.uuid_msb3 = uuid_msb3
        self.uuid_lsb3 = uuid_lsb3
        self.sensor0_scramble = sensor0_scramble
        self.sensor1_scramble = sensor1_scramble
        self.sensor2_scramble = sensor2_scramble
        self.sensor3_scramble = sensor3_scramble
        self.unused1 = unused1

    def __eq__(self, other):
        if isinstance(other, ExtSensorParams):
            return (
                self.sensor0_action == other.sensor0_action and
                self.sensor1_action == other.sensor1_action and
                self.sensor2_action == other.sensor2_action and
                self.sensor3_action == other.sensor3_action and
                self.ad_type0 == other.ad_type0 and
                self.uuid_msb0 == other.uuid_msb0 and
                self.uuid_lsb0 == other.uuid_lsb0 and
                self.ad_type1 == other.ad_type1 and
                self.uuid_msb1 == other.uuid_msb1 and
                self.uuid_lsb1 == other.uuid_lsb1 and
                self.ad_type2 == other.ad_type2 and
                self.uuid_msb2 == other.uuid_msb2 and
                self.uuid_lsb2 == other.uuid_lsb2 and
                self.ad_type3 == other.ad_type3 and
                self.uuid_msb3 == other.uuid_msb3 and
                self.uuid_lsb3 == other.uuid_lsb3 and
                self.sensor0_scramble == other.sensor0_scramble and
                self.sensor1_scramble == other.sensor1_scramble and
                self.sensor2_scramble == other.sensor2_scramble and
                self.sensor3_scramble == other.sensor3_scramble
            )
        return False

    def dump(self):
        string = bitstruct.pack("u2u2u2u2u8u8u8u8u8u8u8u8u8u8u8u8u1u1u1u1u4", self.sensor0_action, self.sensor1_action, self.sensor2_action, self.sensor3_action, self.ad_type0, self.uuid_msb0, self.uuid_lsb0, self.ad_type1, self.uuid_msb1, self.uuid_lsb1, self.ad_type2, self.uuid_msb2, self.uuid_lsb2, self.ad_type3, self.uuid_msb3, self.uuid_lsb3, self.sensor0_scramble, self.sensor1_scramble, self.sensor2_scramble, self.sensor3_scramble, self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u2u2u2u2u8u8u8u8u8u8u8u8u8u8u8u8u1u1u1u1u4", binascii.unhexlify(string))
        self.sensor0_action = d[0]
        self.sensor1_action = d[1]
        self.sensor2_action = d[2]
        self.sensor3_action = d[3]
        self.ad_type0 = d[4]
        self.uuid_msb0 = d[5]
        self.uuid_lsb0 = d[6]
        self.ad_type1 = d[7]
        self.uuid_msb1 = d[8]
        self.uuid_lsb1 = d[9]
        self.ad_type2 = d[10]
        self.uuid_msb2 = d[11]
        self.uuid_lsb2 = d[12]
        self.ad_type3 = d[13]
        self.uuid_msb3 = d[14]
        self.uuid_lsb3 = d[15]
        self.sensor0_scramble = d[16]
        self.sensor1_scramble = d[17]
        self.sensor2_scramble = d[18]
        self.sensor3_scramble = d[19]
        self.unused1 = d[20]

class PktTypesMask():
    def __init__(self, unused=0, mask_enable=0, p3_pacing=0, p2_pacing=0, p1_pacing=0, p0_pacing=0):
        self.unused = unused
        self.mask_enable = mask_enable
        self.p3_pacing = p3_pacing
        self.p2_pacing = p2_pacing
        self.p1_pacing = p1_pacing
        self.p0_pacing = p0_pacing

    def __eq__(self, other):
        if isinstance(other, PktTypesMask):
            return (
                self.mask_enable == other.mask_enable and
                self.p3_pacing == other.p3_pacing and
                self.p2_pacing == other.p2_pacing and
                self.p1_pacing == other.p1_pacing and
                self.p0_pacing == other.p0_pacing
            )
        return False

    def dump(self):
        string = bitstruct.pack("u3u1u1u1u1u1", self.unused, self.mask_enable, self.p3_pacing, self.p2_pacing, self.p1_pacing, self.p0_pacing)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u3u1u1u1u1u1", binascii.unhexlify(string))
        self.unused = d[0]
        self.mask_enable = d[1]
        self.p3_pacing = d[2]
        self.p2_pacing = d[3]
        self.p1_pacing = d[4]
        self.p0_pacing = d[5]

class PwrMgmt():
    def __init__(self, leds_on=PWR_MGMT_DEFAULTS_LEDS_ON, keep_alive_scan=PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN, keep_alive_period=PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD, on_duration=PWR_MGMT_DEFAULTS_ON_DURATION, sleep_duration=PWR_MGMT_DEFAULTS_SLEEP_DURATION, unused=0):
        self.leds_on = leds_on
        self.keep_alive_scan = keep_alive_scan # 10 [msec] resolution
        self.keep_alive_period = keep_alive_period # 5 [sec] resolution
        self.on_duration = on_duration # 30 [sec] resolution
        self.sleep_duration = sleep_duration # 60 [sec] resolution
        self.unused = unused

    def __eq__(self, other):
        if isinstance(other, PwrMgmt):
            return (
                self.leds_on == other.leds_on and
                self.keep_alive_scan == other.keep_alive_scan and
                self.keep_alive_period == other.keep_alive_period and
                self.on_duration == other.on_duration and
                self.sleep_duration == other.sleep_duration
            )
        return False

    def dump(self):
        string = bitstruct.pack("u1u6u5u7u11u2", self.leds_on, self.keep_alive_scan, self.keep_alive_period, self.on_duration, self.sleep_duration, self.unused)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u1u6u5u7u11u2", binascii.unhexlify(string))
        self.leds_on = d[0]
        self.keep_alive_scan = d[1]
        self.keep_alive_period = d[2]
        self.on_duration = d[3]
        self.sleep_duration = d[4]
        self.unused = d[5]

class Lis2Dw12AccelCfg():
    def __init__(self, api_version=LIS2DW12_ACCEL_DEFAULTS_CFG_PACKET_VERSION, state_threshold=LIS2DW12_ACCEL_DEFAULTS_STATE_THRESHOLD, wake_up_duration=LIS2DW12_ACCEL_DEFAULTS_WAKE_UP_DURATION, sleep_duration=LIS2DW12_ACCEL_DEFAULTS_SLEEP_DURATION, unused=0):
        self.api_version = api_version
        self.state_threshold = state_threshold # 31.25 [mg] resolution
        self.wake_up_duration = wake_up_duration # 3 [sec] resolution
        self.sleep_duration = sleep_duration # 5 [sec] resolution
        self.unused = unused

    def __eq__(self, other):
        if isinstance(other, Lis2Dw12AccelCfg):
            return (
                self.api_version == other.api_version and
                self.state_threshold == other.state_threshold and
                self.wake_up_duration == other.wake_up_duration and
                self.sleep_duration == other.sleep_duration
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u6u6u4u8", self.api_version, ((self.state_threshold-0)//31.25), ((self.wake_up_duration-0.03)//3), ((self.sleep_duration-0.16)//5.12), self.unused)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u6u6u4u8", binascii.unhexlify(string))
        self.api_version = d[0]
        self.state_threshold = ((d[1]*31.25)+0)
        self.wake_up_duration = ((d[2]*3)+0.03)
        self.sleep_duration = ((d[3]*5.12)+0.16)
        self.unused = d[4]

class GetModuleParams():
    def __init__(self, interface=0, datapath=0, energy2400=0, energy_sub1g=0, calibration=0, pwr_mgmt=0, sensors=0, periph=0, unused0=0):
        self.interface = interface
        self.datapath = datapath
        self.energy2400 = energy2400
        self.energy_sub1g = energy_sub1g
        self.calibration = calibration
        self.pwr_mgmt = pwr_mgmt
        self.sensors = sensors
        self.periph = periph
        self.unused0 = unused0

    def __eq__(self, other):
        if isinstance(other, GetModuleParams):
            return (
                self.interface == other.interface and
                self.datapath == other.datapath and
                self.energy2400 == other.energy2400 and
                self.energy_sub1g == other.energy_sub1g and
                self.calibration == other.calibration and
                self.pwr_mgmt == other.pwr_mgmt and
                self.sensors == other.sensors and
                self.periph == other.periph
            )
        return False

    def dump(self):
        string = bitstruct.pack("u1u1u1u1u1u1u1u1u104", self.interface, self.datapath, self.energy2400, self.energy_sub1g, self.calibration, self.pwr_mgmt, self.sensors, self.periph, self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u1u1u1u1u1u1u1u1u104", binascii.unhexlify(string))
        self.interface = d[0]
        self.datapath = d[1]
        self.energy2400 = d[2]
        self.energy_sub1g = d[3]
        self.calibration = d[4]
        self.pwr_mgmt = d[5]
        self.sensors = d[6]
        self.periph = d[7]
        self.unused0 = d[8]

class ModuleIfV7():
    def __init__(self, module_type=MODULE_IF, msg_type=0, api_version=API_VERSION_V7, seq_id=0, brg_mac=0, board_type=0, bl_version=0, major_ver=0, minor_ver=0, patch_ver=0, sup_cap_glob=0, sup_cap_datapath=0, sup_cap_energy2400=0, sup_cap_energy_sub1g=0, sup_cap_calibration=0, sup_cap_pwr_mgmt=0, sup_cap_sensors=0, sup_cap_periph=0, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.board_type = board_type
        self.bl_version = bl_version
        self.major_ver = major_ver
        self.minor_ver = minor_ver
        self.patch_ver = patch_ver
        self.sup_cap_glob = sup_cap_glob
        self.sup_cap_datapath = sup_cap_datapath
        self.sup_cap_energy2400 = sup_cap_energy2400
        self.sup_cap_energy_sub1g = sup_cap_energy_sub1g
        self.sup_cap_calibration = sup_cap_calibration
        self.sup_cap_pwr_mgmt = sup_cap_pwr_mgmt
        self.sup_cap_sensors = sup_cap_sensors
        self.sup_cap_periph = sup_cap_periph
        self.unused0 = unused0

    def __eq__(self, other):
        if isinstance(other, ModuleIfV7):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.board_type == other.board_type and
                self.bl_version == other.bl_version and
                self.major_ver == other.major_ver and
                self.minor_ver == other.minor_ver and
                self.patch_ver == other.patch_ver and
                self.sup_cap_glob == other.sup_cap_glob and
                self.sup_cap_datapath == other.sup_cap_datapath and
                self.sup_cap_energy2400 == other.sup_cap_energy2400 and
                self.sup_cap_energy_sub1g == other.sup_cap_energy_sub1g and
                self.sup_cap_calibration == other.sup_cap_calibration and
                self.sup_cap_pwr_mgmt == other.sup_cap_pwr_mgmt and
                self.sup_cap_sensors == other.sup_cap_sensors and
                self.sup_cap_periph == other.sup_cap_periph
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u8u8u1u1u1u1u1u1u1u1u72", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.board_type, self.bl_version, self.major_ver, self.minor_ver, self.patch_ver, self.sup_cap_glob, self.sup_cap_datapath, self.sup_cap_energy2400, self.sup_cap_energy_sub1g, self.sup_cap_calibration, self.sup_cap_pwr_mgmt, self.sup_cap_sensors, self.sup_cap_periph, self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u8u8u1u1u1u1u1u1u1u1u72", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.board_type = d[5]
        self.bl_version = d[6]
        self.major_ver = d[7]
        self.minor_ver = d[8]
        self.patch_ver = d[9]
        self.sup_cap_glob = d[10]
        self.sup_cap_datapath = d[11]
        self.sup_cap_energy2400 = d[12]
        self.sup_cap_energy_sub1g = d[13]
        self.sup_cap_calibration = d[14]
        self.sup_cap_pwr_mgmt = d[15]
        self.sup_cap_sensors = d[16]
        self.sup_cap_periph = d[17]
        self.unused0 = d[18]

class ModuleEnergy2400V7():
    def __init__(self, module_type=MODULE_ENERGY_2400, msg_type=0, api_version=API_VERSION_V7, seq_id=0, brg_mac=0, rxtx_period=0, tx_period=0, energy_pattern=0, output_power=0, tx_probability=BRG_DEFAULT_TX_PROB, unused0=0, unused1=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.rxtx_period = rxtx_period
        self.tx_period = tx_period
        self.energy_pattern = energy_pattern
        self.output_power = output_power
        self.tx_probability = tx_probability
        self.unused0 = unused0
        self.unused1 = unused1

    def __eq__(self, other):
        if isinstance(other, ModuleEnergy2400V7):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.rxtx_period == other.rxtx_period and
                self.tx_period == other.tx_period and
                self.energy_pattern == other.energy_pattern and
                self.output_power == other.output_power and
                self.tx_probability == other.tx_probability
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8s8u3u5u80", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.rxtx_period, self.tx_period, self.energy_pattern, self.output_power, ((self.tx_probability-30)//10), self.unused0, self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8s8u3u5u80", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.rxtx_period = d[5]
        self.tx_period = d[6]
        self.energy_pattern = d[7]
        self.output_power = d[8]
        self.tx_probability = ((d[9]*10)+30)
        self.unused0 = d[10]
        self.unused1 = d[11]

MODULE_ENERGY_SUB1G_V7_OUTPUT_POWER_ENC = {SUB1G_OUTPUT_POWER_14:SUB1G_OUTPUT_POWER_PROFILE_14, SUB1G_OUTPUT_POWER_17:SUB1G_OUTPUT_POWER_PROFILE_17, SUB1G_OUTPUT_POWER_20:SUB1G_OUTPUT_POWER_PROFILE_20, SUB1G_OUTPUT_POWER_23:SUB1G_OUTPUT_POWER_PROFILE_23, SUB1G_OUTPUT_POWER_26:SUB1G_OUTPUT_POWER_PROFILE_26, SUB1G_OUTPUT_POWER_29:SUB1G_OUTPUT_POWER_PROFILE_29, SUB1G_OUTPUT_POWER_32:SUB1G_OUTPUT_POWER_PROFILE_32}
MODULE_ENERGY_SUB1G_V7_OUTPUT_POWER_DEC = {SUB1G_OUTPUT_POWER_PROFILE_14:SUB1G_OUTPUT_POWER_14, SUB1G_OUTPUT_POWER_PROFILE_17:SUB1G_OUTPUT_POWER_17, SUB1G_OUTPUT_POWER_PROFILE_20:SUB1G_OUTPUT_POWER_20, SUB1G_OUTPUT_POWER_PROFILE_23:SUB1G_OUTPUT_POWER_23, SUB1G_OUTPUT_POWER_PROFILE_26:SUB1G_OUTPUT_POWER_26, SUB1G_OUTPUT_POWER_PROFILE_29:SUB1G_OUTPUT_POWER_29, SUB1G_OUTPUT_POWER_PROFILE_32:SUB1G_OUTPUT_POWER_32}
class ModuleEnergySub1GV7():
    def __init__(self, module_type=0, msg_type=0, api_version=API_VERSION_V7, seq_id=0, brg_mac=0, output_power=BRG_DEFAULT_OUTPUT_POWER_SUB_1_GHZ, freq_profile=SUB1G_FREQ_PROFILE_915000, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.output_power = output_power
        self.freq_profile = freq_profile
        self.unused0 = unused0

    def __eq__(self, other):
        if isinstance(other, ModuleEnergySub1GV7):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.output_power == other.output_power and
                self.freq_profile == other.freq_profile
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u104", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, MODULE_ENERGY_SUB1G_V7_OUTPUT_POWER_ENC[self.output_power], self.freq_profile, self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u104", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.output_power = MODULE_ENERGY_SUB1G_V7_OUTPUT_POWER_DEC[d[5]]
        self.freq_profile = d[6]
        self.unused0 = d[7]

class ModulePwrMgmtV7():
    def __init__(self, module_type=MODULE_PWR_MGMT, msg_type=0, api_version=API_VERSION_V7, seq_id=0, brg_mac=0, static_leds_on=PWR_MGMT_DEFAULTS_LEDS_ON, static_keep_alive_period=PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD, static_keep_alive_scan=PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN, static_on_duration=PWR_MGMT_DEFAULTS_ON_DURATION, static_sleep_duration=PWR_MGMT_DEFAULTS_SLEEP_DURATION, dynamic_leds_on=PWR_MGMT_DEFAULTS_LEDS_ON, dynamic_keep_alive_period=PWR_MGMT_DEFAULTS_KEEP_ALIVE_PERIOD, dynamic_keep_alive_scan=PWR_MGMT_DEFAULTS_KEEP_ALIVE_SCAN, dynamic_on_duration=PWR_MGMT_DEFAULTS_ON_DURATION, dynamic_sleep_duration=PWR_MGMT_DEFAULTS_SLEEP_DURATION, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.static_leds_on = static_leds_on
        self.static_keep_alive_period = static_keep_alive_period # 5sec resolution
        self.static_keep_alive_scan = static_keep_alive_scan # 10msec resolution
        self.static_on_duration = static_on_duration # 30sec resolution
        self.static_sleep_duration = static_sleep_duration # 60sec resolution
        self.dynamic_leds_on = dynamic_leds_on
        self.dynamic_keep_alive_period = dynamic_keep_alive_period # 5sec resolution
        self.dynamic_keep_alive_scan = dynamic_keep_alive_scan # 10msec resolution
        self.dynamic_on_duration = dynamic_on_duration # 30sec resolution
        self.dynamic_sleep_duration = dynamic_sleep_duration # 60sec resolution
        self.unused0 = unused0

    def __eq__(self, other):
        if isinstance(other, ModulePwrMgmtV7):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.static_leds_on == other.static_leds_on and
                self.static_keep_alive_period == other.static_keep_alive_period and
                self.static_keep_alive_scan == other.static_keep_alive_scan and
                self.static_on_duration == other.static_on_duration and
                self.static_sleep_duration == other.static_sleep_duration and
                self.dynamic_leds_on == other.dynamic_leds_on and
                self.dynamic_keep_alive_period == other.dynamic_keep_alive_period and
                self.dynamic_keep_alive_scan == other.dynamic_keep_alive_scan and
                self.dynamic_on_duration == other.dynamic_on_duration and
                self.dynamic_sleep_duration == other.dynamic_sleep_duration
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u8u8u8u8u16u8u8u8u8u16u24", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.static_leds_on, ((self.static_keep_alive_period-0)//5), ((self.static_keep_alive_scan-0)//10), ((self.static_on_duration-0)//30), ((self.static_sleep_duration-0)//60), self.dynamic_leds_on, ((self.dynamic_keep_alive_period-0)//5), ((self.dynamic_keep_alive_scan-0)//10), ((self.dynamic_on_duration-0)//30), ((self.dynamic_sleep_duration-0)//60), self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u8u8u8u8u16u8u8u8u8u16u24", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.static_leds_on = d[5]
        self.static_keep_alive_period = ((d[6]*5)+0)
        self.static_keep_alive_scan = ((d[7]*10)+0)
        self.static_on_duration = ((d[8]*30)+0)
        self.static_sleep_duration = ((d[9]*60)+0)
        self.dynamic_leds_on = d[10]
        self.dynamic_keep_alive_period = ((d[11]*5)+0)
        self.dynamic_keep_alive_scan = ((d[12]*10)+0)
        self.dynamic_on_duration = ((d[13]*30)+0)
        self.dynamic_sleep_duration = ((d[14]*60)+0)
        self.unused0 = d[15]

class ModuleCalibrationV7():
    def __init__(self, module_type=MODULE_CALIBRATION, msg_type=0, api_version=0, seq_id=0, brg_mac=0, unused0=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.unused0 = unused0

    def __eq__(self, other):
        if isinstance(other, ModuleCalibrationV7):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u120", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u120", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.unused0 = d[5]

class ModuleDatapathV7():
    def __init__(self, module_type=MODULE_DATAPATH, msg_type=0, api_version=0, seq_id=0, brg_mac=0, global_pacing_group=BRG_DEFAULT_GLOBAL_PACING_GROUP, unused0=0, pacer_interval=BRG_DEFAULT_PACER_INTERVAL, pkt_types_mask=BRG_DEFAULT_PKT_TYPES_MASK, tx_repetition=BRG_DEFAULT_TX_REPETITION, unused1=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.global_pacing_group = global_pacing_group
        self.unused0 = unused0
        self.pacer_interval = pacer_interval
        self.pkt_types_mask = pkt_types_mask
        self.tx_repetition = tx_repetition
        self.unused1 = unused1

    def __eq__(self, other):
        if isinstance(other, ModuleDatapathV7):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.global_pacing_group == other.global_pacing_group and
                self.pacer_interval == other.pacer_interval and
                self.pkt_types_mask == other.pkt_types_mask and
                self.tx_repetition == other.tx_repetition
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u4u4u16u5u3u88", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.global_pacing_group, self.unused0, self.pacer_interval, self.pkt_types_mask, self.tx_repetition, self.unused1)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u4u4u16u5u3u88", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.global_pacing_group = d[5]
        self.unused0 = d[6]
        self.pacer_interval = d[7]
        self.pkt_types_mask = d[8]
        self.tx_repetition = d[9]
        self.unused1 = d[10]

class ModulePeriphV7():
    def __init__(self, module_type=MODULE_PERIPH, msg_type=0, api_version=API_VERSION_V7, seq_id=0, brg_mac=0, peripherals_tlv_params=0):
        self.module_type = module_type
        self.msg_type = msg_type
        self.api_version = api_version
        self.seq_id = seq_id
        self.brg_mac = brg_mac
        self.peripherals_tlv_params = peripherals_tlv_params

    def __eq__(self, other):
        if isinstance(other, ModulePeriphV7):
            return (
                self.module_type == other.module_type and
                self.msg_type == other.msg_type and
                self.api_version == other.api_version and
                self.brg_mac == other.brg_mac and
                self.peripherals_tlv_params == other.peripherals_tlv_params
            )
        return False

    def dump(self):
        string = bitstruct.pack("u4u4u8u8u48u120", self.module_type, self.msg_type, self.api_version, self.seq_id, self.brg_mac, self.peripherals_tlv_params)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u4u4u8u8u48u120", binascii.unhexlify(string))
        self.module_type = d[0]
        self.msg_type = d[1]
        self.api_version = d[2]
        self.seq_id = d[3]
        self.brg_mac = d[4]
        self.peripherals_tlv_params = d[5]

class Lis2Dw12AccelData():
    def __init__(self, api_version=0, state=0, temperature=0, unused0=0):
        self.api_version = api_version
        self.state = state
        self.temperature = temperature
        self.unused0 = unused0

    def __eq__(self, other):
        if isinstance(other, Lis2Dw12AccelData):
            return (
                self.api_version == other.api_version and
                self.state == other.state and
                self.temperature == other.temperature
            )
        return False

    def dump(self):
        string = bitstruct.pack("u8u8u16u184", self.api_version, self.state, self.temperature, self.unused0)
        return string.hex().upper()

    def set(self, string):
        d = bitstruct.unpack("u8u8u16u184", binascii.unhexlify(string))
        self.api_version = d[0]
        self.state = d[1]
        self.temperature = d[2]
        self.unused0 = d[3]

MODULES_LIST = [ModuleIfV7, ModuleEnergy2400V7, ModuleEnergySub1GV7, ModulePwrMgmtV7, ModuleCalibrationV7, ModuleDatapathV7, ModulePeriphV7]
WLT_PKT_TYPES = [ActionV7, Gw2BrgCfgV7, Brg2GwCfgV7, Brg2GwCfgV6, Brg2GwCfgV5, Brg2GwCfgV2, Brg2GwHbV7, Brg2GwHbV6, Brg2GwHbV1, SideInfo, SideInfoSensor, ModuleIfV7, ModuleEnergy2400V7, ModuleEnergySub1GV7, ModulePwrMgmtV7, ModuleCalibrationV7, ModuleDatapathV7, ModulePeriphV7]