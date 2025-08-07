import netifaces


def get_all_network_interfaces():
    # 获取所有网络接口
    interfaces = netifaces.interfaces()
    return interfaces


def get_ip_addresses(interface):
    # 获取指定接口的所有IP地址
    addrs = netifaces.ifaddresses(interface)
    ip_addresses = []

    # 检查是否有AF_INET（IPv4）地址
    if netifaces.AF_INET in addrs:
        for addr_info in addrs[netifaces.AF_INET]:
            ip_addresses.append(addr_info["addr"])

    # 检查是否有AF_INET6（IPv6）地址
    if netifaces.AF_INET6 in addrs:
        for addr_info in addrs[netifaces.AF_INET6]:
            ip_addresses.append(addr_info["addr"])

    return ip_addresses


def main():
    interfaces = get_all_network_interfaces()
    print("Available network interfaces:")
    for interface in interfaces:
        print(f"\nInterface: {interface}")
        ip_addresses = get_ip_addresses(interface)
        if ip_addresses:
            print("IP Addresses:")
            for ip in ip_addresses:
                print(f"  {ip}")
        else:
            print("  No IP addresses found for this interface.")


if __name__ == "__main__":
    main()
