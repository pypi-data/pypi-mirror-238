import json
import os
import sys
import time

import boto3
import click

PRL_PATH = os.path.expanduser("~/.prl")
CREDS_PATH = os.path.join(PRL_PATH, "creds.json")
PLAYGROUND_ENV = os.getenv("PLAYGROUND_ENV")
CLIENT_ID = (
    "59blf1klr2lejsd3uanpk3b0r4"
    if PLAYGROUND_ENV in ["LOCAL", "DEV"]
    else "7r5tn1kic6i262mv86g6etn3oj"
)

client = boto3.client("cognito-idp")


@click.command()
def login():
    """
    Authenticate with PlaygroundRL CLI
    """
    username = click.prompt("email")
    password = click.prompt("password", hide_input=True)

    # TODO: Error handling
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": username, "PASSWORD": password},
        ClientId=CLIENT_ID,
    )

    auth_dict = {
        "refresh_token": response["AuthenticationResult"]["RefreshToken"],
        "access_token": response["AuthenticationResult"]["AccessToken"],
        "id_token": response["AuthenticationResult"]["IdToken"],
        "access_expiry": int(
            time.time() + response["AuthenticationResult"]["ExpiresIn"] - 10
        ),
    }
    auth_json = json.dumps(auth_dict, indent="\t")

    if not os.path.exists(PRL_PATH):
        os.makedirs(PRL_PATH)

    with open(CREDS_PATH, "w") as f:
        f.write(auth_json)


def get_auth_token():
    if not os.path.exists(CREDS_PATH):
        click.echo("Not authenticated. Run the command: prl login.")

    with open(CREDS_PATH, "r") as f:
        auth_dict = json.load(f)

    if time.time() > auth_dict["access_expiry"]:
        # If enough time has elapsed, we need to refresh the token
        try:
            response = client.initiate_auth(
                AuthFlow="REFRESH_TOKEN_AUTH",
                AuthParameters={"REFRESH_TOKEN": auth_dict["refresh_token"]},
                ClientId=CLIENT_ID,
            )
        except:
            click.echo("Your session has expired. Please run the command: prl login.")
            sys.exit()

        auth_dict = {
            "refresh_token": auth_dict["refresh_token"],
            "access_token": response["AuthenticationResult"]["AccessToken"],
            "id_token": response["AuthenticationResult"]["IdToken"],
            "access_expiry": int(
                time.time() + response["AuthenticationResult"]["ExpiresIn"] - 10
            ),
        }
        auth_json = json.dumps(auth_dict, indent="\t")
        # Store the new access token
        with open(CREDS_PATH, "w") as f:
            f.write(auth_json)

    return auth_dict["access_token"]
