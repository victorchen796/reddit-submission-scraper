"""
rules module

This module defines functions to change the rules for the submission_scraper
module.
"""

import json
import os

from log import log

# subreddits is a dictionary where each key-value pair is structured as such:
# '<subreddit name>': {
#     'includeString': [
#         '<rules>'
#     ],
#     'excludeString': [
#         '<rules>'
#     ],
#     'includeFlair': [
#         '<rules>'
#     ],
#     'excludeFlair': [
#         '<rules>'
#     ],
#     'showUnflaired': <boolean>,
#     'includeExclude': <boolean>
# }
script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = 'resources/subreddits.json'
subreddits_path = os.path.join(script_dir, rel_path)
with open(subreddits_path, 'r') as f:
    subreddits = json.loads(f.read())


class AlreadyExistsException(Exception):
    """Raised when the inserted value already exists in subreddits.json"""


class DoesNotExistException(Exception):
    """Raised when the removed value does not exist in subreddits.json"""


def write():
    with open(subreddits_path, 'w') as f:
        f.write(json.dumps(subreddits, indent=2))


def exists(name):
    if name in subreddits.keys():
        return True
    return False


def add_subreddit(name):
    if (exists(name)):
        log("ERROR: /r/" + name + " not added to subreddits.json: \"" +
            name + "\" already exists.")
        raise AlreadyExistsException

    subreddits[name] = {
        'includeString': [],
        'excludeString': [],
        'includeFlair': [],
        'excludeFlair': [],
        'showUnflaired': True,
        'includeExclude': False
    }

    write()
    log("Added /r/" + name + " to subreddits.json.")


def remove_subreddit(name):
    if not exists(name):
        log("ERROR: /r/" + name + " not removed from subreddits.json: \"" +
            name + "\" does not exist.")
        raise DoesNotExistException

    del subreddits[name]

    write()
    log("Removed /r/" + name + " from subreddits.json.")


def add_rule(name, rule, value):
    if not exists(name):
        log("ERROR: \"" + rule + "\" for \"" + value + "\" in /r/" + name +
            " was not added: \"" + name + "\" does not exist.")
        raise DoesNotExistException

    if rule == 'includeString':
        if value in subreddits[name]['excludeString']:
            log("ERROR: \"includeString\" for \"" + value + "\" in /r/" +
                name + " was not added: \"excludeString\" for \"" + value +
                "\" already exists.")
            raise AlreadyExistsException
    elif rule == 'excludeString':
        if value in subreddits[name]['includeString']:
            log("ERROR: \"excludeString\" for \"" + value + "\" in /r/" +
                name + " was not added: \"includeString\" for \"" + value +
                "\" already exists.")
            raise AlreadyExistsException

    if value in subreddits[name][rule]:
        log("ERROR: \"" + rule + "\" for \"" + value + "\" in /r/" + name +
            " was not added: \"" + rule + "\" for \"" + value + "\" " +
            "already exists.")
        raise AlreadyExistsException
    else:
        subreddits[name][rule].append(value)
        log("Added \"" + rule + "\" for \"" + value + "\" in /r/" + name +
            " to subreddits.json.")

    subreddits[name][rule].sort()
    write()


def remove_rule(name, rule, value):
    if not exists(name):
        log("ERROR: \"" + rule + "\" for \"" + value + "\" in /r/" + name +
            " was not removed: \"" + name + "\" does not exist.")
        raise DoesNotExistException

    if value not in subreddits[name][rule]:
        log("ERROR: \"" + rule + "\" for \"" + value + "\" in /r/" + name +
            " was not removed: \"" + rule + "\" for \"" + value + "\" " +
            "does not exist.")
        raise DoesNotExistException
    else:
        subreddits[name][rule].remove(value)
        log("Removed \"" + rule + "\" for \"" + value + "\" in /r/" +
            name + " from subreddits.json.")

    write()


def toggle_unflaired(name):
    subreddits[name]['showUnflaired'] = not subreddits[name]['showUnflaired']

    if subreddits[name]['showUnflaired']:
        log("Showing unflaired posts for /r/" + name + ".")
    else:
        log("Hiding unflaired posts for /r/" + name + ".")

    write()


def toggle_include(name):
    subreddits[name]['includeExclude'] = \
        not subreddits[name]['includeExclude']

    if subreddits[name]['includeExclude']:
        log("Toggled include mode for flairs for /r/" + name + ".")
    else:
        log("Toggled exclude mode for flairs for /r/" + name + ".")

    write()


def reset_subreddit(name):
    if not exists(name):
        log("ERROR: rules for /r/" + name + " were not reset: \"" + name +
            "\" does not exist.")
        raise DoesNotExistException

    subreddits[name] = {
        'includeString': [],
        'excludeString': [],
        'includeFlair': [],
        'excludeFlair': [],
        'showUnflaired': True,
        'includeExclude': False
    }

    write()
    log("Rules for /r/" + name + " were reset.")


def reset():
    for name in list(subreddits):
        del subreddits[name]
    write()
