import rich
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from prompt_toolkit import prompt
from inferless_cli.utils.services import get_workspaces_list
from inferless_cli.utils.helpers import (
    decrypt_tokens,
    get_by_keys,
    key_bindings,
    get_workspaces,
    save_tokens,
)
from prompt_toolkit.validation import Validator
from inferless_cli.utils.validators import validate_workspaces


app = typer.Typer(
    no_args_is_help=True,
)


@app.command()
def use():
    rich.print("[bold]Choose a workspace[/bold]\n")
    workspaces = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="fetching...", total=None)

        workspaces = get_workspaces_list()

        progress.remove_task(task)

    workspace_name = prompt(
        "Select a workspace: (Use tab to autocomplete)  ",
        completer=get_workspaces(workspaces),
        complete_while_typing=True,
        key_bindings=key_bindings,
        validator=Validator.from_callable(
            lambda choice: validate_workspaces(choice, workspaces)
        ),
        validate_while_typing=False,
    )
    workspace_id = get_by_keys(workspaces, workspace_name, "name", "is")

    token, refesh, user_id, _, _ = decrypt_tokens()

    rich.print(
        f"[green]Switched to the [white]{workspace_name}[/white] workspace.[/green]"
    )
    save_tokens(token, refesh, user_id, workspace_id, workspace_name)


if __name__ == "__main__":
    app()
