import subprocess
import sys
import ipaddress
import argparse
import pythonping


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def try_ping_host(ip, mtu):
    responses = iter(pythonping.ping(ip, size=mtu, df=True, count=1))
    try:
        response = next(responses)
        return response.success
    except StopIteration:
        return False


MIN_MTU = 68
HEADER_SIZE = 28


def find_mtu(ip, max_mtu):
    if not is_valid_ip(ip):
        print("Invalid IP address.")
        return

    if not try_ping_host(ip, MIN_MTU):
        print("Destination is unreachable.")
        return

    if max_mtu - HEADER_SIZE < MIN_MTU:
        print(f"Max MTU value must be greater than {MIN_MTU + HEADER_SIZE}.")
        return

    l = MIN_MTU
    r = max_mtu - HEADER_SIZE + 1
    while r - l > 1:
        m = (l + r) // 2
        if try_ping_host(ip, m):
            l = m
        else:
            r = m

    print(f"Maximum MTU value: {l + HEADER_SIZE}")
    return l


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--ip',
        dest='ip',
        default='127.0.0.1',
        help='Destination IP address'
    )

    parser.add_argument(
        '-x',
        '--max',
        dest='max',
        default=1500,
        help='Max MTU value to check',
        type=int
    )

    args = parser.parse_args()
    find_mtu(args.ip, args.max)


if __name__ == "__main__":
    main()
