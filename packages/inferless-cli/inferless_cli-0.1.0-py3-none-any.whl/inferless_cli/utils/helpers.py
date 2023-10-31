import json
import os
import sys
import webbrowser
import rich
import typer
import yaml
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from pyfiglet import Figlet
from cryptography.fernet import Fernet
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
import jwt
from datetime import datetime, timezone
from rich.rule import Rule
import importlib.util

from .constants import (
    encryption_key,
    frameworks,
    upload_methods,
    taskType,
    huggingface_type,
    machine_types,
    default_machine_values,
    docs_url,
    inferless_dir_path,
)
import subprocess


fernet = Fernet(encryption_key)

key_bindings = KeyBindings()


def get_default_machine_values(gpu_type, is_dedicated):
    if is_dedicated not in default_machine_values:
        return None
    if gpu_type not in default_machine_values[is_dedicated]:
        return None
    return default_machine_values[is_dedicated][gpu_type]


def save_cli_tokens(key, secret):
    try:
        # Get the user's home directory
        home_dir = os.path.expanduser("~")

        # Create the .inferless directory in the user's home directory if it doesn't exist
        inferless_dir = os.path.join(home_dir, inferless_dir_path)
        os.makedirs(inferless_dir, exist_ok=True)

        # Encrypt the tokens
        encrypted_key = fernet.encrypt(key.encode())
        encrypted_secret = fernet.encrypt(secret.encode())

        # Write the encrypted tokens to the config.txt file
        config_file_path = os.path.join(inferless_dir, "credentials")
        with open(config_file_path, "wb") as config_file:
            config_file.write(encrypted_key + b"\n" + encrypted_secret)
    except Exception as e:
        print(f"An error occurred while saving the tokens: {e}")


def save_tokens(token, refresh_token, user_id, workspace_id, workspace_name):
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Create the .inferless directory in the user's home directory if it doesn't exist
    inferless_dir = os.path.join(home_dir, inferless_dir_path)
    os.makedirs(inferless_dir, exist_ok=True)

    # Encrypt the tokens
    encrypted_token = fernet.encrypt(token.encode())
    encrypted_refresh_token = fernet.encrypt(refresh_token.encode())
    encrypted_user_id = fernet.encrypt(user_id.encode())
    encrypted_workspace_id = fernet.encrypt(workspace_id.encode())
    encrypted_workspace_name = fernet.encrypt(workspace_name.encode())

    # Write the encrypted tokens to the config.txt file
    config_file_path = os.path.join(inferless_dir, "config")
    with open(config_file_path, "wb") as config_file:
        config_file.write(
            encrypted_token
            + b"\n"
            + encrypted_refresh_token
            + b"\n"
            + encrypted_user_id
            + b"\n"
            + encrypted_workspace_id
            + b"\n"
            + encrypted_workspace_name
        )


def create_yaml(config, file_name="inferless.yaml"):
    # Create the YAML file (inferless.yaml)
    try:
        with open(file_name, "w") as yaml_file:
            yaml.dump(config, yaml_file, default_flow_style=False)
    except Exception as e:
        print("Failed to create YAML file: {}".format(e))


