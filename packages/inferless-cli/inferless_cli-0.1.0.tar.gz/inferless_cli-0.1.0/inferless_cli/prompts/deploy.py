import time
import os
import zipfile
import tempfile
import typer


# from botocore.exceptions import NoCredentialsError
from prompt_toolkit import prompt
from inferless_cli.utils.helpers import (
    check_app_py_in_root,
    check_import_source,
    decrypt_tokens,
    read_json,
    read_yaml,
)
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

# from inferless_cli.utils.constants import (
#     aws_access_key_id,
#     aws_secret_access_key,
#     s3_bucket_name,
# )
from inferless_cli.utils.services import (
    get_model_details,
    import_model,
    set_env_variables,
    update_model_configuration,
    upload_io,
    validate_import_model,
    start_import_model,
    upload_file,
)


# Check if 'app.py' exists in the current directory
def deploy_local(config_file_name):
    if check_app_py_in_root():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            rich.print(
                "Deploying from local directory (make sure you have saved your code)"
            )
            task_id = progress.add_task(description="Getting warmed up...", total=None)
            config = read_yaml(config_file_name)

            _, _, _, workspace_id, _ = decrypt_tokens()

            payload = {
                "name": config.get("name"),
                "details": {
                    "is_auto_build": False,
                    "webhook_url": "",
                    "is_cli_deploy": True,
                },
                "import_source": "FILE",
                "source_framework_type": "PYTORCH",
                "source_location": "LOCAL_FILE",
                "provider": "GITHUB",
                "workspace": workspace_id,
            }
            progress.update(task_id, description="Creating model...")
            details = import_model(payload)

            if "model_import" in details:
                model_id = details["model_import"]["id"]

                progress.update(
                    task_id, description="Uploading model to secure location..."
                )
                with tempfile.TemporaryDirectory() as temp_dir:
                    directory_to_snapshot = os.getcwd()  # Current working directory
                    zip_filename = os.path.join(
                        temp_dir, f"{os.path.basename(directory_to_snapshot)}.zip"
                    )

                    # Create a zip file of the directory
                    with zipfile.ZipFile(
                        zip_filename, "w", zipfile.ZIP_DEFLATED
                    ) as zipf:
                        for root, _, files in os.walk(directory_to_snapshot):
                            for file in files:
                                zipf.write(
                                    os.path.join(root, file),
                                    os.path.relpath(
                                        os.path.join(root, file), directory_to_snapshot
                                    ),
                                )

                    s3_key = f"cli_zip_files/{model_id}/{os.path.basename(directory_to_snapshot)}.zip"
                    with open(zip_filename, "rb") as zip_file:
                        model_url = upload_file(zip_file, s3_key)

                        payload["details"]["model_url"] = model_url
                        payload["id"] = model_id

                _ = import_model(payload)

                inputs = read_json(config["optional"]["input_file_name"])
                outputs = read_json(config["optional"]["output_file_name"])

                _ = upload_io(
                    {"id": model_id, "input_json": inputs, "output_json": outputs}
                )

                progress.update(task_id, description="Validating the model...")
                _ = start_import_model({"id": model_id})

                status, res = poll_model_status(model_id)
                if status == "FAILURE":
                    error_msg = res["model_import"]["import_error"]["message"]
                    rich.print(f"[red]{error_msg}[/red]")
                    raise typer.Abort(1)

                config_payload = {
                    "id": model_id,
                    "configuration": {
                        "cpu": int(config["configuration"]["vcpu"]),
                        "inference_time": config["configuration"]["inference_time"],
                        "is_auto_build": False,
                        "is_dedicated": config["configuration"]["is_dedicated"],
                        "machine_type": config["configuration"]["gpu_type"],
                        "is_serverless": config["configuration"]["is_serverless"],
                        "max_replica": config["configuration"]["max_replica"],
                        "min_replica": config["configuration"]["min_replica"],
                        "memory": int(config["configuration"]["ram"]),
                        "scale_down_delay": config["configuration"]["scale_down_delay"],
                    },
                }
                progress.update(task_id, description="Updating model configuration...")
                _ = update_model_configuration(config_payload)

                if config["env"]:
                    env_payload = {
                        "model_import_id": model_id,
                        "variables": config["env"],
                    }
                    progress.update(
                        task_id, description="Setting environment variables..."
                    )
                    _ = set_env_variables(env_payload)
                _ = validate_import_model({"id": model_id})
                progress.remove_task(task_id)

                rich.print(
                    f"Model import started, here is your model_import_id: [blue]{model_id}[/blue]"
                )


def deploy_git(config_file_name):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        rich.print("Deploying from git (make sure you have pushed your code to git)")
        task_id = progress.add_task(description="Getting warmed up...", total=None)
        config = read_yaml(config_file_name)

        _, _, _, workspace_id, _ = decrypt_tokens()

        payload = {
            "name": config.get("name"),
            "details": {
                "is_auto_build": False,
                "webhook_url": "",
                "github_url": config.get("model_url"),
            },
            "import_source": "GIT",
            "source_framework_type": "PYTORCH",
            "provider": "GITHUB",
            "workspace": workspace_id,
        }
        progress.update(task_id, description="Creating model...")
        details = import_model(payload)

        if "model_import" in details:
            model_id = details["model_import"]["id"]
            inputs = read_json(config["optional"]["input_file_name"])
            outputs = read_json(config["optional"]["output_file_name"])

            _ = upload_io(
                {"id": model_id, "input_json": inputs, "output_json": outputs}
            )

            progress.update(task_id, description="Validating the model...")
            _ = start_import_model({"id": model_id})

            status, res = poll_model_status(model_id)
            if status == "FAILURE":
                error_msg = res["model_import"]["import_error"]["message"]
                rich.print(f"[red]{error_msg}[/red]")
                raise typer.Abort(1)

            config_payload = {
                "id": model_id,
                "configuration": {
                    "cpu": int(config["configuration"]["vcpu"]),
                    "inference_time": config["configuration"]["inference_time"],
                    "is_auto_build": False,
                    "is_dedicated": config["configuration"]["is_dedicated"],
                    "machine_type": config["configuration"]["gpu_type"],
                    "is_serverless": config["configuration"]["is_serverless"],
                    "max_replica": config["configuration"]["max_replica"],
                    "min_replica": config["configuration"]["min_replica"],
                    "memory": int(config["configuration"]["ram"]),
                    "scale_down_delay": config["configuration"]["scale_down_delay"],
                },
            }
            progress.update(task_id, description="Updating model configuration...")
            _ = update_model_configuration(config_payload)

            if config["env"]:
                env_payload = {
                    "model_import_id": model_id,
                    "variables": config["env"],
                }
                progress.update(task_id, description="Setting environment variables...")
                _ = set_env_variables(env_payload)
            _ = validate_import_model({"id": model_id})
            progress.remove_task(task_id)

            rich.print(
                f"Model import started, here is your model_import_id: [blue]{model_id}[/blue]"
            )


def poll_model_status(id):
    while True:
        response = get_model_details(id)
        status = response.get("model_import", {}).get("status")

        if status in ["FILE_STRUCTURE_VALIDATED", "SUCCESS", "FAILURE"]:
            return status, response

        if status is None:
            raise Exception("Status was None, response was: %s" % response)

        if status in ["FILE_STRUCTURE_VALIDATION_FAILED", "IMPORT_FAILED"]:
            raise Exception("Status was %s, response was: %s" % (status, response))

        time.sleep(5)
