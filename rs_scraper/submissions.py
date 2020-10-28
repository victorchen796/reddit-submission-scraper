"""
submissions module

This module supports storing information about submissions.
This allows the user to open submissions after scraping from reddit.
"""

import json
import os
import webbrowser

from log import log

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = 'resources/submissions.json'
submissions_path = os.path.join(script_dir, rel_path)
submissions = {}


class DoesNotExistException(Exception):
    """Raised when the requested subreddit or submission does not exist"""


def write():
    with open(submissions_path, 'w') as f:
        f.write(json.dumps(submissions, indent=2))


def add_submission(name, title, link, author, time, flair):
    if name not in submissions.keys():
        submissions[name] = []
    submission = {
        'title': title,
        'author': author,
        'link': link,
        'time': time,
        'flair': flair
    }
    submissions[name].append(submission)
    write()
    log("Added new submission to /r/" + name + ".")


def open_submission(name, index):
    # inputted index will be submission index + 1
    if name not in submissions.keys():
        log("Error: submission \"" + str(index) + "\" in /r/" + name +
            " not opened: \"" + name + "\" does not exist.")
        raise DoesNotExistException
    elif len(submissions[name]) < index - 1:
        log("Error: submission \"" + str(index) + "\" in /r/" + name +
            " not opened: submission + \"" + str(index) + "\" does not exist.")
        raise DoesNotExistException
    else:
        webbrowser.open(submissions[name][index - 1]['link'])
        log("Link for submission \"" + str(index) + "\" in /r/" + name +
            " opened: \"" + submissions[name][index - 1]['link'] + "\".")


def clear():
    for name in submissions.keys():
        del submissions[name]
    write()
