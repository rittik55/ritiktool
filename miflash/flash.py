import os
import subprocess
import time
from pathlib import Path

from miflash.system import console

SCRIPT_LABELS = {
    "flash_all": "Flash all [green]without[/green] locking bootloader",
    "flash_all_lock": "Flash all [red]with[/red] lock bootloader",
    "flash_all_except_data_storage": "Flash all [green]except[/green] data storage",
    "flash_all_except_storage": "Flash all [green]except[/green] storage",
}

def available_scripts(rom_dir):
    rom_dir = Path(rom_dir)
    scripts = list(rom_dir.glob("*.sh"))
    if not scripts:
        scripts = list(rom_dir.rglob("*.sh"))
    return sorted(scripts, key=lambda p: p.name)

def select_script(rom_dir):
    rom_dir = Path(rom_dir)
    scripts = available_scripts(rom_dir)

    if not scripts:
        console.print("\n[red]✗ No .sh flash scripts found in this ROM folder![/red]\n", highlight=False)
        raise SystemExit(1)

    for i, path in enumerate(scripts, start=1):
        label = SCRIPT_LABELS.get(path.stem, path.name)
        console.print(f"\n [green]{i}[/green] - {label}", highlight=False)

    while True:
        choice = console.input("\nEnter your [green]choice[/green]: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(scripts):
            return scripts[int(choice) - 1]
        console.print("\n[red]Invalid choice![/red]", highlight=False)

def wait_for_device(fastboot_path):
    with console.status("[white]device not connected...[/white]", spinner="dots") as status:
        while True:
            try:
                result = subprocess.run([fastboot_path, "devices"], capture_output=True, text=True, timeout=5)
            except FileNotFoundError:
                console.print(f"\n[red]✗ fastboot not found at '{fastboot_path}'[/red]\n", highlight=False)
                raise SystemExit(1)
            except subprocess.TimeoutExpired:
                time.sleep(0.4)
                continue

            output = (result.stdout + result.stderr).lower()

            if "no permissions" in output:
                status.update("[red]no permission — check udev rules / device authorization[/red]")
            elif result.stdout.strip():
                console.print("\n[green]device connected[/green]\n", highlight=False)
                return
            else:
                status.update("[white]device not connected...[/white]")

            time.sleep(0.5)

def run_flash_script(script_path, fastboot_path):
    script_path = Path(script_path).resolve()
    env = {**os.environ, "PATH": os.path.dirname(fastboot_path) + os.pathsep + os.environ.get("PATH", "")}

    console.print("\nFlashing process will start now...\n", highlight=False)
    command = ["bash", str(script_path)]

    result = subprocess.run(command, cwd=str(script_path.parent), env=env)

    if result.returncode != 0:
        console.print(f"\n[red]✗ Flashing failed (exit code {result.returncode})[/red]\n", highlight=False)
        raise SystemExit(result.returncode)

    console.print("\n[green]Flashing complete[/green]\n", highlight=False)
