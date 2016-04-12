import logging
import json
from xdrlib import Unpacker

from sflowcollect.SFlowFlowRecord import SFlowFlowRecord
from sflowcollect.SFlowCounterRecord import SFlowCounterRecord


class SFlowSample:
    # Constants for the sample_data member of 'struct sample_record'
    # (p. 32 of sflow_version_5.txt).  See pp. 29-31 for the meaning
    # of these values.
    SAMPLE_DATA_FLOW_SAMPLE = 1
    SAMPLE_DATA_COUNTER_SAMPLE = 2
    SAMPLE_DATA_EXPANDED_FLOW_SAMPLE = 3
    SAMPLE_DATA_EXPANDED_COUNTER_SAMPLE = 4

    def __init__(self, unpacker: Unpacker):
        self.type = None
        self.sample = None

        self.type = unpacker.unpack_uint()

        if self.type == SFlowSample.SAMPLE_DATA_FLOW_SAMPLE:
            self.sample = SFlowFlowSample(unpacker)

        elif self.type == SFlowSample.SAMPLE_DATA_COUNTER_SAMPLE:
            self.sample = SFlowCounterSample(unpacker)

        elif self.type == SFlowSample.SAMPLE_DATA_EXPANDED_FLOW_SAMPLE:
            self.sample = SFlowExpandedFlowSample(unpacker)

        elif self.type == SFlowSample.SAMPLE_DATA_EXPANDED_COUNTER_SAMPLE:
            self.sample = SFlowExpandedCounterSample(unpacker)

        else:
            logging.debug("Unknown data format: {}".format(type))
            logging.debug(unpacker.unpack_opaque())

    @property
    def data(self) -> dict:
        return dict(
            type=self.type,
            sample=self.sample.data
        )

    @property
    def json(self) -> str:
        return json.dumps(self.data, indent=4)

    def __str__(self):
        """
        Return json representation of the Datagram object
        :return: str
        """
        return self.json

    def __repr__(self):
        """
        Return json representation of the Datagram object
        :return: str
        """
        return self.json


class SFlowFlowSample:

    def __init__(self, unpacker: Unpacker):
        self.sequence_number = None
        self.source_id = None
        self.sampling_rate = None
        self.sample_pool = None
        self.drops = None
        self.input_if = None
        self.output_if = None
        self.flows = []

        sample_data = unpacker.unpack_opaque()
        unpacker_sample_data = Unpacker(sample_data)
        self._parse_raw_sflow_flow_sample(unpacker_sample_data)

    @property
    def number_of_flows(self) -> int:
        return len(self.flows)

    def _parse_raw_sflow_flow_sample(self, unpacker: Unpacker):
        self.sequence_number = unpacker.unpack_uint()
        self.source_id = unpacker.unpack_uint()
        self.sampling_rate = unpacker.unpack_uint()
        self.sample_pool = unpacker.unpack_uint()
        self.drops = unpacker.unpack_uint()
        self.input_if = unpacker.unpack_uint()
        self.output_if = unpacker.unpack_uint()

        flows_in_sample = unpacker.unpack_uint()
        for _ in range(flows_in_sample):
            self.flows.append(SFlowFlowRecord(unpacker))

    @property
    def data(self) -> dict:
        return dict(
            sequence_number=self.sequence_number,
            source_id=self.source_id,
            sampling_rate=self.sampling_rate,
            sample_pool=self.sample_pool,
            drops=self.drops,
            input_if=self.input_if,
            output_if=self.output_if,
            flows=[flow.data for flow in self.flows]
        )


class SFlowCounterSample:

    def __init__(self, unpacker: Unpacker):
        self.sequence_number = None
        self.source_id = None
        self.counters = []

        sample_data = unpacker.unpack_opaque()
        unpacker_sample_data = Unpacker(sample_data)
        self._parse_raw_sflow_counter_sample(unpacker_sample_data)

    @property
    def number_of_counters(self) -> int:
        return len(self.counters)

    def _parse_raw_sflow_counter_sample(self, unpacker: Unpacker):
        self.sequence_number = unpacker.unpack_uint()
        self.source_id = unpacker.unpack_uint()
        counters_in_sample = unpacker.unpack_uint()

        for _ in range(counters_in_sample):
            self.counters.append(SFlowCounterRecord(unpacker))

    @property
    def data(self) -> dict:
        return dict(
            sequence_number=self.sequence_number,
            source_id=self.source_id,
            counters=[counter.data for counter in self.counters]
        )


class SFlowExpandedFlowSample:

    def __init__(self, unpacker: Unpacker):
        # struct flow_sample_expanded
        self.sequence_number = None
        self.source_id = {}
        self.sampling_rate = None
        self.sample_pool = None
        self.drops = None
        self.input_if = {}
        self.output_if = {}
        self.flows = []

        sample_data = unpacker.unpack_opaque()
        unpacker_sample_data = Unpacker(sample_data)
        self._parse_raw_expanded_sflow_flow_sample(unpacker_sample_data)

    def _parse_raw_expanded_sflow_flow_sample(self, unpacker: Unpacker):
        self.sequence_number = unpacker.unpack_uint()
        self.source_id['type'] = unpacker.unpack_uint()
        self.source_id['index'] = unpacker.unpack_uint()
        self.sampling_rate = unpacker.unpack_uint()
        self.sample_pool = unpacker.unpack_uint()
        self.drops = unpacker.unpack_uint()
        self.input_if['format'] = unpacker.unpack_uint()
        self.input_if['value'] = unpacker.unpack_uint()
        self.output_if['format'] = unpacker.unpack_uint()
        self.output_if['value'] = unpacker.unpack_uint()

        flows_in_sample = unpacker.unpack_uint()
        for _ in range(flows_in_sample):
            self.flows.append(SFlowFlowRecord(unpacker))

    @property
    def data(self) -> dict:
        return dict(
            sequence_number=self.sequence_number,
            source_id=self.source_id,
            sampling_rate=self.sampling_rate,
            sample_pool=self.sample_pool,
            drops=self.drops,
            input_if=self.input_if,
            output_if=self.output_if,
            flows=[flow.data for flow in self.flows]
        )


class SFlowExpandedCounterSample:

    def __init__(self, unpacker: Unpacker):
        # struct struct counters_sample_expanded
        self.sequence_number = None
        self.source_id = {}
        self.counters = []

        sample_data = unpacker.unpack_opaque()
        unpacker_sample_data = Unpacker(sample_data)
        self._parse_raw_expanded_sflow_counter_sample(unpacker_sample_data)

    @property
    def number_of_counters(self) -> int:
        return len(self.counters)

    def _parse_raw_expanded_sflow_counter_sample(self, unpacker: Unpacker):
        self.sequence_number = unpacker.unpack_uint()
        self.source_id['type'] = unpacker.unpack_uint()
        self.source_id['index'] = unpacker.unpack_uint()
        counters_in_sample = unpacker.unpack_uint()

        for _ in range(counters_in_sample):
            self.counters.append(SFlowCounterRecord(unpacker))

    @property
    def data(self) -> dict:
        return dict(
            sequence_number=self.sequence_number,
            source_id=self.source_id,
            counters=[counter.data for counter in self.counters]
        )
