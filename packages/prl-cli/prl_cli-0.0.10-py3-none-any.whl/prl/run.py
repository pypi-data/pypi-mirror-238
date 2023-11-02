import json

import click
import requests
from jsonschema import ValidationError, validate

from .auth import get_auth_token
from .util import (
    BE_HOST,
    FE_HOST,
    RUN_SCHEMA_PATH,
    display_error_and_exit,
    list_test_suites,
    prompt_user_for_suite,
)


@click.group()
def run():
    """
    Commands relating to starting or viewing runs
    """
    pass


@click.command()
@click.argument("config-file", type=click.File("r"), required=True)
def start(config_file: bool):
    """
    Start a new run of a test suite.

    Optionally, if the test suite was defined with "fixed_output" fields
    and if the --use-fixed-output flag is passed, then it will
    use a fixed set of outputs instead of querying the model under test.
    This is useful to evaluate the performance of the evaluator itself.
    """
    try:
        parameters = json.load(config_file)
    except Exception:
        display_error_and_exit("Config file was not valid JSON")

    try:
        with open(RUN_SCHEMA_PATH, "r") as f:
            schema = json.load(f)
            validate(instance=parameters, schema=schema)
    except ValidationError as e:
        display_error_and_exit(
            f"Config file provided did not conform to JSON schema. Message: {e.message}"
        )

    suiteid = prompt_user_for_suite()

    response = requests.post(
        url=f"{BE_HOST}/start_run/",
        headers={"Authorization": get_auth_token()},
        json={"test_suite_id": suiteid, "parameters": parameters},
    )

    if response.status_code == 200:
        run_id = response.json()["run_id"]
        click.secho("Successfully started run.", fg="green")
        click.secho(f"{FE_HOST}/results?run_id={run_id}", bold=True)
    else:
        click.secho("Could not start run", fg="red")


run.add_command(start)
