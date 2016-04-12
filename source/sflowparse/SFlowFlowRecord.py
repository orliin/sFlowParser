import logging
from xdrlib import Unpacker
from enum import Enum


class SFlowFlowRecord:

    # Constants for the flow_format member of 'struct flow_record'
    # (p. 29).  See pp. 35-41 for the meaning of these values.
    FLOW_DATA_RAW_HEADER = 1
    FLOW_DATA_ETHERNET_HEADER = 2
    FLOW_DATA_IPV4_HEADER = 3
    FLOW_DATA_IPV6_HEADER = 4
    FLOW_DATA_EXT_SWITCH = 1001
    FLOW_DATA_EXT_ROUTER = 1002
    FLOW_DATA_EXT_GATEWAY = 1003
    FLOW_DATA_EXT_USER = 1004
    FLOW_DATA_EXT_URL = 1005
    FLOW_DATA_EXT_MPLS = 1006
    FLOW_DATA_EXT_NAT = 1007
    FLOW_DATA_EXT_MPLS_TUNNEL = 1008
    FLOW_DATA_EXT_MPLS_VC = 1009
    FLOW_DATA_EXT_MPLS_FEC = 1010
    FLOW_DATA_EXT_MPLS_LVP_FEC = 1011
    FLOW_DATA_EXT_VLAN_TUNNEL = 1012

    def __init__(self, unpacker: Unpacker):
        self.flow_format = None
        self.flow = None

        self.flow_format = unpacker.unpack_uint()
        flow_data = unpacker.unpack_opaque()
        unpacker_flow_data = Unpacker(flow_data)

        if self.flow_format == SFlowFlowRecord.FLOW_DATA_RAW_HEADER:
            self.flow = FlowDataRawHeader(unpacker_flow_data)
        elif self.flow_format == SFlowFlowRecord.FLOW_DATA_ETHERNET_HEADER:
            self.flow = FlowDataEthernetHeader(unpacker_flow_data)
        elif self.flow_format == SFlowFlowRecord.FLOW_DATA_IPV4_HEADER:
            self.flow = FlowDataIPv4Header(unpacker_flow_data)
        elif self.flow_format == SFlowFlowRecord.FLOW_DATA_EXT_SWITCH:
            self.flow = FlowDataExtSwitch(unpacker_flow_data)
        else:
            logging.debug('read_flow_record:Unimplemented data_format (%d)' % self.flow_format)

    @property
    def data(self) -> dict:
        return dict(
            flow_format=self.flow_format,
            flow=self.flow.data,
        )


class FlowDataRawHeader:

    class HeaderProtocol(Enum):
        ETHERNET_ISO88023 = 1
        ISO88024_TOKENBUS = 2
        ISO88025_TOKENRING = 3
        FDDI = 4
        FRAME_RELAY = 5
        X25 = 6
        PPP = 7
        SMDS = 8
        AAL5 = 9
        AAL5_IP = 10
        IPv4 = 11
        IPv6 = 12
        MPLS = 13
        POS = 14

    '''
    /* opaque = flow_data; enterprise = 0; format = 1 */

    struct sampled_header {
       header_protocol protocol;
       unsigned int frame_length;
       unsigned int stripped;
       opaque header<>;
    }
    '''
    def __init__(self, unpacker: Unpacker):
        self.protocol = None
        self.frame_length = None
        self.stripped = None
        self.header = None

    @property
    def data(self):
        return dict(
            protocol=self.HeaderProtocol(self.protocol)
        )


class FlowDataEthernetHeader:

    def __init__(self, unpacker: Unpacker):
        pass

    @property
    def data(self):
        return dict()


class FlowDataIPv4Header:

    def __init__(self, unpacker: Unpacker):
        pass

    @property
    def data(self):
        return dict()


class FlowDataExtSwitch:

    def __init__(self, unpacker: Unpacker):
        pass

    @property
    def data(self):
        return dict()
