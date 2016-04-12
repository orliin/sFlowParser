from xdrlib import Unpacker
from socket import ntohl
import json
import logging

from sflowparse.SFlowSample import SFlowSample
from sflowparse.helpers import ip_to_string, agent_ip_version_to_string


class SFlowDatagram:

    def __init__(self: object, unpacker: Unpacker):
        # self.raw_data = unpacker.get_buffer()
        self.sflow_version = None
        self.agent_ip_version = None
        self.agent_ip_address = None
        self.sub_agent_id = None
        self.sequence_number = None
        self.switch_uptime = None
        self.samples = []

        self._parse_raw_sflow_datagram(unpacker)

    @property
    def number_of_samples(self) -> int:
        return len(self.samples)

    def _parse_raw_sflow_datagram(self, unpacker: Unpacker):
        self.sflow_version = unpacker.unpack_int()
        if not self.sflow_version == 5:
            logging.debug("Unimplemented sFlow version: {}".format(self.sflow_version))
            # TODO: read remainder if needed
            return

        self.agent_ip_version = unpacker.unpack_int()
        if self.agent_ip_version == 1:
            self.agent_ip_address = ntohl(unpacker.unpack_uint())
        # TODO: implement other versions
        else:
            logging.debug("Unimplemented agent IP version: {}".format(self.agent_ip_version))
            return

        self.sub_agent_id = unpacker.unpack_uint()
        self.sequence_number = unpacker.unpack_uint()
        self.switch_uptime = unpacker.unpack_uint()

        samples_in_datagram = unpacker.unpack_uint()
        for _ in range(samples_in_datagram):
            try:
                self.samples.append(SFlowSample(unpacker))
            except Exception as e:
                logging.warning("Bad sample")
                raise e

    @property
    def data(self) -> dict:
        return dict(
            sflow_version=self.sflow_version,
            agent_ip_version=agent_ip_version_to_string(self.agent_ip_version),
            agent_ip_address=ip_to_string(self.agent_ip_address),
            sub_agent_id=ip_to_string(self.sub_agent_id),
            sequence_number=self.sequence_number,
            switch_uptime=self.switch_uptime,
            samples=[sample.data for sample in self.samples]
            )

    def __getitem__(self, key):
        return self.data[key]

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
