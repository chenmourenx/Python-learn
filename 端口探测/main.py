import socket
import telnetlib
import threading
import nmap
import scapy.all as scapy


def check_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((host, port))
        print(f"The port {port} on host {host} is open.\n")
        s.close()
        return True
    except:
        # print(f"The port {port} on host {host} is closed.")
        s.close()
        return False


def check_telnet_port(host, port):
    try:
        telnetlib.Telnet(host, port, timeout=5)
        print(f"The port {port} on host {host} is open for Telnet.\n")
        return True
    except:
        # print(f"The port {port} on host {host} is closed for Telnet.\n")
        return False


def check_nmap_port(host, port):
    nm = nmap.PortScanner()
    nm.scan(host, str(port))
    if nm[host]['tcp'][int(port)]['state'] == 'open':
        print(f"The port {port} on host {host} is open for nmap.\n")
        return True
    else:
        # print(f"The port {port} on host {host} is closed for Nmap.\n")
        return False


def check_scapy_port(host, port):
    ans, unans = scapy.sr(scapy.IP(dst=host) / scapy.TCP(dport=port, flags="S"), timeout=5, verbose=False)
    if len(ans) > 0:
        print(f"The port {port} on host {host} is open for Scapy.\n")
        return True
    else:
        # print(f"The port {port} on host {host} is closed for Scapy.\n")
        return False


def run_check_port(host, port):
    t = threading.Thread(target=check_port, args=(host, port))
    t.start()


def run_check_telnet_port(host, port):
    t = threading.Thread(target=check_telnet_port, args=(host, port))
    t.start()


def run_check_nmap_port(host, port):
    t = threading.Thread(target=check_nmap_port, args=(host, port))
    t.start()


def run_check_scapy_port(host, port):
    t = threading.Thread(target=check_scapy_port, args=(host, port))
    t.start()


# 请在下面填入实际检测的主机名或 IP 地址
host = "www.baidu.com"
try:
    host = socket.gethostbyname(host)
except:
    print(f"Could not resolve host {host}")
    exit()
port_list = [80, 443, 22, 21, 23]

threads = []

for port in port_list:
    t = threading.Thread(target=run_check_port, args=(host, port))
    threads.append(t)
    t = threading.Thread(target=run_check_telnet_port, args=(host, port))
    threads.append(t)
    t = threading.Thread(target=run_check_nmap_port, args=(host, port))
    threads.append(t)
    t = threading.Thread(target=run_check_scapy_port, args=(host, port))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()
