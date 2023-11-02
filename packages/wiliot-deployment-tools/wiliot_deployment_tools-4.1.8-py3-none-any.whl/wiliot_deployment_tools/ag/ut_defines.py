# Files
UT_MQTT_LOG_FILE = "ut_mqtt_log.json"

# GW defines
GW_ID =                         "gatewayId"
ADDITIONAL =                    "additional"
REPORTED_CONF =                 "reportedConf"
GW_CONF =                       "gatewayConf"
GW_NAME =                       "gatewayName"
GW_API_VERSION =                "apiVersion"
LAT =                           "lat"
LNG =                           "lng"


GW_DATA_MODE =                  "gwDataMode"
TAGS_AND_BRGS =                 "Tags & Bridges"
TAGS_ONLY =                     "Tags only"
BRGS_ONLY_38 =                  "Bridges only (ch38)"
BRGS_ONLY_39 =                  "Bridges only (ch39)"
HIBERNATE =                     "Hibernate"

BLE_WIFI =                      "ble_wifi"
BLE_LAN =                       "ble_lan"

GW_ENERGY_PATTERN =             "energizingPattern"
VERSION =                       "version"
WIFI_VERSION =                  "interfaceChipSwVersion"
BLE_VERSION =                   "bleChipSwVersion"
DATA_COUPLING =                 "dataCoupling"
GW_MGMT_MODE =                  "gwMgmtMode"
GW_MODE =                       "gwMode"
ACTIVE =                        "active"
TRANSPARENT =                   "transparent"
PROD =                          "prod"

GET_INFO_ACTION =               "getGwInfo"
REBOOT_GW_ACTION =              "rebootGw"
LOG_PERIOD_ACTION =             "LogPeriodSet"
GET_LOGS =                      "getLogs"
GW_INFO =                       "gatewayInfo"
GW_LOGS =                       "gatewayLogs"
GW_ACTION_ACK =                 "ReceivedAction"
GW_LATITUDE =                   "Latitude"
GW_LONGITUDE =                  "Longitude"
GW_MEL_MODULE_ACK =             "ReceivedMel"
GW_LOG_PERIOD =                 30

# Thin gw defines
THIN_GW_PROTOCOL_VERSION =      "protocolVersion"
THIN_GW_ACTION =                "action"
THIN_GW_GW_ID =                 "gatewayId"
TX_PKT =                        "txPacket"
TX_MAX_DURATION_MS =            "txMaxDurationMs"
TX_MAX_RETRIES =                "txMaxRetries"
TRANPARENT_PKT_LEN =            31 * 2
COUPLED_DATA_PKT_LEN =          29 * 2 # No 1E16

# Bridge defines
BRIDGE_ID =                     "bridgeId"
BRG_STATUS =                    "bridgeStatus"
BRG_STATS =                     "bridgeStats"
BRG_CONFIG =                    "bridgeConfig"
BRG_ACTION =                    "bridgeAction"
BRG_REBOOT =                    "rebootBridge"
BRG_BLINK =                     "blinkBridgeLed"
BRG_ACK_STR =                   GW_ACTION_ACK+"="

OTA_ENABLED =                   "otaUpgradeEnabled"
TX_PROBABILITY =                "txProbability"
TX_REPETITION =                 "txRepetition"
GLOBAL_PACING_GROUP =           "globalPacingGroup"
BOARD_TYPE =                    "boardType"
OUTPUT_POWER_SUB1G =            "sub1GhzOutputPower"
SUB1GHZ_FREQ =                  "sub1GhzFrequency"

FANSTEL =                       "FANSTEL"
MINEW =                         "MINEW"
ENERGOUS =                      "ENERGOUS"
MOKO =                          "MOKO"
UN_INIT =                       "UN_INIT"
DB =                            "DUAL_BAND"
SB =                            "SINGLE_BAND"
BOARD_TYPES_PROFILE_DICT = {0:"FANSTEL_SINGLE_BAND", 1:"FANSTEL_DUAL_BAND", 2:"MINEW_SINGLE_BAND", 3:"MINEW_DUAL_BAND", 4:"ENERGOUS_DUAL_BAND", 0xFFFFFFFF:"UN_INIT"}

# Tags defines
EXT_ID =                        "externalId"
UNKNOWN =                       "unknown"

# Common defines
PACKETS =                       "packets"
TIMESTAMP =                     "timestamp"
ID =                            "id"
CONFIG =                        "config"
ACTION =                        "action"
PAYLOAD =                       "payload"

WLT_SERVER =                    "wiliotServer"
PACER_INTERVAL =                "pacerInterval"
PKT_TYPES_MASK =                "packetTypesMask"
RX_TX_PERIOD =                  "rxTxPeriodMs"
TX_PERIOD =                     "txPeriodMs"
ENERGY_PATTERN =                "energyPattern"
OUTPUT_POWER_2_4 =              "2.4GhzOutputPower"
NFPKT =                         "nfpkt"
RSSI =                          "rssi"
USE_STAT_LOC =                  "useStaticLocation"

