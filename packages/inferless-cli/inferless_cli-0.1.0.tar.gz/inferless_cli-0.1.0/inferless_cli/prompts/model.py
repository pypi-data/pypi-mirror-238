from datetime import datetime
from prompt_toolkit.validation import Validator
import typer
from typing import Annotated, Optional
from prompt_toolkit import prompt
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.console import Console
from inferless_cli.utils.helpers import (
    decrypt_tokens,
    get_models,
    get_by_keys,
    key_bindings,
)

from inferless_cli.utils.services import (
    activate_model,
    deactivate_model,
    delete_model,
    get_workspace_models,
    rebuild_model,
    get_model_code,
)
from inferless_cli.utils.validators import validate_models


app = typer.Typer(
    no_args_is_help=True,
)

processing = "processing..."
desc = "[progress.description]{task.description}"
no_models = "[red]No models found in your workspace[/red]"
model_id_string = "Model ID"


@app.command(
    "rebuild",
    help="rebuild a model.",
)
def rebuild(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    models = {}
    _, _, _, workspace_id, _ = decrypt_tokens()
    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        models = get_workspace_models(workspace_id=workspace_id)

        progress.remove_task(task_id)

    if len(models["models"]["models"]) == 0:
        rich.print(no_models)
        raise typer.Exit(1)

    if model_id is None:
        modal_name = prompt(
            "Select the model you want to rebuild: ",
            completer=get_models(models=models["models"]["models"]),
            complete_while_typing=True,
            key_bindings=key_bindings,
            validator=Validator.from_callable(
                lambda choice: validate_models(
                    choice, models=models["models"]["models"]
                )
            ),
            validate_while_typing=False,
        )

        model_id = get_by_keys(models["models"]["models"], modal_name, "name", "is")

    validate = typer.confirm("Are you sure you want to rebuild this model? (y/n): ")
    if validate:
        model_name = None
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            model_name = get_by_keys(
                models["models"]["models"],
                model_id,
                "id",
                "name",
            )
            if model_name is None:
                rich.print(f"Model with id: [bold]{model_id}[/bold] not found")
                typer.Exit(1)

            _ = rebuild_model(model_id)

            progress.remove_task(task_id)

        rich.print(f"Rebuilding model: [bold]{model_name}[/bold]")


@app.command(
    "list",
    help="List all models.",
)
def list():
    _, _, _, workspace_id, _ = decrypt_tokens()

    models = {}

    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        models = get_workspace_models(workspace_id=workspace_id)

        progress.remove_task(task_id)

    if len(models["models"]["models"]) == 0:
        rich.print(no_models)
        raise typer.Exit(1)

    table = Table(
        title="Model List",
        box=rich.box.ROUNDED,
        title_style="bold Black underline on white",
    )
    table.add_column("ID", style="yellow")
    table.add_column(
        "Name",
    )
    table.add_column("Created At")
    table.add_column("Updated At")
    table.add_column("Is Serverless")
    table.add_column("Status")

    for model in models["models"]["models"]:
        created_at = datetime.fromisoformat(model["created_at"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        updated_at = datetime.fromisoformat(model["updated_at"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        table.add_row(
            model["id"],
            model["name"],
            created_at,
            updated_at,
            "Yes" if model["is_serverless"] else "No",
            model["status"],
        )

    total_models = models["models"]["total_models"]
    total_models_deployed = models["models"]["total_models_deployed"]

    console = Console()
    console.print(table)
    console.print("\n")
    # Display total models and total models deployed
    console.print(f"Total Models: [bold]{total_models}[/bold]\n")
    console.print(f"Total Models Deployed: [bold]{total_models_deployed}[/bold]\n")


@app.command(
    "deactivate",
    help="deactivate a model.",
)
def deactivate(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    _, _, _, workspace_id, _ = decrypt_tokens()

    models = {}

    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        models = get_workspace_models(workspace_id=workspace_id, filter="ACTIVE")

        progress.remove_task(task_id)

    if len(models["models"]["models"]) == 0:
        rich.print("[red]No Active models found in your workspace[/red]")
        raise typer.Exit(1)

    if model_id is None:
        modal_name = prompt(
            "Select the model you want to deactivate: ",
            completer=get_models(models["models"]["models"]),
            complete_while_typing=True,
            key_bindings=key_bindings,
            validator=Validator.from_callable(
                lambda choice: validate_models(choice, models["models"]["models"])
            ),
            validate_while_typing=False,
        )

        model_id = get_by_keys(models["models"]["models"], modal_name, "name", "is")

    validate = typer.confirm("Are you sure you want to deactivate this model? (y/n): ")
    if validate:
        model_name = None
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            model_name = get_by_keys(
                models["models"]["models"],
                model_id,
                "id",
                "name",
            )
            if model_name is None:
                rich.print(f"Model with id: [bold]{model_id}[/bold] not found")
                typer.Exit(1)

            _ = deactivate_model(model_id)

            progress.remove_task(task_id)
        rich.print(f"Deactivating model: [bold]{model_name}[/bold]")


@app.command(
    "activate",
    help="activate a model.",
)
def activate(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    _, _, _, workspace_id, _ = decrypt_tokens()

    models = {}

    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        models = get_workspace_models(workspace_id=workspace_id, filter="INACTIVE")

        progress.remove_task(task_id)

    if len(models["models"]["models"]) == 0:
        rich.print("[red]No Deactivated models found in your workspace[/red]")
        raise typer.Exit(1)

    if model_id is None:
        modal_name = prompt(
            "Select the model you want to activate: ",
            completer=get_models(models["models"]["models"]),
            complete_while_typing=True,
            key_bindings=key_bindings,
            validator=Validator.from_callable(
                lambda choice: validate_models(choice, models["models"]["models"])
            ),
            validate_while_typing=False,
        )

        model_id = get_by_keys(models["models"]["models"], modal_name, "name", "is")

    # validate = typer.confirm("Are you sure you want to activate this model? (y/n): ")
    # if validate:
    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)
        model_name = get_by_keys(
            models["models"]["models"],
            model_id,
            "id",
            "name",
        )
        if model_name is None:
            rich.print(f"Model with id: [bold]{model_id}[/bold] not found")
            typer.Exit(1)

        _ = activate_model(model_id)

        progress.remove_task(task_id)

        rich.print(f"Activating model: [bold]{model_name}[/bold]")


@app.command(
    "delete",
    help="delete a model.",
)
def delete(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    _, _, _, workspace_id, _ = decrypt_tokens()

    models = {}

    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        models = get_workspace_models(workspace_id=workspace_id)

        progress.remove_task(task_id)

    if len(models["models"]["models"]) == 0:
        rich.print(no_models)
        raise typer.Exit(1)

    if model_id is None:
        modal_name = prompt(
            "Select the model you want to delete: ",
            completer=get_models(models["models"]["models"]),
            complete_while_typing=True,
            key_bindings=key_bindings,
            validator=Validator.from_callable(
                lambda choice: validate_models(choice, models["models"]["models"])
            ),
            validate_while_typing=False,
        )

        model_id = get_by_keys(models["models"]["models"], modal_name, "name", "is")

    validate = typer.confirm("Are you sure you want to delete this model? (y/n):")
    if validate:
        model_name = None
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            model_name = get_by_keys(
                models["models"]["models"],
                model_id,
                "id",
                "name",
            )
            if model_name is None:
                rich.print(f"Model with id: [bold]{model_id}[/bold] not found")
                typer.Exit(1)
            _ = delete_model(model_id)

            progress.remove_task(task_id)
        rich.print(f"Model model: [bold]{model_name}[/bold]")


@app.command("info", help="Get model details.")
def info(
    model_id: Annotated[Optional[str], typer.Option(help="Model ID")] = None,
):
    _, _, _, workspace_id, _ = decrypt_tokens()

    models = {}

    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        models = get_workspace_models(workspace_id=workspace_id)

        progress.remove_task(task_id)

    if len(models["models"]["models"]) == 0:
        rich.print(no_models)
        raise typer.Exit(1)

    if model_id is None:
        modal_name = prompt(
            "Select the model you want to get details for: ",
            completer=get_models(models["models"]["models"]),
            complete_while_typing=True,
            key_bindings=key_bindings,
            validator=Validator.from_callable(
                lambda choice: validate_models(choice, models["models"]["models"])
            ),
            validate_while_typing=False,
        )

        model_id = get_by_keys(models["models"]["models"], modal_name, "name", "id")

    model_name = None
    data = None
    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        model_name = get_by_keys(
            data=models["models"]["models"],
            value=model_id,
            key1="id",
            key2="name",
        )
        if model_name is None:
            rich.print(f"Model with id: [bold]{model_id}[/bold] not found")
            typer.Exit(1)
        data = get_model_code(model_id)

        progress.remove_task(task_id)

    if data is not None:
        rich.print("[bold]Details:[/bold]")
        rich.print(f"[green]Name:[/green] {model_name}")
        rich.print(f"[green]ID:[/green] {model_id}")
        rich.print(f"[green]URL:[/green] {data['location']}\n")
