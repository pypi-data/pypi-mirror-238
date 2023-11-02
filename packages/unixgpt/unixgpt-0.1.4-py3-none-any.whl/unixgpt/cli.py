from rich.console import Console
from rich.table import Table

from .argparser import parse
from .models.openai import OpenAIClient
from .library import (
    save_to_library
)
from .utils import (
    execute_unix_command, 
    copy_command_to_clipboard
)
from .prompts import OPENAI_UNIX_COMMAND_PROMPT


ACTIONS = {
    "execute": "e",
    "copy": "c",
    "save": "s",
    "revise": "r",
    "abort": "a"
}

console = Console()


def cli(OPEN_API_KEY):
    args = parse()

    # -i, --input
    input: str = args.input.strip()
    if input:
        handle_input(input, OPEN_API_KEY)


def handle_input(nl_input: str, OPEN_API_KEY: str):
    openai_client = OpenAIClient(OPEN_API_KEY)

    console.print("=> Searching... 👨‍💻")
    unix_command = openai_client.fetch_unix_command(
        user_input=nl_input,
        system_prompt=OPENAI_UNIX_COMMAND_PROMPT,
        model="gpt-3.5-turbo",
    )
    unix_command = unix_command.strip()

    if unix_command.lower() == "unknown":
        console.print("=> Command not found. 🤷‍♂️")

        table = Table()
        table.add_column("Action", style="bold")
        table.add_column("Key", style="bold")
        table.add_column("Description", style="bold")

        actions = [
            {"Name": "Revise", "Key": "r", "Description": "Revise the input"},
            {"Name": "Abort", "Key": "a", "Description": "Abort the program"},
        ]

        for action in actions:
            table.add_row(
                action["Name"],
                action["Key"],
                action["Description"],
            )

        console.print(table)

        handle_unknown_actions(nl_input=nl_input)

    else:
        console.print(f"=> Command found! 🙆‍♂️ [code] {unix_command} [/code]")

        table = Table()
        table.add_column("Action", style="bold")
        table.add_column("Key", style="bold")
        table.add_column("Combineable", style="bold")
        table.add_column("Description", style="bold")

        actions = [
            {"Name": "Execute", "Key": "e", "Combineable": "Yes", "Description": "Execute the command"},
            {"Name": "Copy", "Key": "c", "Combineable": "Yes", "Description": "Copy the command"},
            {"Name": "Save", "Key": "s", "Combineable": "Yes", "Description": "Save the command"},
            {"Name": "Revise", "Key": "r", "Combineable": "No", "Description": "Revise the input"},
            {"Name": "Abort", "Key": "a", "Combineable": "No", "Description": "Abort the program"},
        ]

        for action in actions:
            table.add_row(
                action["Name"],
                action["Key"],
                action["Combineable"],
                action["Description"],
            )

        console.print(table)

        handle_known_actions(unix_command=unix_command, nl_input=nl_input)


def handle_unknown_actions(nl_input: str):
    action_input = input("=> Choose an action key: ").strip().lower()
    
    if not any(act in action_input for act in ACTIONS.values()):
        console.print("=> Enter a valid action. 🤦‍♂️")
        handle_unknown_actions(nl_input)
    
    if ACTIONS["abort"] in action_input:
        handle_abort_action()
        return
    if ACTIONS["revise"] in action_input:
        handle_revise_action(nl_input)
        return


def handle_known_actions(unix_command: str, nl_input: str):
    action_input = input("=> Choose action key(s): ").strip().lower()

    if not any(act in action_input for act in ACTIONS.values()):
        console.print("=> Enter a valid action. 🤦‍♂️")
        handle_known_actions(unix_command, nl_input)

    if ACTIONS["abort"] in action_input:
        handle_abort_action()
        return
    if ACTIONS["revise"] in action_input:
        handle_revise_action(nl_input)
        return
    
    if ACTIONS["copy"] in action_input:
        handle_copy_action(unix_command)
    if ACTIONS["save"] in action_input:
        handle_save_action(unix_command, nl_input)
    if ACTIONS["execute"] in action_input:
        handle_execute_action(unix_command)



def handle_execute_action(unix_command: str):
    console.print("=> Executing... 👨‍💻")
    response = execute_unix_command(unix_command)

    if "success" in response:
        console.print(f"=> {response['success']}")
    else:
        console.print(f"=> {response['error']}")



def handle_copy_action(unix_command: str):
    response = copy_command_to_clipboard(unix_command)

    if "success" in response:
       console.print(f"=> {response['success']}")
    else:
        console.print(f"=> {response['error']}")


def handle_save_action(unix_command: str, nl_input: str):
    save_to_library(nl_input, unix_command)


def handle_revise_action(nl_input: str):
    pass


def handle_abort_action():
    console.print("=> Aborting... 🙍‍♂️")
    exit(1)