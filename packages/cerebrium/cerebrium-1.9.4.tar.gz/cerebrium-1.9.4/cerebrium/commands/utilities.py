import json
import sys
import requests
import typer
import os
import yaml
import cerebrium.utils as utils
from cerebrium.api import _check_response, api_url
from cerebrium import __version__ as cerebrium_version
from cerebrium.utils import env
from cerebrium.core import app


@app.command()
def version():
    """
    Print the version of the Cerebrium CLI
    """
    print(cerebrium_version)


@app.command()
def login(
    private_api_key: str = typer.Argument(
        ...,
        help=(
            "Private API key for the user. Your login will be saved in your Cerebrium settings in the home directory on your local machine. "
        ),
    ),
):
    """
    Set private API key for the user in ~/.cerebrium/config.yaml
    """
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = None

    if env == "dev":
        print("❗️❗️Logging in with dev API key❗️❗️")
        key_name = "dev_api_key"
    else:
        key_name = "api_key"

    if config is None:
        config = {key_name: private_api_key}
    else:
        config[key_name] = private_api_key

    with open(config_path, "w") as f:
        yaml.dump(config, f)
    print("✅  Logged in successfully.")


@app.command()
def delete_model(
    name: str = typer.Argument(..., help="Name of the Cortex deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
):
    """
    Delete a model or training job from Cerebrium
    """
    if not api_key:
        api_key = utils.get_api_key()
    print(f'Deleting model "{name}" from Cerebrium...')
    delete_response = requests.delete(
        f"{api_url}/delete-model",
        headers={"Authorization": api_key},
        json={
            "name": name,
        },
    )

    _check_response(delete_response, key="success", error_msg="Error deleting model: ")
    if delete_response.json()["success"]:
        print("✅ Model deleted successfully.")
    else:
        print("❌ Model deletion failed.")


@app.command()
def model_scaling(
    api_key: str = typer.Option("", help="Private API key for the user."),
    name: str = typer.Argument(..., help="The name of your model."),
    cooldown: int = typer.Option(
        None,
        min=0,
        help=(
            "Update the cooldown period of your deployment. "
            "This is the number of seconds before your app is scaled down to 0."
        ),
    ),
    min_replicas: int = typer.Option(
        None,
        min=0,
        help=(
            "Update the minimum number of replicas to keep running for your deployment."
        ),
    ),
    max_replicas: int = typer.Option(
        None,
        min=1,
        help=(
            "Update the maximum number of replicas to keep running for your deployment."
        ),
    ),
):
    """
    Change the cooldown, min and max replicas of your deployment via the CLI
    """
    if not api_key:
        api_key = utils.get_api_key()
    if not api_key:
        utils.cerebriumLog(message="API key must be provided.", level="ERROR")
    if (
        max_replicas is not None
        and min_replicas is not None
        and max_replicas <= min_replicas
    ):
        utils.cerebriumLog(
            message="Maximum replicas must be greater than or equal to minimum replicas.",
            level="ERROR",
        )

    # check all params are not none

    print(f"Updating scaling for model '{name}'...")
    if cooldown is not None:
        print(f"\tSetting cooldown to {cooldown} seconds...")
    if min_replicas is not None:
        print(f"\tSetting minimum replicas to {min_replicas}...")
    if max_replicas is not None:
        print(f"\tSetting maximum replicas to {max_replicas}...")

    body = {}
    if cooldown is not None:
        body["cooldownPeriodSeconds"] = cooldown
    if min_replicas is not None:
        body["minReplicaCount"] = min_replicas
    if max_replicas is not None:
        body["maxReplicaCount"] = max_replicas
    if not body:
        print("Nothing to update...")
        print("Cooldown, minReplicas and maxReplicas are all None ✅")
        sys.exit(0)

    body["name"] = name
    update_response = requests.post(
        f"{api_url}/update-model-scaling",
        headers={"Authorization": api_key},
        json=body,
    )

    _check_response(
        update_response, key="message", error_msg="Error updating scaling: "
    )
    print(json.loads(update_response.text).get("message"))
    sys.exit(0)
