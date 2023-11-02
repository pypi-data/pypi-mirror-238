import json
import os
import sys
from io import TextIOWrapper
from typing import Any, Dict

import boto3
import click
import requests
from gql import gql
from jsonschema import ValidationError, validate
from prl.auth import get_auth_token

from .util import (
    BE_HOST,
    FE_HOST,
    SUITE_SCHEMA_PATH,
    display_error_and_exit,
    get_client,
    list_test_suites,
    prompt_user_for_suite,
)

UNARY_OPERATORS = ["is_concise", "is_legal", "valid_json", "valid_yaml"]


@click.group()
def suite():
    """
    Start, create, or view tests and test suites
    """
    pass


def parse_suite_interactive():
    title = click.prompt("Test Suite Title")
    while title == "":
        title = click.prompt("Title cannot be empty. Reenter")

    description = click.prompt("Test Suite Description")

    i = 1
    keep_generating_prompts = True
    tests = []
    while keep_generating_prompts:
        click.secho(f"---Test {i}---", bold=True)
        input_under_test = click.prompt("Input under test (e.g. the prompt)")

        keep_generating_criteria = True
        j = 1
        checks = []
        while keep_generating_criteria:
            operator = click.prompt(f"Operator {j}")
            criteria = click.prompt(f"Criteria {j}")
            checks.append({"criteria": criteria, "operator": operator})
            j += 1

            keep_generating_criteria = click.confirm("Keep Generating Checks?")

        i += 1

        tests.append({"input_under_test": input_under_test, "checks": checks})
        keep_generating_prompts = click.confirm("Keep generating tests?")

    return {"title": title, "description": description, "tests": tests}


def parse_suite_file(file):
    # TODO: Validate file format
    try:
        parsed_json = json.load(file)
    except Exception as e:
        display_error_and_exit("The input file provided is not valid JSON")

    if not os.path.exists(SUITE_SCHEMA_PATH):
        display_error_and_exit(
            "Could not find schema file. The CLI tool is likely misconfigured."
        )

    # Use jsonschema to do most of our validation
    try:
        with open(SUITE_SCHEMA_PATH, "r") as schema_file:
            schema = json.load(schema_file)
            validate(instance=parsed_json, schema=schema)
    except ValidationError as e:
        display_error_and_exit(
            f"The file provided did not conform to the correct format. Validation Error: {e.message}. Look at the examples or the jsonschema to see the correct format."
        )

    # We need to do some custom validation that JSON schema doesn't support
    tests = parsed_json["tests"]
    for test in tests:
        if "input_under_test" not in test and "file_under_test" not in test:
            display_error_and_exit(
                "For all tests, either 'input_under_test' or 'file_under_test' must be provided"
            )
        if "input_under_test" in test and "file_under_test" in test:
            display_error_and_exit(
                "Both input_under_test and file_under_test were defined for a test. Only one should be specified."
            )

        if "file_under_test" in test:
            fp = test["file_under_test"]
            if not os.path.exists(fp):
                display_error_and_exit(f"File does not exist: {fp}")
            if not os.path.isfile(fp):
                display_error_and_exit(f"Path is a directory: {fp}")

        for check in test["checks"]:
            operator = check["operator"]
            if operator not in UNARY_OPERATORS and "criteria" not in check:
                display_error_and_exit(
                    f"'criteria' field must be specified for check with operator: '{operator}'"
                )
    return parsed_json


def upload_file(suite_id: str, file_path: str) -> str:
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{BE_HOST}/upload_file/?test_suite_id={suite_id}",
            files={"file": f},
            headers={"Authorization": get_auth_token()},
        )
        if response.status_code != 200:
            raise Exception(f"Failed to upload file {file_path}")
        return response.json()["file_id"]


def upload_files(suite_id: str, data: Dict[str, Any]):
    # Map from file path to file id
    files = {}
    for test in data["tests"]:
        if "file_under_test" in test:
            file_path = test["file_under_test"]
            files[file_path] = upload_file(suite_id, file_path)
        if "file_fixed_output" in test:
            file_path = test["file_fixed_output"]
            files[file_path] = upload_file(suite_id, file_path)
    return files


