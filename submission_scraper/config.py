"""
edit_config module

This module defines functions used to edit the configuration settings
required for PRAW.
"""

import json
import os

import logger

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = "resources/config.json"
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
        logger.log("config.json is not initialized.")
        set_config(None, None, None)
        return False
    else:
        logger.log("config.json is initialized.")
        return True


def set_config(id, secret, agent):
    """Sets values in config.json."""
    configs = {'client_id': id, 'client_secret': secret, 'user_agent': agent}

    with open(config_path, 'w') as f:
        f.write(json.dumps(configs, indent=2))

    logger.log("Updated config.json: " + id + ", " + secret + ", " + agent)
