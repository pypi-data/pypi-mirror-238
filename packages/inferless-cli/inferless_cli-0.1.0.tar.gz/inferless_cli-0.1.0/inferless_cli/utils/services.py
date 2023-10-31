import rich
import typer
from inferless_cli.utils.api import make_request
from inferless_cli.utils.constants import (
    get_connected_accounts_url,
    get_volumes_list_url,
    get_prefilled_io_url,
    get_templates_list_url,
    validate_token_url,
    get_workspaces,
    get_workspace_models_url,
    rebuild_model_url,
    activate_model_url,
    deactivate_model_url,
    delete_model_url,
    import_model_url,
    upload_io_url,
    set_variables_url,
    update_model_configurations_url,
    validate_import_model_url,
    start_import_url,
    get_model_details_url,
    get_model_code_url,
    initilize_model_upload_url,
    get_signed_url_for_model_upload_url,
    complete_model_upload_url,
)
from inferless_cli.utils.exceptions import ModelNotFoundException, APIException
from inferless_cli.utils.helpers import (
    decrypt_cli_key,
    decrypt_tokens,
    save_tokens,
    validate_jwt,
)


def get_connected_accounts(import_source):
    payload = {
        "import_source": import_source,
    }

    response = make_request(
        get_connected_accounts_url, method="POST", auth=True, data=payload
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    accounts = []
    try:
        accounts = response.json()["details"]
    except KeyError:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )
    return accounts


def get_workspaces_list():
    try:
        response = make_request(get_workspaces, method="POST", auth=True)
    except APIException as e:
        print(e)
        return []
    else:
        if response.status_code != 200:
            print(f"Failed to get data from API. Status code: {response.status_code}")
            return []

        workspaces = response.json()["details"]
        return workspaces


