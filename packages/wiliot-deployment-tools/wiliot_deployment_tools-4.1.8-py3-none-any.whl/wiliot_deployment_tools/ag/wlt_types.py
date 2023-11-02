from wiliot_deployment_tools.ag.ut_defines import *
from wiliot_deployment_tools.ag.wlt_types_ag import *
class WltPkt():
    supported_pkt_types = WLT_PKT_TYPES

    def __init__(self, hdr=Hdr(), generic=None, pkt=None):
        self.hdr = hdr
        self.generic = generic
        self.pkt = pkt

    def __eq__(self, other):
        if isinstance(other, WltPkt):
            return (
                self.hdr == other.hdr and
                self.generic == other.generic and
                self.pkt == other.pkt
            )
        return False

    def dump(self):
        if self.pkt:
            return self.hdr.dump() + self.pkt.dump()
        return self.hdr.dump() + self.generic.dump()

    def set(self, string):
        if not string.startswith("1E16"):
            string = "1E16" + string

        self.hdr.set(string[0:14])
        if self.hdr.group_id == GROUP_ID_BRG2GW or self.hdr.group_id == GROUP_ID_GW2BRG:
            # GROUP_ID_BRG2GW & GROUP_ID_GW2BRG
            self.generic = GenericV7()
            self.generic.set(string[14:62])

            # MEL modules
            if self.generic.module_type == MODULE_IF and self.generic.msg_type == BRG_MGMT_MSG_TYPE_CFG_INFO:
                self.pkt = ModuleIfV7()
                self.pkt.set(string[14:62])
            elif self.generic.module_type == MODULE_ENERGY_2400:
                self.pkt = ModuleEnergy2400V7()
                self.pkt.set(string[14:62])
            elif self.generic.module_type == MODULE_ENERGY_SUB1G:
                self.pkt = ModuleEnergySub1GV7()
                self.pkt.set(string[14:62])
            elif self.generic.module_type == MODULE_PWR_MGMT:
                self.pkt = ModulePwrMgmtV7()
                self.pkt.set(string[14:62])
            elif self.generic.module_type == MODULE_PERIPH:
                self.pkt = ModulePeriphV7()
                self.pkt.set(string[14:62])
            elif self.generic.module_type == MODULE_CALIBRATION:
                self.pkt = ModuleCalibrationV7()
                self.pkt.set(string[14:62])
            elif self.generic.module_type == MODULE_DATAPATH:
                self.pkt = ModuleDatapathV7()
                self.pkt.set(string[14:62])
            # OLD global config
            elif self.generic.module_type == MODULE_GLOBAL:
                if self.hdr.group_id == GROUP_ID_GW2BRG:
                    # GROUP_ID_GW2BRG
                    if self.generic.msg_type == BRG_MGMT_MSG_TYPE_CFG_SET:
                        self.pkt = Gw2BrgCfgV7()
                        self.pkt.set(string[14:62])
                else:
                    # GROUP_ID_BRG2GW
                    if self.generic.msg_type == BRG_MGMT_MSG_TYPE_CFG_SET or self.generic.msg_type == BRG_MGMT_MSG_TYPE_CFG_INFO:
                        if self.generic.api_version == API_VERSION_V2:
                            self.pkt = Brg2GwCfgV2()
                            self.pkt.set(string[14:62])
                        elif self.generic.api_version == API_VERSION_V5:
                            self.pkt = Brg2GwCfgV5()
                            self.pkt.set(string[14:62])
                        elif self.generic.api_version == API_VERSION_V6:
                            self.pkt = Brg2GwCfgV6()
                            self.pkt.set(string[14:62])
                        else:
                            self.pkt = Brg2GwCfgV7()
                            self.pkt.set(string[14:62])
                    elif self.generic.msg_type == BRG_MGMT_MSG_TYPE_HB:
                        if self.generic.api_version < API_VERSION_V6:
                            self.pkt = Brg2GwHbV1()
                            self.pkt.set(string[14:62])
                        elif self.generic.api_version == API_VERSION_V6:
                            self.pkt = Brg2GwHbV6()
                            self.pkt.set(string[14:62])
                        else:
                            self.pkt = Brg2GwHbV7()
                            self.pkt.set(string[14:62])
                    elif self.generic.msg_type == BRG_MGMT_MSG_TYPE_ACTION:
                        self.pkt = ActionV7()
                        self.pkt.set(string[14:62])
        elif self.hdr.group_id == GROUP_ID_SIDE_INFO_SENSOR:
            self.pkt = SideInfoSensor()
            self.pkt.set(string[14:62])
        elif self.hdr.group_id == GROUP_ID_SIDE_INFO:
            self.pkt = SideInfo()
            self.pkt.set(string[14:62])

hex_str2int = lambda x: int(x,16)