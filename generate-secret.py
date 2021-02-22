#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Generates a secret key called <app-name>.key.

Usage:

    ./generate-secret.py <app-name>
"""

import argparse
import secrets
import shutil
from pathlib import Path


DEFAULT_USER = "deploy"

here = Path(__file__).parent

parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
parser.add_argument(
    "app_name",
    metavar="app-name",
    help="name of the app you want to deploy; "
    "must match a key in DEPLOYMENTS in app/configuration.py",
)
parser.add_argument(
    "-u",
    "--user",
    default=DEFAULT_USER,
    help=f"owner of the key [default: {DEFAULT_USER}]",
)
parser.add_argument(
    "-g",
    "--group",
    default=DEFAULT_USER,
    help=f"group of the key [default: {DEFAULT_USER}]",
)
args = parser.parse_args()

key_file = here / f"{args.app_name}.key"
key_file.write_text(secrets.token_urlsafe())
shutil.chown(key_file, user=args.user, group=args.group)
key_file.chmod(0o400)
