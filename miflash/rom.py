import os
import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path

from miflash.system import console

ARCHIVE_EXTENSIONS = (".tgz", ".tar.gz", ".tar", ".zip", ".7z")
SKIP_DIRS = {"Android", ".git", "node_modules", ".cache", "cache"}


def default_scan_root() -> Path:
    internal_storage = Path("/sdcard")
    if internal_storage.exists():
        return internal_storage
    return Path.cwd()


def find_roms(root: Path):
    candidates = []
    if not root.exists():
        return candidates

    with console.status("[white]Scanning internal storage for ROM files...[/white]", spinner="dots"):
        for dirpath, dirnames, filenames in os.walk(str(root), topdown=True, followlinks=False):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS]

            p_dir = Path(dirpath)

            for fname in filenames:
                name_lower = fname.lower()
                if any(name_lower.endswith(ext) for ext in ARCHIVE_EXTENSIONS):
                    candidates.append(p_dir / fname)

    return sorted(candidates, key=lambda p: p.name)


def extract_rom(archive_path: Path) -> Path:
    archive_path = Path(archive_path).resolve()
    name_lower = archive_path.name.lower()

    if name_lower.endswith(".tar.gz"):
        dest_folder_name = archive_path.name[:-7]
    elif archive_path.suffix.lower() in ARCHIVE_EXTENSIONS:
        dest_folder_name = archive_path.stem
    else:
        dest_folder_name = archive_path.name

    # Download फ़ोल्डर के अंदर hybrid-fastboot-rom डायरेक्टरी
    base_extract_dir = Path("/sdcard/Download/hybrid-fastboot-rom")
    extract_to = base_extract_dir / dest_folder_name
    extract_to.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[cyan]Extracting to:[/cyan] [dim]{extract_to}[/dim]")

    if name_lower.endswith((".7z", ".zip", ".tgz", ".tar.gz", ".tar")):
        res = subprocess.run(
            ["7z", "x", str(archive_path), f"-o{extract_to}", "-y", "-bso0", "-bsp1"]
        )
        if res.returncode != 0:
            console.print("\n[yellow]Running alternative extractor...[/yellow]")
            subprocess.run(["7z", "x", str(archive_path), f"-o{extract_to}", "-y"])

    console.print("[green]✔ Extraction complete![/green]\n")

    sh_files = list(extract_to.rglob("*.sh"))
    if sh_files:
        return sh_files[0].parent

    return extract_to