@key_bindings.add("c-space")
def _(event):
    """
    Start auto completion. If the menu is showing already, select the next
    completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


def get_frameworks():
    return WordCompleter(
        frameworks,
        ignore_case=True,
    )


def get_task_types():
    return WordCompleter(
        [item["value"] for item in taskType],
        ignore_case=True,
    )


def get_volumes(volumes):
    return WordCompleter(
        [item["name"] for item in volumes],
        ignore_case=True,
    )


def get_templates(templates):
    return WordCompleter(
        [item["name"] for item in templates],
        ignore_case=True,
    )


def get_models(models):
    return WordCompleter(
        [item["name"] for item in models],
        ignore_case=True,
    )


def get_workspaces(workspaces):
    return WordCompleter(
        [item["name"] for item in workspaces],
        ignore_case=True,
    )


def get_machine_types():
    return WordCompleter(
        machine_types,
        ignore_case=True,
    )


def get_huggingface_types():
    return WordCompleter(
        [item["value"] for item in huggingface_type],
        ignore_case=True,
    )


def get_upload_methods():
    return WordCompleter(
        upload_methods,
        ignore_case=True,
    )


def print_inferless():
    f = Figlet(font="standard")
    text = FormattedText(
        [
            ("#d5fd6c", f.renderText("INFERLESS")),
        ]
    )

    print_formatted_text(text)


def version_callback(value: bool):
    if value:
        typer.echo("inferless-cli version: 0.1.0")
        raise typer.Exit()


# Function to decrypt tokens
def decrypt_tokens():
    home_dir = os.path.expanduser("~")

    # Create the .inferless directory in the user's home directory if it doesn't exist
    inferless_dir = os.path.join(home_dir, ".inferless")
    config_file_path = os.path.join(inferless_dir, "config")

    if os.path.exists(config_file_path):
        with open(config_file_path, "rb") as f:
            encrypted_tokens = f.read()

            (
                encrypted_token,
                encrypted_refresh_token,
                encrypted_user_id,
                encrypted_workspace_id,
                encrypted_workspace_name,
            ) = encrypted_tokens.split(b"\n")
            token = fernet.decrypt(encrypted_token).decode()
            refresh_token = fernet.decrypt(encrypted_refresh_token).decode()
            user_id = fernet.decrypt(encrypted_user_id).decode()
            workspace_id = fernet.decrypt(encrypted_workspace_id).decode()
            workspace_name = fernet.decrypt(encrypted_workspace_name).decode()
            return token, refresh_token, user_id, workspace_id, workspace_name
    else:
        return None, None, None, None, None


def decrypt_cli_key():
    home_dir = os.path.expanduser("~")

    # Create the .inferless directory in the user's home directory if it doesn't exist
    inferless_dir = os.path.join(home_dir, ".inferless")
    from cryptography.fernet import InvalidToken

    config_file_path = os.path.join(inferless_dir, "credentials")

    if os.path.exists(config_file_path):
        with open(config_file_path, "rb") as f:
            encrypted_cli_keys = f.read()
            encrypted_key, encrypted_secret = encrypted_cli_keys.split(b"\n")
            try:
                key = fernet.decrypt(encrypted_key).decode()
                secret = fernet.decrypt(encrypted_secret).decode()
                return key, secret
            except InvalidToken:
                print("Invalid credentials. Please run inferless setup")
                sys.exit(1)
    else:
        return None, None


def validate_jwt(jwt_token):
    try:
        # Decode the JWT token without verifying it (no secret key)
        payload = jwt.decode(
            jwt_token, options={"verify_signature": False}, algorithms="HS256"
        )
        # Check if the 'exp' (expiration) claim exists and is in the future
        if "exp" in payload:
            exp_timestamp = payload["exp"]
            if isinstance(exp_timestamp, int):
                current_timestamp = datetime.now(timezone.utc).timestamp()
                if exp_timestamp >= current_timestamp:
                    # Token is not expired
                    return True
                else:
                    # Token has expired
                    return False
            else:
                # 'exp' claim is not an integer
                return False
        else:
            # 'exp' claim is missing
            return False

    except jwt.ExpiredSignatureError:
        # Token has expired
        return False
    except jwt.InvalidTokenError:
        # Token is invalid or tampered with
        return False


def generate_input_and_output_files(
    input_data,
    output_data,
    input_file_name="input.json",
    output_file_name="output.json",
):
    """
    Generate input and output JSON files.

    Args:
        input_data (dict): The data to be saved in the input JSON file.
        output_data (dict): The data to be saved in the output JSON file.
        input_file_name (str): The name of the input JSON file. Default is 'input.json'.
        output_file_name (str): The name of the output JSON file. Default is 'output.json'.

    Returns:
        None
    """
    # Save the input data to input.json
    try:
        with open(input_file_name, "w") as input_file:
            json.dump(input_data, input_file, indent=4)
    except:
        print("An error occurred while saving the input data.")

    # Save the output data to output.json
    try:
        with open(output_file_name, "w") as output_file:
            json.dump(output_data, output_file, indent=4)
    except:
        print("An error occurred while saving the output data.")


def get_by_keys(data, value, key1, key2):
    if data is None:
        raise ValueError("data is None")
    if value is None:
        raise ValueError("value is None")
    if key1 is None:
        raise ValueError("key1 is None")
    if key2 is None:
        raise ValueError("key2 is None")
    for item in data:
        if item.get(key1) == value:
            return item.get(key2)
    return None


def check_path():
    """Checks whether the `inferless` executable is on the path and usable."""

    try:
        subprocess.run(["inferless", "--help"], capture_output=True)
        return
    except FileNotFoundError:
        text = (
            "[red]The `[white]modal[/white]` command was not found on your path!\n"
            "You may need to add it to your path or use `[white]python -m modal[/white]` as a workaround.[/red]\n"
        )
    except PermissionError:
        text = (
            "[red]The `[white]inferless[/white]` command is not executable!\n"
            "You may need to give it permissions or use `[white]python -m inferless[/white]` as a workaround.[/red]\n"
        )
    text += "See more information here:\n\n" f"[link={docs_url}]{docs_url}[/link]\n"

    rich.print(text)
    rich.print(Rule(style="white"))


def open_url(url: str) -> bool:
    try:
        browser = webbrowser.get()
        if isinstance(browser, webbrowser.GenericBrowser):
            return False
        if not hasattr(browser, "open_new_tab"):
            return False
        return browser.open_new_tab(url)
    except webbrowser.Error:
        return False


APP_PY = "app.py"


def check_app_py_in_root():
    if os.path.exists(APP_PY):
        # Import app.py as a module
        spec = importlib.util.spec_from_file_location("app", APP_PY)
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)

        # Check if InferlessPythonModel class is present
        if hasattr(app_module, "InferlessPythonModel"):
            # Check if the class has the required methods
            model_class = app_module.InferlessPythonModel
            required_methods = ["initialize", "infer", "finalize"]
            missing_methods = [
                method
                for method in required_methods
                if not hasattr(model_class, method)
            ]

            if not missing_methods:
                return True, None
            else:
                return (
                    False,
                    f"app.py is present, but InferlessPythonModel is missing the following methods: {', '.join(missing_methods)}",
                )

        else:
            return (
                False,
                "app.py is present, but InferlessPythonModel class is missing.",
            )

    else:
        return os.path.isfile(APP_PY)


def check_import_source(file_name):
    if os.path.isfile(file_name):
        with open("inferless.yaml", "r") as yaml_file:
            inferless_config = yaml.safe_load(yaml_file)
            import_source = inferless_config.get("import_source", "")
            try:
                decrypted_import_source = fernet.decrypt(import_source).decode()
                return decrypted_import_source
            except:
                return None

    return None


def read_yaml(file_name):
    if os.path.isfile(file_name):
        with open(file_name, "r") as yaml_file:
            try:
                inferless_config = yaml.safe_load(yaml_file)
                return inferless_config
            except yaml.YAMLError as exc:
                print(exc)
    return None


def read_json(file_name):
    try:
        with open(file_name, "r") as json_file:
            file_data = json.load(json_file)
            return file_data
    except:
        return None
