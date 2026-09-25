from pathlib import Path
import miflash.fastboot as fb_mod
from miflash.flash import run_flash_script, select_script, wait_for_device
from miflash.rom import default_scan_root, extract_rom, find_roms, ARCHIVE_EXTENSIONS
from miflash.system import console, detect_device

def choose_rom(roms):
    if not roms:
        console.print("No ROM found in current directory.", highlight=False)
        raise SystemExit(1)

    for i, rom in enumerate(roms, start=1):
        console.print(f"\n [green]{i}[/green] - {str(rom)}", highlight=False)

    console.print("\n [dim]https://github.com/rittik55/ritiktool[/dim]\n", highlight=False)

    while True:
        choice = console.input("Enter your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(roms):
            return roms[int(choice) - 1]
        console.print("Invalid choice!", highlight=False)

def main():
    root = default_scan_root()
    roms = find_roms(root)

    selected = choose_rom(roms)

    is_archive = any(selected.name.lower().endswith(ext) for ext in ARCHIVE_EXTENSIONS)
    if selected.is_file() or is_archive:
        selected = extract_rom(selected)

    script = select_script(selected)

    fb_obj = fb_mod.fastboot()
    wait_for_device(fb_obj.bin)

    run_flash_script(script, fb_obj.bin)

if __name__ == "__main__":
    main()
