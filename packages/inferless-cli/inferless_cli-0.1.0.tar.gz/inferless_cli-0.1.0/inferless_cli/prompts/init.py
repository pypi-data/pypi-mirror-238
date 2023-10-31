import typer
from inferless_cli.utils.services import get_connected_accounts
from inferless_cli.utils.helpers import (
    create_yaml,
    decrypt_tokens,
    get_default_machine_values,
    get_upload_methods,
    key_bindings,
    generate_input_and_output_files,
    get_machine_types,
    fernet,
)
from inferless_cli.utils.services import (
    get_connected_accounts,
)
from inferless_cli.utils.validators import (
    has_github_provider,
    validate_machine_types,
    validate_upload_method,
    validate_model_name,
    validate_url,
)
from inferless_cli.utils.constants import (
    github,
    git,
    huggingface,
    default_input_json,
    default_output_json,
    default_input_file_name,
    default_output_file_name,
    io_docs_url,
)
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from rich.progress import Progress, SpinnerColumn, TextColumn
import rich

processing = "processing..."
desc = "[progress.description]{task.description}"


def init_prompt():
    """Prompt the user for configuration parameters."""
    rich.print("Welcome to the Inferless Model Initialization!")
    _, _, _, workspace_id, workspace_name = decrypt_tokens()

    config_file_name = prompt(
        "Enter config file name: ",
        default="%s" % "inferless.yaml",
    )

    import_source = prompt(
        "How do you want to upload the model? (press tab to autocomplete) ",
        completer=get_upload_methods(),
        complete_while_typing=True,
        key_bindings=key_bindings,
        validator=Validator.from_callable(validate_upload_method),
        validate_while_typing=False,
    )

    name = prompt(
        "Model name: ",
        validator=Validator.from_callable(validate_model_name),
    )

    config = {
        "source_framework_type": "PYTORCH",
        "name": name,
        "workspace_id": workspace_id,
        "workspace_name": workspace_name,
    }

    #
    # Get connected accounts
    accounts = []
    if import_source == git:
        with Progress(
            SpinnerColumn(),
            TextColumn(desc),
            transient=True,
        ) as progress:
            task_id = progress.add_task(description=processing, total=None)
            try:
                accounts = get_connected_accounts(import_source)
            except Exception as e:
                rich.print(
                    f"[red]Error while getting connected accounts: {e.__class__.__name__}[/red]\n"
                )
                raise typer.Abort(1)
            progress.remove_task(task_id)

        # exit if no connected accounts found
        if len(accounts) == 0:
            rich.print(
                "[red]No connected accounts found. Please connect your account first.[/red]\n"
            )
            raise typer.Abort(1)

    if "optional" not in config:
        config["optional"] = {}

    if "details" not in config:
        config["details"] = {}

    if "configuration" not in config:
        config["configuration"] = {}

    input_json = {}
    output_json = {}
    input_file_name = default_input_file_name
    output_file_name = default_output_file_name

    if import_source == git:
        if has_github_provider(accounts):
            # Prompt 4a: Model URL
            model_url = prompt(
                "github repo URL: ",
                validator=Validator.from_callable(validate_url),
            )
            input_json = default_input_json
            output_json = default_output_json

            config["model_url"] = model_url
            config["provider"] = github

        else:
            rich.print(
                "No connected Github account found. Please connect your Github account first."
            )
            raise typer.Abort(1)

    is_serverless = typer.confirm("Do you want to use serverless? ", default=False)

    gpu_type = prompt(
        "GPU Type: (press tab to autocomplete) ",
        completer=get_machine_types(),
        complete_while_typing=True,
        key_bindings=key_bindings,
        validator=Validator.from_callable(validate_machine_types),
        validate_while_typing=False,
    )

    is_dedicated = False
    if not is_serverless:
        is_dedicated = typer.confirm("Is the machine type dedicated? ", default=False)
        config["configuration"]["is_dedicated"] = is_dedicated

    if is_serverless:
        is_dedicated = True
        config["configuration"]["is_dedicated"] = True

    # Get default values based on GPU Type and is_dedicated
    default_values = get_default_machine_values(
        gpu_type, "dedicated" if is_dedicated else "shared"
    )

    # Prompts for non-serverless options
    if not is_serverless:
        config["configuration"]["custom_docker_config"] = ""
        config["configuration"]["custom_docker_template"] = "default"

        config["configuration"]["custom_volume_name"] = ""
        config["configuration"]["custom_volume_config"] = "default"

        config["configuration"]["min_replica"] = "1"
        config["configuration"]["max_replica"] = "1"
        config["configuration"]["scale_down_delay"] = "10"

    # Prompts for serverless options
    if is_serverless:
        config["configuration"]["min_replica"] = "1"
        config["configuration"]["max_replica"] = "1"
        config["configuration"]["scale_down_delay"] = "10"

    config["optional"]["input_file_name"] = input_file_name
    config["optional"]["output_file_name"] = output_file_name
    config["configuration"]["inference_time"] = "180"
    config["configuration"]["is_serverless"] = is_serverless
    config["configuration"]["gpu_type"] = gpu_type
    config["configuration"]["is_dedicated"] = is_dedicated
    config["configuration"]["vcpu"] = default_values["cpu"]
    config["configuration"]["ram"] = default_values["memory"]
    config["import_source"] = fernet.encrypt(import_source.encode())
    config["env"] = {}
    config["version"] = "1.0.0"

    create_yaml(config, config_file_name)
    generate_input_and_output_files(
        input_json,
        output_json,
        input_file_name,
        output_file_name,
    )
    rich.print(
        f"{input_file_name} and {output_file_name} files generated successfully! Also pre filled jsons. feel free to modify the files"
    )
    rich.print(
        f"for more information on input and output json please refer our docs: [link={io_docs_url}]{io_docs_url}[/link]\n"
    )

    rich.print("[green]Initialization completed successfully![/green]\n")
