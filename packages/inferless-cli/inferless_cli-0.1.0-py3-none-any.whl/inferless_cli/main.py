import rich
import typer

from inferless_cli.prompts import model
from .utils.services import get_auth_validation
from .utils.helpers import check_import_source, version_callback
from .prompts import init, login, workspace, token, deploy
from prompt_toolkit import prompt

app = typer.Typer(
    name="Inferless CLI",
    add_completion=False,
    rich_markup_mode="markdown",
    no_args_is_help=True,
    help="""
    Inferless - Deploy Machine Learning Models in Minutes.

    See the website at https://inferless.com/ for documentation and more information
    about running code on Inferless.
    """,
)


@app.callback()
def inferless(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    """
    This function is currently empty because it is intended to be used as a callback for the `inferless` command.
    The `inferless` command is not yet implemented, but this function is included here as a placeholder for future development.
    """
    pass


app.add_typer(token.app, name="token", help="Manage Inferless tokens")
app.add_typer(
    workspace.app,
    name="workspace",
    help="Manage Inferless workspaces",
    callback=get_auth_validation,
)
app.add_typer(
    model.app,
    name="model",
    help="Manage Inferless models",
    callback=get_auth_validation,
)


@app.command("init", help="Initialize a new Inferless model")
def init_def():
    get_auth_validation()
    init.init_prompt()


@app.command("deploy", help="Initialize a new Inferless model")
def init_def():
    get_auth_validation()
    config_file_name = prompt(
        "Enter the name of your config file: ", default="inferless.yaml"
    )
    if check_import_source(config_file_name) == "GIT":
        deploy.deploy_git(config_file_name)
    elif check_import_source(config_file_name) == "LOCAL":
        deploy.deploy_local(config_file_name)
    else:
        rich.print(
            "[red] config file not found [/red] please run [blue] inferless init [/blue] "
        )
        raise typer.Exit(1)


@app.command("login", help="Login to Inferless")
def login_def():
    login.login_prompt()


if __name__ == "__main__":
    app()
