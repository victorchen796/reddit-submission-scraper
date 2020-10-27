"""
edit_config module

This module defines functions used to edit the configuration settings
required for PRAW.
"""

import json
import os

import log

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = 'resources/config.json'
config_path = os.path.join(script_dir, rel_path)


def check_config():
    """
    Checks if config.json's values are null.

    If at least one value is null, change all values to null.
    Returns True if no values are null and False otherwise.
    """
    with open(config_path, 'r') as f:
        configs = json.loads(f.read())

    if (configs['client_id'] is None or configs['client_secret'] is None or
            configs['user_agent'] is None):
        set_config(None, None, None)
        return False
    else:
        return True


def set_config(client_id, client_secret, user_agent):
    """Sets values in config.json."""
    configs = {
        'client_id': client_id,
        'client_secret': client_secret,
        'user_agent': user_agent
    }

    with open(config_path, 'w') as f:
        f.write(json.dumps(configs, indent=2))

    log.log("Set client_id to \"" + client_id + "\".")
    log.log("Set client_secret to \"" + client_secret + "\".")
    log.log("Set user_agent + \"" + user_agent + "\".")


def get_config():
    """Returns the config values as a string"""
    with open(config_path, 'r') as f:
        configs = json.loads(f.read())

    config_string = "client_id = " + configs['client_id'] + \
        "\nclient_secret = " + configs['client_secret'] + \
        "\nuser_agent = " + configs['user_agent'] + "\n"

    log.log("Got config values")
    return config_string


def reset():
    """Clears all fields of config"""
    set_config(None, None, None)