# Speedtest
SPEEDTEST_LATENCY =             "SpeedTestLatency"
SPEEDTEST_STRESS =              "SpeedTestStress"
LATENCY_STR =                   "SpeedTestLatency MQTT! Recived"
STRESS_STR =                    "SpeedTestStress MQTT! finished sending"
SPEEDTESTS =                    {SPEEDTEST_LATENCY:LATENCY_STR, SPEEDTEST_STRESS:STRESS_STR}
SPEEDTEST_TIME_LIMIT =          GW_LOG_PERIOD + 20

# External Sensors
IS_SENSOR =                      "isSensor"
IS_EMBEDDED =                    "isEmbedded"
IS_SCRAMBLED =                   "isScrambled"
SENSOR_UUID =                    "sensorServiceId"
SENSOR_ID =                      "sensorId"

ACTION_LONG_TIMEOUT =            120
ACTION_SHORT_TIMEOUT =           5

# Versions
VERSIONS = {
    "1.5.0" : {WIFI_VERSION: "3.5.32", BLE_VERSION: "3.7.25"},
    "1.5.2" : {WIFI_VERSION: "3.5.132", BLE_VERSION: "3.7.25"},
    "1.6.1" : {WIFI_VERSION: "3.5.51", BLE_VERSION: "3.8.18"},
    "1.7.0" : {WIFI_VERSION: "3.9.8", BLE_VERSION: "3.9.24"},
    "1.7.1" : {WIFI_VERSION: "3.10.6", BLE_VERSION: "3.10.13"},
    "1.8.0" : {WIFI_VERSION: "3.11.36", BLE_VERSION: "3.11.40"},
    "1.8.2" : {WIFI_VERSION: "3.11.36", BLE_VERSION: "3.11.42"},
    "1.9.0" : {WIFI_VERSION: "3.12.10", BLE_VERSION: "3.12.36"},
    "1.10.1" : {WIFI_VERSION: "3.13.29", BLE_VERSION: "3.13.25"},
    "3.14.0" : {WIFI_VERSION: "3.14.33", BLE_VERSION: "3.14.64"}
}

# Tests defines
DEFAULT_GW_FIELD_UPDATE_TIMEOUT =   10
DEFAULT_BRG_FIELD_UPDATE_TIMEOUT =  10
HB_PERIOD =                         30
HB_SCAN_TIMEOUT =                   HB_PERIOD + 5
GW_STAT_SCAN_TIMEOUT =              65
BRG_STAT_SCAN_TIMEOUT =             65
BRG_OTA_UPDATE_TIMEOUT =            210
BRG_GLOBAL_PACING_SCAN_TIME =       180
GW_VERSION_UPDATE_DATA_SCAN_TIME =  180
GW_LATITUDE_DEFAULT =               33.0222
GW_LONGITUDE_DEFAULT =              -117.0839
GW_API_VER_DEFAULT =                "200"

# Internal python ut defines - used only in ut
PACER_INTERVAL_THRESHOLD =                          0.90
GLOBAL_PACING_GROUP_THRESHOLD =                     0.70
TX_REPETITION_THRESHOLD =                           0.50
NO_RESPONSE =                                       "NO_RESPONSE"
DONE =                                              "DONE"
TEST_SUCCESS =                                      ":)"
NONE_WILIOT_PKT_CTR =                               "beaconCount"
BASIC_GW_TEST =                                     "basic_gw_test"
MULTI_BRG_TEST =                                    "multibrg_brg_test"
BASIC_BRG_TEST =                                    "basic_brg_test"
ACTION_BRG_TEST =                                   "action_brg_test"
MGMT_PKT =                                          "mgmt_pkt"
SIDE_INFO_PKT =                                     "side_info_pkt"
DECODED_DATA =                                      "decoded_data"
PACKETS_ECHO_OFF =                                  0x10

# Non Default defines
BRG_NON_DEFAULT_RXTX_PERIOD =                       25
BRG_NON_DEFAULT_TX_PERIOD =                         8
BRG_NON_DEFAULT_OUTPUT_POWER_SUB1G =                26
BRG_NON_DEFAULT_PWR_MGMT_KEEP_ALIVE_SCAN =          0
BRG_NON_DEFAULT_TX_REPETITION = 2

LIS2DW12_ACCEL_NON_DEFAULT_STATE_THRESHOLD =        95
LIS2DW12_ACCEL_NON_DEFAULT_WAKE_UP_DURATION =       121
LIS2DW12_ACCEL_NON_DEFAULT_SLEEP_DURATION =         36

# ---------------------------------------------------RTSA defines---------------------------------------------------
# common defines
TRACE_LOG_FILE_NAME =                   "TRACELOG"
TRACE_LOG_FILE_PATH =                   "C:/SignalVu-PC Files/" + TRACE_LOG_FILE_NAME + ".TOV"

# freq defines
FREQ_2_4_GHZ =                          {'37':2.402, '38':2.426, '39':2.480}
FREQ_SUB1G_MHZ =                        {'865_7':865.700, '915':915.000, '916_3':916.300, '917_5':917.500, '918':918.000, '919_1':919.100}

