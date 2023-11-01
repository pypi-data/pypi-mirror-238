import sys
import time
from typing import Union

from cloudpathlib.anypath import to_anypath
from prodigy_teams_recipes_sdk import (
    Input,
    InputDataset,
    IntProps,
    Props,
    action_recipe,
)
from prodigy_teams_recipes_sdk.prodigy_teams_pam_sdk import models as pam_models
from prodigy_teams_recipes_sdk.prodigy_teams_pam_sdk.recipe_client import (
    Metrics,
    Settings,
    get_pam_client,
)


@action_recipe(
    title="Hello world",
    description="Print 'hello world'",
    field_props={"n_lines": IntProps(title="Number of lines to print", min=1)},
)
def hello_world(*, n_lines: int):
    """Print 'hello world' {n_lines} times and exit."""
    for i in range(n_lines):
        print(f"{i}: Hello world!")


@action_recipe(
    title="Wait and exit",
    description="Wait and exit with a given code",
    field_props={
        # fmt: off
        "seconds": IntProps(title="Number of seconds to wait"),
        "exit_code": IntProps(title="Exit code to return", description="For example, 1 to exit with an error"),
        # fmt: on
    },
)
def wait_and_exit(*, seconds: int, exit_code: int):
    """Wait for {seconds} and then exit with with code {exit_code}"""
    print(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)
    print(f"Exiting with status code: {exit_code}")
    sys.exit(exit_code)


@action_recipe(
    title="Print file length",
    field_props={"input_file": Props(title="Input file")},
)
def print_file_length(input_file: Input):
    """Print the number of lines in the input file"""
    stream = input_file.load(rehash=True, dedup=True, input_key="text")
    n_lines = len(list(stream))
    print(f"Number of lines: {n_lines}")


@action_recipe(
    title="Print dataset or file length",
    field_props={"data": Props(title="Input data")},
)
def print_dataset_or_file_length(data: Union[Input, InputDataset]):
    """Print the number of examples in an Input file or Dataset"""
    if isinstance(data, Input):
        print("Loading Input Asset")
        stream = data.load(rehash=True, dedup=True, input_key="text")
    else:
        print("Loading Dataset")
        stream = data.load()
    n_examples = len(list(stream))
    print(f"Number of Examples loaded: {n_examples}")


@action_recipe()
def send_dummy_metrics():
    """Call PAM with dummy metrics data"""
    import time

    metrics = Metrics("my_cool_metrics", int)
    metrics.log(1)
    time.sleep(5)
    metrics.log(50)
    time.sleep(5)
    metrics.log(120, final=True)


@action_recipe()
def create_asset(asset_name: str, path: str):
    cfg = Settings()
    if not cfg.validate():
        raise ValueError("Invalid settings")

    assert cfg.broker_id

    pam_client = get_pam_client(cfg.pam_host, cfg.pam_token)

    broker_id = cfg.broker_id
    version = "0.1"
    kind = "input"
    meta = {"loader": "txt"}

    dest = to_anypath(path)
    dest.parent.mkdir(parents=True, exist_ok=True)

    with dest.open("wb") as f:
        f.write(b"This is an example asset")

    response = pam_client.asset.create(
        pam_models.AssetCreating(
            broker_id=broker_id,
            name=asset_name,
            version=version,
            path=path,
            kind=kind,
            meta=meta,
        )
    )

    print("Asset created:", response)
