import subprocess
import sys
import ipaddress
import argparse


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def iswin():
    return sys.platform.startswith("win")


def islinux():
    return sys.platform.startswith("linux")


def ismac():
    return sys.platform.startswith("darwin")


def single_ping_args(ip):
    args = ["ping", ip]
    if iswin():
        args.extend(["-n", "1"])
    else:
        args.extend(["-c", "1"])
    return args


def ping_host(ip):
    try:
        subprocess.check_output(single_ping_args(ip), stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def find_mtu(ip, min_mtu, max_mtu, step):
    if not is_valid_ip(ip):
        print("Invalid IP address.")
        return

    if not ping_host(ip):
        print("Destination is unreachable.")
        return
    
    if min_mtu < 0 or max_mtu < 0 or step <= 0:
        print("MTU values must be positive.")
        return
    
    if min_mtu > max_mtu:
        print("Minimum MTU value cannot be greater than maximum.")
        return

    good_mtu = 0
    for mtu in range(min_mtu, max_mtu, step):
        try:
            args = single_ping_args(ip)
            if iswin():
                args.extend(["-f", "-l", str(mtu)])
            elif islinux():
                args.extend(["-M", "do", "-s", str(mtu)])
            elif ismac():
                args.extend(["-D", "-s", str(mtu)])
            subprocess.check_output(args, stderr=subprocess.DEVNULL)
            good_mtu = mtu
        except subprocess.CalledProcessError:
            if good_mtu:
                print(f"Maximum MTU value: {good_mtu}")
            else:
                print("Failed to find MTU value.")
            return
    print(f"Upper limit of range reached: {good_mtu}")


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
        '-n',
        '--min',
        dest='min',
        default=500,
        help='Min MTU value to check',
        type=int
    )

    parser.add_argument(
        '-x',
        '--max',
        dest='max',
        default=1500,
        help='Max MTU value to check',
        type=int
    )

    parser.add_argument(
        '-s',
        '--step',
        dest='step',
        default=10,
        help='Step value',
        type=int
    )

    args = parser.parse_args()
    find_mtu(args.ip, args.min, args.max, args.step)


if __name__ == "__main__":
    main()
