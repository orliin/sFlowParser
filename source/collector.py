import logging
import pickle
from collections import deque
from socket import socket, AF_INET, SOCK_DGRAM
from xdrlib import Unpacker

from source.sflowparse.SFlowDatagram import SFlowDatagram
from source.collector.RealTimeCollector import RealTimeCollector

MODE = '-file'  # -socket, -socket+file or -file
RAW_DATA_FILENAME = 'raw.dat'

BYTES_LIST_SIZE_LIMIT = 1000


def get_raw_data(mode, bytes_deque):
    if mode == '-socket+file':
        listen_address = ("0.0.0.0", 6343)
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(listen_address)

        while True:
            data, collector_address = sock.recvfrom(65535)

            print(len(bytes_deque))
            if len(bytes_deque) <= BYTES_LIST_SIZE_LIMIT:
                bytes_deque.append(data)

            if len(bytes_deque) == BYTES_LIST_SIZE_LIMIT:
                try:
                    f = open(RAW_DATA_FILENAME, mode='wb')
                    pickle.dump(bytes_deque, f)
                    f.close()
                except IOError as ex:
                    f.close()
                    raise ex

            yield data

    elif mode == '-socket':
        listen_address = ("0.0.0.0", 6343)
        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(listen_address)

        while True:
            data, collector_address = sock.recvfrom(65535)
            yield data

    elif mode == '-file':
        with open(RAW_DATA_FILENAME, mode='rb') as f:
            bytes_deque = pickle.load(f)
            for data in bytes_deque:
                yield data


if __name__ == '__main__':
    logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

    sflow_datagram = None
    real_time_collector = RealTimeCollector()

    bytes_deque_global = deque()
    for raw_data in get_raw_data(MODE, bytes_deque_global):

        unpacker = Unpacker(raw_data)

        try:
            sflow_datagram = SFlowDatagram(unpacker)
        except Exception as e:
            logging.warning("Bad sflow datagram: {}".format(raw_data))
            continue
            raise e

        #print(sflow_datagram)
        for sample in sflow_datagram.data['samples']:
            if sample['type'] == 1:
                print("insert traffic,agent_ip_address={0},input_if={1},output_if={2} sample_pool={3},sequence_number={4},sampling_rate={5}"
                      .format(sflow_datagram.data['agent_ip_address'],
                              sample['sample']['input_if'],
                              sample['sample']['output_if'],
                              sample['sample']['sample_pool'],
                              sample['sample']['sequence_number'],
                              sample['sample']['sampling_rate']
                              ))

        real_time_collector.add(sflow_datagram.data)