# SignalVu API commands defines
TRACE_DETECTION =                       {'average':'AVERage', 'positive':'POSitive', 'negative':'NEGative', 'positive-negative':'POSNegative', 'sample':'SAMPle'}
MAX_TRACE_POINTS =                      {'1K':'ONEK', '10K':'TENK', '100K':'HUNDredk', 'never_decimate':'NEVerdecimate' }

# default values
DEFAULT_LENGTH_MS =                     30
DEFAULT_TIME_PER_DIVISION_SEC =         5
DEFAULT_RX_TX_PERIOD_SEC =              0.015
BEACON_MIN_LENGTH_SEC =                 375e-6
BEACON_MAX_LENGTH_SEC =                 500e-6
ENERGIZING_TIME_THRESHOLD =             0.3
BEACON_POWER_THRESHOLD =                0.9
BEACON_POWER_CURVE_38 =                 0.7
BEACON_POWER_CURVE_39 =                 0.625
DEFAULT_SPAN_MHZ =                      5

# test times
FREQ_BEACONS_ANALYSIS_TIME_DELTA =      10

# structured energizing patterns information
class energizingPattern:
    def __init__(self, ble_calibration_beacons = [], ble_energy = {}, ble_post_energy_beacons = [], sub1G_energy = False, info = ""):
        self.ble_calibration_beacons = ble_calibration_beacons
        self.ble_energy = ble_energy
        self.ble_post_energy_beacons = ble_post_energy_beacons
        self.sub1G_energy = sub1G_energy
        self.info = info

EP_INFO = {
        '17' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']]),
        '18' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['39'] : 1.0}),
        '20' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['37'] : 0.2, FREQ_2_4_GHZ['39'] : 0.8}),
        '24' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['37'] : 1.0}),
        '25' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['38'] : 1.0}),
        '26' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={2.454 : 1.0}),
        '27' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39'], FREQ_2_4_GHZ['39']]),
        '29' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['38'] : 0.3333, 2.454 : 0.3333, FREQ_2_4_GHZ['39'] : 0.3333}),
        '36' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'],FREQ_2_4_GHZ['38'],FREQ_2_4_GHZ['39']], info="idle"),
        '37' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], 2.415, FREQ_2_4_GHZ['39'], 2.441, 2.428, 2.454, 2.467], ble_energy={2.450 : 1.0}, info="euro"),
        '50' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], sub1G_energy=True),
        '51' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['39'] : 1.0}, sub1G_energy=True),
        '52' : energizingPattern(sub1G_energy=True),
        '55' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['37'] : 1.0}, sub1G_energy=True),
        '56' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={FREQ_2_4_GHZ['38'] : 1.0}, sub1G_energy=True),
        '57' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], FREQ_2_4_GHZ['38'], FREQ_2_4_GHZ['39']], ble_energy={2.454 : 1.0}, sub1G_energy=True),
        '61' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], 2.415, FREQ_2_4_GHZ['39'], 2.441, 2.428, 2.454, 2.467], sub1G_energy=True, info="euro"),
        '62' : energizingPattern(ble_calibration_beacons=[FREQ_2_4_GHZ['37'], 2.415, FREQ_2_4_GHZ['39'], 2.441, 2.428, 2.454, 2.467], ble_energy={2.475 : 1.0}, sub1G_energy=True, info="euro"),
        '99' : energizingPattern(ble_calibration_beacons=[i/1000.0 for i in range(2402, 2481, 2)])
                }

EP_FREQ_BREAKDOWN_COUNTER_SETUP = {
    2.402 : {'beacons':0, 'energy_in_ms': 0.0},
    2.426 : {'beacons':0, 'energy_in_ms': 0.0},
    2.480 : {'beacons':0, 'energy_in_ms': 0.0},
    2.403 : {'beacons':0, 'energy_in_ms': 0.0},
    2.427 : {'beacons':0, 'energy_in_ms': 0.0},
    2.483 : {'beacons':0, 'energy_in_ms': 0.0},
    2.454 : {'beacons':0, 'energy_in_ms': 0.0},
    2.481 : {'beacons':0, 'energy_in_ms': 0.0},
    2.415 : {'beacons':0, 'energy_in_ms': 0.0},
    2.441 : {'beacons':0, 'energy_in_ms': 0.0},
    2.428 : {'beacons':0, 'energy_in_ms': 0.0},
    2.467 : {'beacons':0, 'energy_in_ms': 0.0},
    2.475 : {'beacons':0, 'energy_in_ms': 0.0},
    0.8657 : {'beacons':0, 'energy_in_ms': 0.0},
    0.915 : {'beacons':0, 'energy_in_ms': 0.0},
    0.9163 : {'beacons':0, 'energy_in_ms': 0.0},
    0.9175 : {'beacons':0, 'energy_in_ms': 0.0},
    0.918 : {'beacons':0, 'energy_in_ms': 0.0},
    0.9191 : {'beacons':0, 'energy_in_ms': 0.0}
}