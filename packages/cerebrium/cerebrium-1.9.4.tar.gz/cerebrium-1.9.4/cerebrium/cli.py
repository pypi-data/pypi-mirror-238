from cerebrium.core import app
from cerebrium.commands.cortex import deploy, build, init  # noqa: E402 F401
from cerebrium.commands.storage import storage, _check_response  # noqa: E402 F401
from cerebrium.commands.utilities import delete_model, model_scaling  # noqa: E402 F401

if __name__ == "__main__":
    app()
