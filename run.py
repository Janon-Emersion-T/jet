import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from core.memory import init_memory, save_memory
from core.command_router import route_command
from core.autonomous_learning import ensure_autonomous_learning_worker


def print_banner():
    print("")
    print("========================================")
    print(" JARVIS TERMINAL MODE")
    print("========================================")
    print("Type your command and press ENTER.")
    print("Type 'exit', 'quit', or 'bye' to stop.")
    print("")


def main():
    init_memory()
    ensure_autonomous_learning_worker()
    print_banner()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit", "bye", "stop"}:
                print("Jarvis: Shutting down terminal mode safely.")
                break

            response = route_command(user_input)

            print("")
            print("Jarvis:")
            print(response)
            print("")

            save_memory(user_input, response)

        except KeyboardInterrupt:
            print("\nJarvis: Terminal mode stopped safely.")
            break

        except Exception as error:
            print("")
            print("Jarvis encountered an error:")
            print(error)
            print("")


if __name__ == "__main__":
    main()
