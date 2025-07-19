import network
import socket
import time
from machine import Pin
import ubinascii
import gc
import struct

# get pico w's own mac address
def get_own_mac():
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        mac = ubinascii.hexlify(wlan.config('mac')).decode()
        formatted_mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)]).upper()
        return formatted_mac
    except:
        return "mac not found"

# get access point mac
def get_ap_mac():
    try:
        ap = network.WLAN(network.AP_IF)
        if ap.active():
            mac = ubinascii.hexlify(ap.config('mac')).decode()
            formatted_mac = ':'.join([mac[i:i+2] for i in range(0, 12, 2)]).upper()
            return formatted_mac
    except:
        return "ap mac err"
def pad(s, width):
    s = str(s)
    return s + ' ' * (width - len(s)) if len(s) < width else s

# scan visible wifi devices
def scan_for_devices():
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        networks = wlan.scan()

        print(pad("ssid", 20) + pad("mac address", 18) + pad("signal", 8) + "channel")
        print("-" * 60)

        for net in networks:
            ssid = net[0].decode('utf-8') if net[0] else 'hidden'
            bssid = ubinascii.hexlify(net[1]).decode()
            bssid_formatted = ':'.join([bssid[i:i+2] for i in range(0, 12, 2)]).upper()
            signal = net[3]
            channel = net[2]

            print(
                pad(ssid[:19], 20) +
                pad(bssid_formatted, 18) +
                pad(str(signal) + "dBm", 8) +
                f"ch{channel}"
            )


        return networks
    except Exception as e:
        print(f"scan error: {e}")
        return []

# listen for dhcp requests to grab macs
def monitor_dhcp_requests():
    try:
        dhcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dhcp_socket.bind(('', 67))
        dhcp_socket.settimeout(1.0)

        while True:
            try:
                data, addr = dhcp_socket.recvfrom(1024)
                client_ip = addr[0]

                if len(data) >= 28:
                    mac_bytes = data[28:34]
                    mac_str = ubinascii.hexlify(mac_bytes).decode()
                    mac_formatted = ':'.join([mac_str[i:i+2] for i in range(0, 12, 2)]).upper()

                    print(f"dhcp request: {client_ip} -> mac: {mac_formatted}")
                    return mac_formatted

            except OSError:
                continue
            except Exception as e:
                print(f"dhcp error: {e}")
                break

    except Exception as e:
        print(f"dhcp setup fail: {e}")
        return None

# client info collection from http
def enhanced_client_tracking(client_ip, request_data):
    client_info = {}

    own_mac = get_own_mac()
    ap_mac = get_ap_mac()

    print(f"pico sta mac: {own_mac}")
    print(f"pico ap mac: {ap_mac}")

    user_agent = extract_user_agent(request_data)
    headers = parse_http_headers(request_data)

    client_info = {
        "ip": client_ip,
        "pico_sta_mac": own_mac,
        "pico_ap_mac": ap_mac,
        "user_agent": user_agent,
        "headers": headers,
        "timestamp": time.time()
    }

    return client_info

# parse http headers
def parse_http_headers(request_data):
    headers = {}
    try:
        lines = request_data.split('\r\n')
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
    except:
        pass
    return headers

# extract user-agent from request
def extract_user_agent(request_data):
    try:
        lines = request_data.split('\r\n')
        for line in lines:
            if line.lower().startswith('user-agent:'):
                return line.split(':', 1)[1].strip()
    except:
        return "unknown"
    return "not found"

# test mac related functions
def test_mac_functions():
    print("="*50)
    print("mac test")
    print("="*50)

    print("1. pico macs:")
    print(f"   sta: {get_own_mac()}")
    print(f"   ap: {get_ap_mac()}")

    print("2. scanning wifi:")
    networks = scan_for_devices()

    print(f"\n3. total: {len(networks)} networks")

    print("4. listening dhcp (5 sec)...")
    start_time = time.time()
    while time.time() - start_time < 5:
        mac = monitor_dhcp_requests()
        if mac:
            print(f"   caught mac: {mac}")
            break
        time.sleep(0.1)

    print("test done")

if __name__ == "__main__":
    test_mac_functions()


