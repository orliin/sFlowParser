def ip_to_string(ip: int) -> str:
    """Returns ip as a string in dotted quad notation."""
    #    ip = ntohl(ip)              # network byte order is big-endian
    return '%d.%d.%d.%d' % (ip & 0xff,
                            (ip >> 8) & 0xff,
                            (ip >> 16) & 0xff,
                            (ip >> 24) & 0xff)


def agent_ip_version_to_string(version: int) -> str:
    if version == 1:
        return 'IPv4'
    elif version == 2:
        return 'IPv6'
    else:
        return 'unknown'


def speed_to_string(speed):
    speed_name = {10000000: '10Mb',
                  100000000: '100Mb',
                  1000000000: '1Gb',
                  10000000000: '10Gb'}

    if speed in speed_name:
        return speed_name[speed]
    else:
        return str(speed)
