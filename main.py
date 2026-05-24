
from rich.console import Console
from core.memory import init_memory, save_memory
from core.command_router import route_command
from voice.offline_voice_mode import start_offline_voice_mode

console = Console()

def main():
    init_memory()

    console.print("[bold cyan]JARVIS SYSTEM ONLINE AND READY FOR USE[/bold cyan]")
    console.print("[green]Awaiting your command, Janon.[/green]\n")

    while True:
        user_input = input("YOU: ").strip()

        if user_input.lower() in ["exit", "quit", "shutdown"]:
            console.print("[red]JARVIS SHUTTING DOWN. ALL MEMORY WILL BE SAVED AND SYSTEM WILL TERMINATE[/red]")
            save_memory()
            break

        if user_input.lower() in [
            "activate voice mode",
            "start voice mode",
            "voice mode"
        ]:
            start_offline_voice_mode()
            continue

        response = route_command(user_input)

        console.print("\n[bold blue]JARVIS:[/bold blue]")
        console.print(response)
        console.print()

        save_memory(user_input, response)

if __name__ == "__main__":
    main()
