import os
import shutil
import subprocess
import tarfile
import zipfile
from pathlib import Path

from miflash.system import console

ARCHIVE_EXTENSIONS = (".tgz", ".tar.gz", ".tar", ".zip", ".7z")
SKIP_DIRS = {"Android", ".git", "node_modules", ".cache", "cache"}
MIN_ROM_SIZE_BYTES = 800 * 1024 * 1024


def default_scan_root() -> Path:
    internal_storage = Path("/sdcard")
    if internal_storage.exists():
        return internal_storage
    return Path.cwd()


def find_roms(root: Path):
    candidates = []
    if not root.exists():
        return candidates

    extracted_target = Path("/sdcard/Download/hybrid-fastboot-rom")
    if extracted_target.exists() and extracted_target.is_dir():
        if list(extracted_target.glob("*.sh")) or list(extracted_target.rglob("*.sh")):
            candidates.append(extracted_target)

    with console.status("[white]Scanning storage for ROM files (>= 800MB)...[/white]", spinner="dots"):
        for dirpath, dirnames, filenames in os.walk(str(root), topdown=True, followlinks=False):
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS and d != "hybrid-fastboot-rom"]

            p_dir = Path(dirpath)
            for fname in filenames:
                name_lower = fname.lower()
                if any(name_lower.endswith(ext) for ext in ARCHIVE_EXTENSIONS):
                    fpath = p_dir / fname
                    try:
                        if fpath.stat().st_size >= MIN_ROM_SIZE_BYTES:
                            candidates.append(fpath)
                    except OSError:
                        pass

    return candidates


def extract_rom(archive_path: Path) -> Path:
    archive_path = Path(archive_path).resolve()
    target_dir = Path("/sdcard/Download/hybrid-fastboot-rom")

    if archive_path.is_dir():
        sh_files = list(archive_path.rglob("*.sh"))
        return sh_files[0].parent if sh_files else archive_path

    name_lower = archive_path.name.lower()

    if target_dir.exists():
        console.print("[yellow]Cleaning previous files in hybrid-fastboot-rom...[/yellow]")
        shutil.rmtree(target_dir, ignore_errors=True)

    target_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"\n[cyan]Extracting directly to:[/cyan] [dim]{target_dir}[/dim]")

    if name_lower.endswith((".7z", ".zip", ".tgz", ".tar.gz", ".tar")):
        res = subprocess.run(
            ["7z", "x", str(archive_path), f"-o{target_dir}", "-y", "-bso0", "-bsp1"]
        )
        if res.returncode != 0:
            console.print("\n[yellow]Running alternative extractor...[/yellow]")
            subprocess.run(["7z", "x", str(archive_path), f"-o{target_dir}", "-y"])

    items = list(target_dir.iterdir())
    if len(items) == 1 and items[0].is_dir():
        inner_folder = items[0]
        for sub_item in inner_folder.iterdir():
            shutil.move(str(sub_item), str(target_dir / sub_item.name))
        inner_folder.rmdir()

    console.print("[green]Extraction complete directly in hybrid-fastboot-rom![/green]\n")

    sh_files = list(target_dir.rglob("*.sh"))
    if sh_files:
        return sh_files[0].parent

    return target_dir
