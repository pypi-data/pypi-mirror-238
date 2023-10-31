import json
import os
import re
import sys
import tempfile
import time
import zipfile
from typing import Union

import requests
from cerebrium.errors import CerebriumRequestError
from cerebrium.utils import env
import cerebrium.utils as utils
from tenacity import retry, stop_after_delay, wait_fixed
from termcolor import colored
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from yaspin import yaspin
from yaspin.spinners import Spinners

dashboard_url = (
    "https://dev-dashboard.cerebrium.ai"
    if env == "dev"
    else "https://dashboard.cerebrium.ai"
)
api_url = (
    "https://dev-rest-api.cerebrium.ai"
    if env == "dev"
    else "https://rest-api.cerebrium.ai"
)


def _check_payload(method: str, payload: dict) -> None:
    """
    Check that the payload for a given method is valid.

    Args:
        payload (dict): The payload to check.

    Returns:
        bool: True if the payload is valid, False otherwise.
    """
    if method not in ("getUploadUrl", "checkDeploymentStatus"):
        utils.cerebriumLog(
            prefix="ValueError",
            message=f"Method '{method}' not supported",
            level="ERROR",
        )
    if "name" not in payload:
        utils.cerebriumLog(
            prefix="ValueError",
            message=f"Payload for '{method}' must contain 'name' key",
            level="Error",
        )


def _cerebrium_request(
    method: str,
    http_method: str,
    api_key: str,
    payload: Union[dict, None] = None,
    enable_spinner: bool = False,
    pending_text: str = "",
    end_text: str = "",
) -> dict:
    """
    Make a request to the Cerebrium API.

    Args:
        method (str): The server method to use.
        api_key (str): The API key for the Cerebrium account.
        payload (dict): The payload to send with the request.
        enable_spinner (bool): A toggle to enable the spinner.
        pending_text (str): The text to display while the request is pending.
        end_text(str): The text to display when the request is complete.

    Returns:
        dict ('status_code': int, 'data': dict): The response code and data.
    """

    headers = {"Authorization": api_key, "ContentType": "application/json"}
    url = f"{api_url}/{method}"

    # Make a request to the Cerebrium API
    @retry(stop=stop_after_delay(60), wait=wait_fixed(8))
    def _request():
        data = None if payload is None else json.dumps(payload)
        if http_method == "POST":
            response = requests.post(url, headers=headers, data=data, timeout=30)
        else:
            response = requests.get(url, headers=headers, params=payload, timeout=30)
        return {"status_code": response.status_code, "data": json.loads(response.text)}

    if enable_spinner:
        with yaspin(Spinners.arc, text=pending_text, color="magenta"):
            response = _request()
        if response["status_code"] == 200:
            print(f"✅ {end_text}")
        else:
            print(f"✗ {end_text}")
            raise CerebriumRequestError(
                response["status_code"],
                method,
                response["data"],
            )
    else:
        response = _request()
    return response


def _check_response(
    response: requests.Response,
    key: Union[str, None] = None,
    error_msg="API request failed:",
) -> None:
    """
    Check the response from the Cerebrium API for errors.

    Args:
        response (requests.Response): API response.
        key (str): Key param that the response should contain.
        fail_msg (str, optional) = "API request failed": The error message output.

    Returns:
        bool: True if the response is valid, False otherwise.
    """
    message = f"Status code: {response.status_code}\n"
    # Check if the text is valid json or an error message
    response_json = {}
    try:
        response_json = json.loads(response.text or "{}")
    except json.decoder.JSONDecodeError:
        if not response.text:
            message += "Response text is empty, caused json parse error:"
        else:
            message += f"Response text is not valid json: {response.text}"
        utils.cerebriumLog(level="ERROR", message=message, prefix=error_msg)

    if key is not None:
        fail = response.status_code != 200 or (response_json.get(key, None) is None)
    else:
        fail = response.status_code != 200

    if fail:
        if response_json.get("message", None):
            message += response_json.get("message", "")
            utils.cerebriumLog(level="ERROR", message=message, prefix=error_msg)
        else:
            utils.cerebriumLog(level="ERROR", message=response.text, prefix=error_msg)


def _setup_app(headers: dict, body: dict, url=f"{api_url}/setupApp") -> dict:
    """
    Setup the app on Cerebrium for a run or deployment.
    """
    upload_url_response = requests.post(
        url,
        headers=headers,
        json=body,
    )

    _check_response(
        response=upload_url_response,
        key="status",
        error_msg="Error getting upload URL:",
    )
    return upload_url_response.json()


