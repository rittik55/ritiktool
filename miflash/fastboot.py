import shutil

class FastbootDevice:
    def __init__(self, bin_path="fastboot"):
        self.bin = bin_path

def fastboot(device=None):
    path = shutil.which("fastboot") or shutil.which("termux-fastboot") or "fastboot"
    return FastbootDevice(bin_path=path)

Fastboot = fastboot
