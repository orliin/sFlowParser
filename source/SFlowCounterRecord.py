import logging
from xdrlib import Unpacker

from sflowcollect.helpers import speed_to_string


class SFlowCounterRecord:
    COUNTER_DATA_GENERIC_INTERFACE = 1
    COUNTER_DATA_ETHERNET_INTERFACE = 2
    COUNTER_DATA_TOKEN_RING = 3
    COUNTER_DATA_VG_INTERFACE = 4
    COUNTER_DATA_VLAN = 5
    COUNTER_DATA_PROCESSOR = 1001

    def __init__(self, unpacker: Unpacker):
        self.counter_format = None
        self.counter = None

        self.counter_format = unpacker.unpack_uint()
        counter_data = unpacker.unpack_opaque()
        unpacker_counter_data = Unpacker(counter_data)

        if self.counter_format == SFlowCounterRecord.COUNTER_DATA_GENERIC_INTERFACE:
            self.flow = GenericInterfaceCounters(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_ETHERNET_INTERFACE:
            self.flow = EthernetInterfaceCounters(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_TOKEN_RING:
            pass
            self.flow = _(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_VG_INTERFACE:
            pass
            self.flow = _(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_VLAN:
            pass
            self.flow = _(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_PROCESSOR:
            pass
            self.flow = _(unpacker_counter_data)
        else:
            logging.debug('read_flow_record:Unimplemented data_format (%d)' % self.flow_format)

    @property
    def data(self) -> dict:
        return dict(
        )


class GenericInterfaceCounters:

    def __init__(self, unpacker: Unpacker):
        self.index = None
        self.if_type = None
        self.speed = None
        self.direction = None
        self.status = None
        self.in_octets = None
        self.in_ucasts = None
        self.in_mcasts = None
        self.in_bcasts = None
        self.in_discards = None
        self.in_errors = None
        self.in_unknown_protos = None
        self.out_octets = None
        self.out_ucasts = None
        self.out_mcasts = None
        self.out_bcasts = None
        self.out_discards = None
        self.out_errors = None
        self.promiscuous_mode = None

        self._parse_raw_generic_interface_counters(unpacker)

    def _parse_raw_generic_interface_counters(self, unpacker: Unpacker):
        # Unpack Generic Interface Counters
        #     unsigned int ifIndex;
        #     unsigned int ifType;
        #     unsigned hyper ifSpeed;
        #     unsigned int ifDirection;      derived from MAU MIB (RFC 2668)
        #                                    0 = unkown, 1=full-duplex, 2=half-duplex,
        #                                    3 = in, 4=out
        #     unsigned int ifStatus;         bit field with the following bits assigned
        #                                    bit 0 = ifAdminStatus (0 = down, 1 = up)
        #                                    bit 1 = ifOperStatus (0 = down, 1 = up)
        #     unsigned hyper ifInOctets;
        #     unsigned int ifInUcastPkts;
        #     unsigned int ifInMulticastPkts;
        #     unsigned int ifInBroadcastPkts;
        #     unsigned int ifInDiscards;
        #     unsigned int ifInErrors;
        #     unsigned int ifInUnknownProtos;
        #     unsigned hyper ifOutOctets;
        #     unsigned int ifOutUcastPkts;
        #     unsigned int ifOutMulticastPkts;
        #     unsigned int ifOutBroadcastPkts;
        #     unsigned int ifOutDiscards;
        #     unsigned int ifOutErrors;
        #     unsigned int ifPromiscuousMode;

        self.index = unpacker.unpack_uint()
        self.if_type = unpacker.unpack_uint()
        self.speed = unpacker.unpack_uhyper()
        self.direction = unpacker.unpack_uint()
        self.status = unpacker.unpack_uint()
        self.in_octets = unpacker.unpack_uhyper()
        self.in_ucasts = unpacker.unpack_uint()
        self.in_mcasts = unpacker.unpack_uint()
        self.in_bcasts = unpacker.unpack_uint()
        self.in_discards = unpacker.unpack_uint()
        self.in_errors = unpacker.unpack_uint()
        self.in_unknown_protos = unpacker.unpack_uint()
        self.out_octets = unpacker.unpack_uhyper()
        self.out_ucasts = unpacker.unpack_uint()
        self.out_mcasts = unpacker.unpack_uint()
        self.out_bcasts = unpacker.unpack_uint()
        self.out_discards = unpacker.unpack_uint()
        self.out_errors = unpacker.unpack_uint()
        self.promiscuous_mode = unpacker.unpack_uint()

    # TODO: change this to json
    def __repr__(self):
        return ('<IfCounters| idx: %d, speed: %s, in_octets: %d, out_octets: %d>' %
                (self.index,
                 speed_to_string(self.speed),
                 self.in_octets,
                 self.out_octets))


class EthernetInterfaceCounters:

    def __init__(self, unpacker: Unpacker):
        self.dot3_stats_alignment_errors = None
        self.dot3_stats_fcs_errors = None
        self.dot3_stats_single_collision_frames = None
        self.dot3_stats_multiple_collision_frames = None
        self.dot3_stats_sqe_test_errors = None
        self.dot3_stats_deferred_transmissions = None
        self.dot3_stats_late_collisions = None
        self.dot3_stats_excessive_collisions = None
        self.dot3_stats_internal_mac_transmit_errors = None
        self.dot3_stats_carrier_sense_errors = None
        self.dot3_stats_frame_too_longs = None
        self.dot3_stats_internal_mac_receive_errors = None
        self.dot3_stats_symbol_errors = None

        self._parse_raw_ethernet_interface_counters(unpacker)

    def _parse_raw_ethernet_interface_counters(self, unpacker: Unpacker):
        # Unpack ethernet_counters structure
        #      unsigned int dot3_stats_alignment_errors;
        #      unsigned int dot3_stats_fcs_errors;
        #      unsigned int dot3_stats_single_collision_frames;
        #      unsigned int dot3_stats_multiple_collision_frames;
        #      unsigned int dot3_stats_sqe_test_errors;
        #      unsigned int dot3_stats_deferred_transmissions;
        #      unsigned int dot3_stats_late_collisions;
        #      unsigned int dot3_stats_excessive_collisions;
        #      unsigned int dot3_stats_internal_mac_transmit_errors;
        #      unsigned int dot3_stats_carrier_sense_errors;
        #      unsigned int dot3_stats_frame_too_longs;
        #      unsigned int dot3_stats_internal_mac_receive_errors;
        #      unsigned int dot3_stats_symbol_errors;

        self.dot3_stats_alignment_errors = unpacker.unpack_uint()
        self.dot3_stats_fcs_errors = unpacker.unpack_uint()
        self.dot3_stats_single_collision_frames = unpacker.unpack_uint()
        self.dot3_stats_multiple_collision_frames = unpacker.unpack_uint()
        self.dot3_stats_sqe_test_errors = unpacker.unpack_uint()
        self.dot3_stats_deferred_transmissions = unpacker.unpack_uint()
        self.dot3_stats_late_collisions = unpacker.unpack_uint()
        self.dot3_stats_excessive_collisions = unpacker.unpack_uint()
        self.dot3_stats_internal_mac_transmit_errors = unpacker.unpack_uint()
        self.dot3_stats_carrier_sense_errors = unpacker.unpack_uint()
        self.dot3_stats_frame_too_longs = unpacker.unpack_uint()
        self.dot3_stats_internal_mac_receive_errors = unpacker.unpack_uint()
        self.dot3_stats_symbol_errors = unpacker.unpack_uint()