def create_test_suite(data: Dict[str, Any]) -> str:
    query = gql(
        f"""
    mutation createTestSuite {{
        updateTestSuite(
            description: "{data['description']}",
            testSuiteId: "0",
            title: "{data['title']}"
        ) {{
            testSuite {{
            description
            id
            org
            title
            }}
        }}
    }}
    """
    )
    result = get_client().execute(query)
    suite_id = result["updateTestSuite"]["testSuite"]["id"]
    return suite_id


def add_tests(data, files, suite_id):
    test_ids = []
    for test in data["tests"]:
        # TODO: Escape chars better
        if "file_under_test" in test:
            file_path = test["file_under_test"]
            input_under_test = files[file_path]
            input_under_test_type = "file"
        else:
            input_under_test = test["input_under_test"]
            input_under_test_type = "raw"

        # TODO: avoid double json
        checks = json.dumps(json.dumps(test["checks"]))
        # TODO: Do this server side

        if "fixed_output" in test:
            fixed_output = test["fixed_output"]
            fixed_output_type = "raw"
        elif "file_fixed_output" in test:
            fixed_output = files[test["file_fixed_output"]]
            fixed_output_type = "file"
        else:
            fixed_output = ""
            fixed_output_type = "raw"

        query = gql(
            f"""
        mutation addUpdateTest {{
              updateTest(
                  sampleOutput: {json.dumps(fixed_output)},
                  sampleOutputType: "{fixed_output_type}",
                  checks: {checks}, 
                  inputUnderTest: {json.dumps(input_under_test)}, 
                  inputUnderTestType: "{input_under_test_type}",
                  testSuiteId: "{suite_id}") {{
                  test {{
                    testId
                  }}
                }}
            }}
            """
        )
        response = get_client().execute(query)
        test_ids.append(response["updateTest"]["test"]["testId"])

    test_id_list = ", ".join([f'"{test_id}"' for test_id in test_ids])
    query = gql(
        f"""
            mutation removeOldTests {{
              removeUnusedTests(
                  testSuiteId: "{suite_id}",
                  inUseTests: [{test_id_list}]
                ) {{
                    success
                }}
            }}
            """
    )
    response = get_client().execute(query)


def parse_suite(interactive: bool, file: TextIOWrapper) -> Dict[str, Any]:
    if not interactive and file is None:
        click.echo(
            "Either --interactive must be passed, or an input file should be specified"
        )
        sys.exit(1)

    if interactive:
        data = parse_suite_interactive()
    else:
        data = parse_suite_file(file)

    return data


@click.command()
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Enable interactive mode instead of reading from file",
)
@click.argument("file", type=click.File("r"), required=False)
def create(interactive: bool, file: str):
    """
    Creates a new test suite.

    There are two modes. In normal operation, inputs are read from a JSON file:

    \tprl suite create <filename>

    In interactive mode, the user is prompted for values:

    \tprl suite create --interactive

        Requires authentication to use.
    """
    # try:
    data = parse_suite(interactive, file)
    suite_id = create_test_suite(data)

    files = upload_files(suite_id, data)

    add_tests(data, files, suite_id)
    # Execute the query on the transport
    click.secho("Successfully created test suite.", fg="green")
    click.secho(f"{FE_HOST}/view?test_suite_id={suite_id}", bold=True)


#  except Exception as e:
# click.secho("Suite Creation Failed. Error: " + str(e), fg="red")


@click.command()
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Enable interactive mode instead of reading from file",
)
@click.argument("file", type=click.File("r"), required=False)
def update(interactive: bool, file: str):
    try:
        suite_id = prompt_user_for_suite()
        data = parse_suite(interactive, file)

        files = upload_files(suite_id, data)

        add_tests(data, files, suite_id)
        # Execute the query on the transport
        click.secho("Successfully updated test suite.", fg="green")
        click.secho(f"{FE_HOST}/view?test_suite_id={suite_id}", bold=True)

    except Exception as e:
        click.secho("Suite Update Failed. Error: " + str(e), fg="red")


@click.command()
def list_():
    """
    List test suites associated with this organization
    """
    suites = list_test_suites()

    suite_text = "\n".join([f"{i}: {s['title']}" for i, s in enumerate(suites)])
    click.echo(suite_text)


suite.add_command(create)
suite.add_command(list_, "list")
suite.add_command(update)
