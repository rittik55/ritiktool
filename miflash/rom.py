import os
import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path

from miflash.system import console

ARCHIVE_EXTENSIONS = (".tgz", ".tar.gz", ".tar", ".zip", ".7z")

def default_scan_root() -> Path:
    termux_storage = Path("/sdcard/Download")
    if termux_storage.exists():
        return termux_storage
    return Path.cwd()

def find_roms(root: Path):
    candidates = []
    if not root.exists():
        return candidates

    for item in root.iterdir():
        name = item.name.lower()
        if item.is_file() and any(name.endswith(ext) for ext in ARCHIVE_EXTENSIONS):
            candidates.append(item)
        elif item.is_dir() and (list(item.glob("*.sh")) or list(item.rglob("*.sh"))):
            candidates.append(item)

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

    extract_to = archive_path.parent / dest_folder_name
    extract_to.mkdir(parents=True, exist_ok=True)

    with console.status("[white]Extracting ROM archive, please wait...[/white]", spinner="dots"):
        if name_lower.endswith((".tgz", ".tar.gz", ".tar")):
            with tarfile.open(archive_path, "r:*") as tar:
                tar.extractall(path=extract_to)

        elif name_lower.endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)

        elif name_lower.endswith(".7z"):
            subprocess.run(
                ["7z", "x", str(archive_path), f"-o{extract_to}", "-y", "-bso0", "-bsp0"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )

    sh_files = list(extract_to.rglob("*.sh"))
    if sh_files:
        return sh_files[0].parent

    return extract_to
