import json
import sys
import requests
import typer
from cerebrium.api import api_url, _check_response
import cerebrium.utils as utils
from cerebrium.core import app


@app.command()
def storage(
    increase_in_gb: int = typer.Option(
        0,
        help="Increase storage capacity by the given number of GB. Warning: storage cannot be decreased once allocated and this will increase your monthly bill.",
        min=0,
    ),
    get_capacity: bool = typer.Option(
        False,
        help="Get the current storage capacity you have allocated to this project.",
    ),
    api_key: str = typer.Option(
        None,
        help="Private API key for your project. If not provided, will use the API key from your cerebrium login.",
    ),
):
    """A lightweight utility to view persistent storage capacity and increase it."""
    if not api_key:
        api_key = utils.get_api_key()
    if not api_key:
        utils.cerebriumLog(message="Please provide an API key.", level="ERROR")

    if get_capacity:
        response = requests.get(
            f"{api_url}/get-storage-capacity",
            headers={"Authorization": api_key},
        )

        _check_response(response, key="capacity")
        print(f"📦 Storage capacity: {json.loads(response.text).get('capacity')} GB")
        sys.exit(0)

    if increase_in_gb:
        print(f"📦 Increasing storage capacity by {increase_in_gb}GB...")
        response = requests.post(
            f"{api_url}/increase-storage-capacity",
            headers={"Authorization": api_key},
            json={"increaseInGB": increase_in_gb},
        )

        _check_response(response, key="capacity")
        new_size = json.loads(response.text).get("capacity")
        print(f"✅ Storage capacity successfully increased to {new_size} GB.")
        sys.exit(0)
