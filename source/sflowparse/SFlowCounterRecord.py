import logging
from xdrlib import Unpacker

from source.sflowparse.helpers import speed_to_string


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
            self.counter = GenericInterfaceCounters(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_ETHERNET_INTERFACE:
            self.counter = EthernetInterfaceCounters(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_TOKEN_RING:
            pass
            self.counter = TokenRingCounters(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_VG_INTERFACE:
            pass
            self.counter = VgInterfaceCounters(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_VLAN:
            self.counter = VlanCounters(unpacker_counter_data)
        elif self.counter_format == SFlowCounterRecord.COUNTER_DATA_PROCESSOR:
            self.counter = ProcessorCounters(unpacker_counter_data)
        else:
            logging.debug('read_flow_record:Unimplemented data_format (%d)' % self.flow_format)

    @property
    def data(self) -> dict:
        return dict(
            counter_format=self.counter_format,
            counter=self.counter.data
        )


class GenericInterfaceCounters:

    def __init__(self, unpacker: Unpacker):
        self.if_index = None
        self.if_type = None
        self.if_speed = None
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

        self.if_index = unpacker.unpack_uint()
        self.if_type = unpacker.unpack_uint()
        self.if_speed = unpacker.unpack_uhyper()
        self.if_direction = unpacker.unpack_uint()
        self.if_status = unpacker.unpack_uint()
        self.if_in_octets = unpacker.unpack_uhyper()
        self.if_in_ucasts = unpacker.unpack_uint()
        self.if_in_mcasts = unpacker.unpack_uint()
        self.if_in_bcasts = unpacker.unpack_uint()
        self.if_in_discards = unpacker.unpack_uint()
        self.if_in_errors = unpacker.unpack_uint()
        self.if_in_unknown_protos = unpacker.unpack_uint()
        self.if_out_octets = unpacker.unpack_uhyper()
        self.if_out_ucasts = unpacker.unpack_uint()
        self.if_out_mcasts = unpacker.unpack_uint()
        self.if_out_bcasts = unpacker.unpack_uint()
        self.if_out_discards = unpacker.unpack_uint()
        self.if_out_errors = unpacker.unpack_uint()
        self.if_promiscuous_mode = unpacker.unpack_uint()

    # TODO: change this to json
    def __repr__(self):
        return ('<IfCounters| idx: %d, speed: %s, in_octets: %d, out_octets: %d>' %
                (self.if_index,
                 speed_to_string(self.if_speed),
                 self.in_octets,
                 self.out_octets))

    @property
    def data(self) -> dict:
        return dict(
            if_index=self.if_index,
            if_type=self.if_type,
            if_speed=self.if_speed,
            if_direction=self.if_direction,
            if_status=self.if_status,
            if_in_octets=self.if_in_octets,
            if_in_ucasts=self.if_in_ucasts,
            if_in_mcasts=self.if_in_mcasts,
            if_in_bcasts=self.if_in_bcasts,
            if_in_discards=self.if_in_discards,
            if_in_errors=self.if_in_errors,
            if_in_unknown_protos=self.if_in_unknown_protos,
            if_out_octets=self.if_out_octets,
            if_out_ucasts=self.if_out_ucasts,
            if_out_mcasts=self.if_out_mcasts,
            if_out_bcasts=self.if_out_bcasts,
            if_out_discards=self.if_out_discards,
            if_out_errors=self.if_out_errors,
            if_promiscuous_mode=self.if_promiscuous_mode,
        )



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

    @property
    def data(self) -> dict:
        return dict(
            dot3_stats_alignment_errors=self.dot3_stats_alignment_errors,
            dot3_stats_fcs_errors=self.dot3_stats_fcs_errors,
            dot3_stats_single_collision_frames=self.dot3_stats_single_collision_frames,
            dot3_stats_multiple_collision_frames=self.dot3_stats_multiple_collision_frames,
            dot3_stats_sqe_test_errors=self.dot3_stats_sqe_test_errors,
            dot3_stats_deferred_transmissions=self.dot3_stats_deferred_transmissions,
            dot3_stats_late_collisions=self.dot3_stats_late_collisions,
            dot3_stats_excessive_collisions=self.dot3_stats_excessive_collisions,
            dot3_stats_internal_mac_transmit_errors=self.dot3_stats_internal_mac_transmit_errors,
            dot3_stats_carrier_sense_errors=self.dot3_stats_carrier_sense_errors,
            dot3_stats_frame_too_longs=self.dot3_stats_frame_too_longs,
            dot3_stats_internal_mac_receive_errors=self.dot3_stats_internal_mac_receive_errors,
            dot3_stats_symbol_errors=self.dot3_stats_symbol_errors,
        )