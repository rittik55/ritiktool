import sys
from rich.console import Console

console = Console()

def run_miflash():
    from miflash.cli import main as miflash_main
    miflash_main()

def show_menu():
    console.print("\n=== [bold cyan]RittikTool Fastboot Flasher[/bold cyan] ===", highlight=False)
    console.print("[dim]https://github.com/rittik55/ritiktool[/dim]\n", highlight=False)
    console.print(" [green]1[/green] - Flash Xiaomi ROM (MiFlash)", highlight=False)
    console.print(" [green]2[/green] - Exit\n", highlight=False)

    while True:
        choice = console.input("Enter choice: ").strip()
        if choice == "1":
            run_miflash()
            break
        elif choice == "2":
            console.print("\nExiting RittikTool.\n", highlight=False)
            sys.exit(0)
        else:
            console.print("Invalid choice!", highlight=False)

def main():
    try:
        show_menu()
    except KeyboardInterrupt:
        console.print("\n\nProcess cancelled by user.\n", highlight=False)
        sys.exit(0)

if __name__ == "__main__":
    main()
