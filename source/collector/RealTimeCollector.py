from time import time

class RealTimeCollector:
    """
    Collecting and analysing real time datagram flow

    RealTimeCollector takes sFlow datagrams and:
        1) aggregates data every second
        2) keeps expiration info for each type of data
        3) sends unexpired data to PersistenceCollector

    1. Data is aggregated (summed up) and every new second is exported to time series.
    2.
    """

    def __init__(self):
        self.current_second = int(time())
        self.persistence_collector = None
        pass

    def add(self, data: dict):
        pass
