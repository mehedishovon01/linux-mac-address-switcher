# MAC Address Changer (Linux / Ubuntu)

A python class-based script for changing your MAC address on Linux (tested on Ubuntu).  

It can:
- Print the current MAC address of a network interface
- Change the MAC (to a user-provided value or a randomly generated one)
- Verify the change

> Requires root privileges (use `sudo`).

--------------

## 1. Find Network Interface Name

Before running the script, you need the correct **interface name** (e.g., `enp34s0`, `wlan0`).  
Run the following command:
```
ip link show
```
Example Output:
```
2: enp34s0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    link/ether 04:7c:16:88:e3:46 brd ff:ff:ff:ff:ff:ff
3: wlan0: <BROADCAST,MULTICAST> ...
    link/ether b8:27:eb:45:67:89 brd ff:ff:ff:ff:ff:ff
```
```
enp34s0 → Ethernet interface
wlan0 → WiFi interface
```
Choose the one you want to change.

# Usage
## 2. Make the script executable:
```
chmod +x mac_changer.py
```
Change to a random MAC
```
sudo python mac_changer.py enp34s0
```
Change to a specific MAC
```
sudo python mac_changer.py enp34s0 00:11:22:33:44:55
```

If you don’t provide a MAC, a random one will be generated.

## 3. Example Output
```
Current MAC for enp34s0: 04:7c:16:88:e3:46
No MAC provided — generated random MAC: 02:1f:9b:cc:3d:7a
Changing enp34s0 MAC to 02:1f:9b:cc:3d:7a...
New MAC for enp34s0: 02:1f:9b:cc:3d:7a
MAC successfully changed.
```

## 4. Restore Original MAC
If your internet breaks after a change, set your original MAC back:
```
sudo python mac_changer.py enp34s0 04:7c:16:88:e3:46
```
## 5. Notes
Only change your MAC for testing or learning purposes.

`Some networks (e.g., corporate, ISP) may block you if the MAC doesn’t match their records`
