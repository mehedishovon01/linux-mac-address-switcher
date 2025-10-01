import os
import random
import re
import subprocess
import sys

class MacChanger:
    MAC_RE = re.compile(r"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}")

    def __init__(self, interface: str, new_mac: str):
        self.interface = interface
        self.new_mac = new_mac.lower() if new_mac else None

    def _require_root(self):
        if os.geteuid() != 0:
            raise PermissionError("This script must be run as root (use sudo).")

    def _run(self, cmd: list) -> str:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()

    def get_current_mac(self) -> str:
        output = self._run(["ip", "link", "show", "dev", self.interface])
        match = self.MAC_RE.search(output)
        return match.group(0) if match else ""

    def _validate_mac(self, mac: str) -> bool:
        return bool(self.MAC_RE.fullmatch(mac))

    def _gen_random_mac(self) -> str:
        first = 0x02  # Locally administered unicast
        parts = [first] + [random.randint(0x00, 0xff) for _ in range(5)]
        return ':'.join(f"{p:02x}" for p in parts)

    def set_mac(self, new_mac: str):
        self._run(["ip", "link", "set", self.interface, "down"])
        self._run(["ip", "link", "set", self.interface, "address", new_mac])
        self._run(["ip", "link", "set", self.interface, "up"])

    def change_mac(self):
        self._require_root()

        current = self.get_current_mac()
        print(f"Current MAC for {self.interface}: {current}")

        if self.new_mac:
            if not self._validate_mac(self.new_mac):
                raise ValueError("Invalid MAC format. Expected aa:bb:cc:dd:ee:ff")
            new_mac = self.new_mac
        else:
            new_mac = self._gen_random_mac()
            print(f"No MAC provided — generated random MAC: {new_mac}")

        print(f"Changing {self.interface} MAC to {new_mac}...")
        self.set_mac(new_mac)

        after = self.get_current_mac()
        print(f"New MAC for {self.interface}: {after}")

        if after and after.lower() == new_mac.lower():
            print("MAC successfully changed.")
        else:
            print("Warning: MAC change did not apply correctly.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python ./mac_changer.py <interface> [new_mac]")
        sys.exit(1)

    iface = sys.argv[1]
    mac = sys.argv[2] if len(sys.argv) > 2 else ""

    changer = MacChanger(iface, mac)
    try:
        changer.change_mac()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