def get_prefilled_io(task_type):
    payload = {"task_type": task_type}

    response = make_request(
        get_prefilled_io_url, method="POST", auth=True, data=payload
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    response_json = response.json()

    if "details" not in response_json:
        api_message = response_json["message"]
        raise APIException(f"Failed to get data from API. Message: {api_message}")

    return response_json["details"]


def get_volumes_list(workspace_id: str):
    payload = {"workspace_id": workspace_id}

    response = make_request(
        get_volumes_list_url, method="POST", auth=True, data=payload
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    if not response.json().get("details"):
        raise APIException("No details in response")

    return response.json()["details"]


def get_templates_list(user_id: str):
    payload = {"user_id": user_id}

    response = make_request(
        get_templates_list_url, method="POST", auth=True, data=payload
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    response_json = response.json()

    if not response_json["success"]:
        raise APIException(
            f"Failed to get data from API. "
            f"Error details: {response_json['details']}"
        )

    return response_json["details"]


def validate_cli_token(key, secret):
    payload = {"access_key": key, "secret_key": secret}
    headers = {"Content-Type": "application/json"}

    response = make_request(
        validate_token_url, method="POST", headers=headers, auth=False, data=payload
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def get_auth_validation():
    error_statement = "[red]Please login to Inferless using `inferless login`[/red]"
    token, _, user_id, workspace_id, workspace_name = decrypt_tokens()
    key, secret = decrypt_cli_key()
    if not key or not secret:
        rich.print(error_statement)
        raise typer.Exit(1)
    if token is None:
        rich.print(error_statement)
        raise typer.Exit(1)
    if not validate_jwt(token):
        try:
            details = validate_cli_token(key, secret)
            if details["access"] and details["refresh"]:
                save_tokens(
                    details["access"],
                    details["refresh"],
                    user_id,
                    workspace_id,
                    workspace_name,
                )
        except Exception:
            rich.print(error_statement)
            raise typer.Exit(1)


def get_workspace_models(workspace_id, filter="NONE"):
    payload = {
        "filter_by": filter,
        "search": "",
        "sort_by": "-updated_at",
        "workspace_id": workspace_id,
    }
    response = make_request(
        get_workspace_models_url, method="POST", auth=True, data=payload
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def rebuild_model(model_id):
    payload = {
        "id": model_id,
    }
    response = make_request(rebuild_model_url, method="POST", auth=True, data=payload)

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def delete_model(model_id):
    payload = {
        "model_id": model_id,
    }
    response = make_request(delete_model_url, method="POST", auth=True, data=payload)

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def activate_model(model_id):
    payload = {
        "min_replica": 0,
        "max_replica": 1,
        "model_id": model_id,
    }
    response = make_request(activate_model_url, method="POST", auth=True, data=payload)

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def deactivate_model(model_id):
    payload = {
        "min_replica": 0,
        "max_replica": 0,
        "model_id": model_id,
    }
    response = make_request(
        deactivate_model_url, method="POST", auth=True, data=payload
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def import_model(data):
    response = make_request(import_model_url, method="POST", auth=True, data=data)

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def upload_io(data):
    response = make_request(upload_io_url, method="POST", auth=True, data=data)

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def update_model_configuration(data):
    response = make_request(
        update_model_configurations_url, method="POST", auth=True, data=data
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def validate_import_model(data):
    response = make_request(
        validate_import_model_url, method="POST", auth=True, data=data
    )

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def set_env_variables(data):
    response = make_request(set_variables_url, method="POST", auth=True, data=data)

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def start_import_model(data):
    response = make_request(start_import_url, method="POST", auth=True, data=data)

    if response.status_code != 200:
        raise APIException(
            f"Failed to get data from API. Status code: {response.status_code}"
        )

    return response.json()["details"]


def get_model_details(id):
    response = make_request(
        f"{get_model_details_url}/{id}/get/", method="GET", auth=True
    )

    if response.status_code == 200:
        return response.json()["details"]

    if response.status_code == 404:
        raise ModelNotFoundException(id)

    raise APIException(
        f"Failed to get data from API. Status code: {response.status_code}"
    )


def get_model_code(id):
    payload = {
        "model_id": id,
    }
    response = make_request(
        f"{get_model_code_url}", method="POST", auth=True, data=payload
    )

    if response.status_code == 200:
        return response.json()["details"]

    if response.status_code == 404:
        raise ModelNotFoundException(id)

    raise APIException(
        f"Failed to get data from API. Status code: {response.status_code}"
    )


def upload_file(selected_file, key):
    if selected_file:
        initialize_response = make_request(
            initilize_model_upload_url, method="POST", data={"key": key}
        )
        initialize_data = initialize_response.json()
        if initialize_data.get("status") == "success" and initialize_data.get(
            "details", {}
        ).get("upload_id"):
            chunk_size = 50 * 1024 * 1024  # 50 MiB
            chunk_count = (selected_file.tell() // chunk_size) + 1

            signed_url_data = make_request(
                get_signed_url_for_model_upload_url,
                method="POST",
                data={
                    "key": key,
                    "upload_id": initialize_data["details"]["upload_id"],
                    "no_of_parts": chunk_count,
                },
            ).json()

            signed_urls = signed_url_data.get("details", {}).get("urls", [])
            multi_upload_array = []

            for upload_count in range(1, chunk_count + 1):
                file_blob = (
                    selected_file.read(chunk_size)
                    if upload_count < chunk_count
                    else selected_file.read()
                )

                pre_signed_url = signed_urls[upload_count - 1].get("signed_url", "")
                if pre_signed_url:
                    headers = {"Content-Type": "application/zip"}
                    upload_response = make_request(
                        pre_signed_url,
                        method="PUT",
                        data=file_blob,
                        auth=False,
                        headers=headers,
                        convert_json=False,
                    )
                    if upload_response.status_code == 200:
                        multi_upload_array.append(
                            {
                                "PartNumber": upload_count,
                                "ETag": upload_response.headers.get("etag").replace(
                                    '"', ""
                                ),
                            }
                        )
            if multi_upload_array:
                complete_data = {
                    "key": key,
                    "upload_id": initialize_data["details"]["upload_id"],
                    "parts": multi_upload_array,
                }
                complete_response = make_request(
                    complete_model_upload_url, data=complete_data, method="POST"
                )

                if complete_response.status_code == 200:
                    return signed_urls[0]["signed_url"].split("?")[0]

    return None
