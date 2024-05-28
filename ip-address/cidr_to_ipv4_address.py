import ipaddress

CIDR = "192.168.1.0/24"

def cidr_to_ip_list():
    network = ipaddress.IPv4Network(CIDR, strict=False)
    return [str(ip) for ip in network.hosts()]

def main():
    ip_list = cidr_to_ip_list()
    for ip in ip_list:
        print(ip)

if __name__ == "__main__":
    main()
