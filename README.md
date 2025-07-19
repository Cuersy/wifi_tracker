## Pico W WiFi & MAC Tracker (MicroPython)

This project is a MicroPython script designed to run on the Raspberry Pi Pico W. It performs passive WiFi scanning, gathers MAC addresses, and collects basic client information via HTTP.

### Features

* **Get Pico W MAC addresses:**

  * Retrieves the MAC address in both STA (station) and AP (access point) modes.

* **Scan nearby WiFi networks:**

  * Lists visible WiFi networks with:

    * SSID
    * BSSID (MAC address)
    * Signal strength (in dBm)
    * Channel number

* **Monitor DHCP requests:**

  * Listens for DHCP request packets to detect connecting devices.
  * Extracts the MAC address from DHCP payloads.
  * Useful for basic device detection, but Pico W does not act as a full router.

* **Enhanced client tracking:**

  * Extracts HTTP request headers and User-Agent from connected clients.
  * Records timestamp, client IP, and other relevant metadata.

* **Lightweight and low-resource:**

  * Compatible with MicroPython running on Pico W.
  * Minimal external dependencies.

### Use Cases

* Basic MAC address logging
* WiFi environment scanning
* Educational network sniffing
* Passive device tracking for embedded systems

### Notes

* MicroPython has limited networking capabilities. Active ARP table inspection or full packet inspection is not supported.
* This script is designed for development and learning purposes. Avoid using it on networks without permission.