def _poll_app_status(
    api_key: str,
    build_id: str,
    name: str,
    project_id: str,
    disable_animation: bool,
    disable_build_logs: bool,
    hide_public_endpoint: bool,
    jwt: str = "<public_api_key>",
    is_code_change: bool = False,
    timeout_seconds=30 * 60,
    is_run: bool = False,
):
    """
    Poll the deployment status of a conduit.

    Args:
        conduit_name (str): The name of the conduit to check the status of.
        api_key (str): The API key for the Cerebrium account.
    """
    # Check the status of the deployment by polling the Cerebrium API for deployment status
    # Poll the streamBuildLogs endpoint with yaspin for max of 10 minutes to get the build status
    print("----------------------------------------")

    t1 = time.time()
    seen_index = 0
    build_status = "IN_PROGRESS"

    spinner_status = "🧱 Setting Up Builder..."
    if is_code_change:
        spinner_status = "🔨 Syncing code change..."
        build_status = "success"

    error_messages = {
        "disk quota exceeded": "💾 You've run out of space in your /persistent-storage. \n"
        "You can add more by running the command: `cerebrium storage --increase-in-gb <the_amount_in_GB>`"
    }  # Error messages to check for
    if not disable_animation:
        spinner = yaspin(text=spinner_status, color="yellow")
        spinner.start()
    else:
        spinner = None
        print(spinner_status)

    def fail(msg, spinner=None):
        if spinner:
            spinner.write(spinner_status)
            spinner.text = ""
            spinner.fail(msg)
            spinner.stop()
            sys.exit(1)
        else:
            utils.cerebriumLog(level="ERROR", message=msg, prefix="Build Failed with:")

    while (build_status != "success") and (not is_code_change):
        build_status_response = requests.get(
            f"{api_url}/streamBuildLogs",
            params={"buildId": build_id},
            headers={"Authorization": api_key},
        )
        # if the response is not 200, print error and exit
        _check_response(
            response=build_status_response, error_msg="Error getting build logs:"
        )

        build_status = build_status_response.json()["status"]

        if not (response_logs := build_status_response.json()["logs"]):
            continue

        concat_logs = "".join(response_logs)
        logs = concat_logs.split("\n")[:-1]
        if not disable_build_logs:
            for message in logs[seen_index:]:
                if message:
                    match = re.match(
                        r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{9})Z ", message
                    )
                    if (
                        match is not None
                    ):  # If the regex matches the beginning of the string
                        created = match[1]
                        message = message[len(created) + 2 :]
                        for e in error_messages:
                            if e in message.lower():
                                msg = (
                                    f"{message[:message.find(e)]}\n"
                                    "\n🚨 Build failed! \n"
                                    f"{error_messages[e]}"
                                )
                                fail(msg, spinner=spinner)
                    if spinner:
                        spinner.write(f"{message}")
                    else:
                        print(message)
                elif spinner:
                    spinner.write("\n")
                else:
                    print()
        seen_index = len(logs)
        if spinner:
            if build_status == "building":
                spinner.text = "🔨 Building App..."
            elif build_status == "initializing":
                spinner.text = "🛠️ Initializing..."
        time.sleep(1)

        if time.time() - t1 > timeout_seconds:
            msg = "⏲️ Polling build logs timed out."
            fail(msg, spinner=spinner)
        elif build_status in ["build_failure", "init_failure"]:
            msg = f"🚨 Build failed with status: {build_status}"
            fail(msg, spinner=spinner)
        elif build_status == "success":
            break

    if spinner:
        spinner.write(spinner_status)
        spinner.stop()
        spinner.text = ""

    if build_status in ("success", "build_success"):
        msg = "🚀 Build complete!"
        if spinner:
            spinner.ok(msg)
        else:
            print(msg)

    if not is_run:
        env = "dev-" if "dev" in api_key else ""
        print("----------------------------------------")
        if not hide_public_endpoint:
            endpoint = f"https://{env}run.cerebrium.ai/v3/{project_id}/{name}/predict"
            print("\n🛜 Endpoint:", endpoint)
            print("💡 You can call the endpoint with the following curl command:")
            print(
                colored(
                    f"curl -X POST {endpoint} \\\n"
                    "     -H 'Content-Type: application/json' \\\n"
                    f"     -H 'Authorization: {jwt}' \\\n"
                    '     --data \'{"prompt": "Hello World!"}\'',
                    "green",
                )
            )
        url = f"{dashboard_url}/projects/{project_id}/models/{project_id}-{name}"
        print("----------------------------------------")
        print(f"🔗 View builds: {url}?tab=builds")
        print(f"🔗 View runs: {url}?tab=runs")
    else:
        print("----------------------------------------")
        print("🏁 Run finished!")


def upload_cortex_files(
    upload_url: str,
    zip_file_name: str,
    file_list: list,
    disable_syntax_check: bool = False,
    disable_animation: bool = False,
    verbose: bool = False,
) -> bool:
    if file_list == []:
        utils.cerebriumLog(
            level="ERROR",
            message="No files to upload.",
            prefix="Error uploading app to Cerebrium:",
        )

    # Zip all files in the current directory and upload to S3
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, zip_file_name)
        dir_name = os.path.dirname(zip_path)
        os.makedirs(dir_name, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            if not disable_syntax_check:
                print("🔎 Running a quick syntax check...")
                utils.run_pyflakes(files=file_list, print_warnings=True)
                print("✅ Syntax check passed!")

            print("🗂️  Zipping files...")
            for f in file_list:
                if os.path.isfile(f):
                    zip_file.write(f)

        print("⬆️  Uploading to Cerebrium...")
        with open(zip_path, "rb") as f:
            headers = {
                "Content-Type": "application/zip",
            }
            if not disable_animation:
                with tqdm(
                    total=os.path.getsize(zip_path),
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    colour="#EB3A6F",
                ) as pbar:  # type: ignore
                    wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                    upload_response = requests.put(
                        upload_url,
                        headers=headers,
                        data=wrapped_f,  # type: ignore
                        timeout=60,
                        stream=True,
                    )
            else:
                upload_response = requests.put(
                    upload_url,
                    headers=headers,
                    data=f,
                    timeout=60,
                    stream=True,
                )

            _check_response(
                response=upload_response,
                key=None,
                error_msg="Error uploading app to Cerebrium:",
            )
            print("✅ Resources uploaded successfully.")
            return True
