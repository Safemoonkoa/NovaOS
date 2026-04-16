"""
NovaOS CLI
----------
Entry point for the `novaos` command-line interface.

Usage examples:
  novaos --command "Open Chrome and search for NVIDIA stock price"
  novaos --chat
  novaos --dashboard
  novaos --doctor
"""

from __future__ import annotations

import argparse
import logging
import sys

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger("novaos")


BANNER = Text.assemble(
    ("  _   _                   ___  ____  \n", "bold cyan"),
    (" | \\ | | _____   ____ _ / _ \\/ ___| \n", "bold cyan"),
    (" |  \\| |/ _ \\ \\ / / _` | | | \\___ \\ \n", "bold cyan"),
    (" | |\\  | (_) \\ V / (_| | |_| |___) |\n", "bold cyan"),
    (" |_| \\_|\\___/ \\_/ \\__,_|\\___/|____/ \n", "bold cyan"),
    ("\n  The desktop AI that sees, thinks and acts.\n", "dim white"),
)


def cmd_doctor() -> None:
    """Check that all required dependencies are available."""
    console.print(Panel("[bold cyan]NovaOS Doctor[/bold cyan]"))
    checks = [
        ("Python 3.12+", _check_python),
        ("Ollama", _check_ollama),
        ("pyautogui", _check_import("pyautogui")),
        ("mss", _check_import("mss")),
        ("chromadb", _check_import("chromadb")),
        ("gradio", _check_import("gradio")),
        ("easyocr", _check_import("easyocr")),
        ("pynput", _check_import("pynput")),
    ]
    all_ok = True
    for name, check in checks:
        ok, msg = check() if callable(check) else check
        status = "[green]OK[/green]" if ok else "[red]MISSING[/red]"
        console.print(f"  {status}  {name}" + (f" — {msg}" if msg else ""))
        if not ok:
            all_ok = False
    if all_ok:
        console.print("\n[bold green]All checks passed! NovaOS is ready.[/bold green]")
    else:
        console.print("\n[bold yellow]Some dependencies are missing. Run: pip install -r requirements.txt[/bold yellow]")


def _check_python():
    import sys
    ok = sys.version_info >= (3, 12)
    return ok, f"{sys.version}"


def _check_ollama():
    try:
        import ollama  # type: ignore
        ollama.list()
        return True, "running"
    except Exception as e:
        return False, str(e)


def _check_import(module: str):
    def _check():
        try:
            __import__(module)
            return True, ""
        except ImportError:
            return False, f"pip install {module}"
    return _check


def cmd_command(command: str, vision: bool = False) -> None:
    """Execute a single command and print the result."""
    from novaos.core.agent import NovaAgent
    console.print(BANNER)
    console.print(f"[dim]Command:[/dim] {command}\n")
    agent = NovaAgent()
    result = agent.process_command(command, use_vision=vision)
    console.print(Panel(result, title="[cyan]NovaOS[/cyan]", border_style="cyan"))


def cmd_chat() -> None:
    """Start an interactive chat session in the terminal."""
    from novaos.core.agent import NovaAgent
    console.print(BANNER)
    console.print("[dim]Interactive mode. Type 'exit' to quit.[/dim]\n")
    agent = NovaAgent()
    while True:
        try:
            user_input = console.input("[bold cyan]You:[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break
        if user_input.lower() in {"exit", "quit", "bye"}:
            console.print("[dim]Goodbye![/dim]")
            break
        if not user_input:
            continue
        result = agent.process_command(user_input)
        console.print(f"[bold cyan]NovaOS:[/bold cyan] {result}\n")


def cmd_dashboard(port: int = 7860) -> None:
    """Launch the local web dashboard."""
    from novaos.ui.dashboard import launch
    console.print(BANNER)
    console.print(f"[cyan]Starting dashboard on http://localhost:{port}[/cyan]")
    launch(port=port)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="novaos",
        description="NovaOS — The desktop AI that sees, thinks and acts on your computer.",
    )
    sub = parser.add_subparsers(dest="subcommand")

    # novaos run "..."
    run_p = sub.add_parser("run", help="Execute a single command.")
    run_p.add_argument("command", type=str, help="Natural-language command to execute.")
    run_p.add_argument("--vision", action="store_true", help="Enable screen capture.")

    # novaos chat
    sub.add_parser("chat", help="Start an interactive terminal chat session.")

    # novaos dashboard
    dash_p = sub.add_parser("dashboard", help="Launch the local web dashboard.")
    dash_p.add_argument("--port", type=int, default=7860)

    # novaos doctor
    sub.add_parser("doctor", help="Check dependencies and system compatibility.")

    # Legacy: --command flag for backwards compatibility
    parser.add_argument("--command", type=str, help=argparse.SUPPRESS)
    parser.add_argument("--doctor", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--dashboard", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.subcommand == "run":
        cmd_command(args.command, vision=args.vision)
    elif args.subcommand == "chat":
        cmd_chat()
    elif args.subcommand == "dashboard":
        cmd_dashboard(args.port)
    elif args.subcommand == "doctor":
        cmd_doctor()
    elif args.command:
        cmd_command(args.command)
    elif args.doctor:
        cmd_doctor()
    elif args.dashboard:
        cmd_dashboard()
    else:
        console.print(BANNER)
        parser.print_help()


if __name__ == "__main__":
    main()
