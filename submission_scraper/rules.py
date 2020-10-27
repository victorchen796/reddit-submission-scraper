"""
rules module

This module defines functions to change the rules for the submission_scraper
module.
"""

# TODO: create a class to store subreddits instead of dictionaries

import json
import os

import log

script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]
rel_path = 'resources/subreddits.json'
subreddits_path = os.path.join(script_dir, rel_path)


class AlreadyExistsException(Exception):
    """Raised when the inserted value already exists in subreddits.json"""


class DoesNotExistException(Exception):
    """Raised when the removed value does not exist in subreddits.json"""


class Subreddits:

    def __init__(self):
        """
        self.subs is structured as such:
        {
            '<subreddit name>': {
                'includeString': [
                    '<rules>'
                ],
                'excludeString': [
                    '<rules>'
                ],
                'includeFlair': [
                    '<rules>'
                ],
                'excludeFlair': [
                    '<rules>'
                ],
                'showUnflaired': <boolean>,
                'includeExclude': <boolean>
            }
        }
        """
        with open(subreddits_path, 'r') as f:
            self.subs = json.loads(f.read())

    def write(self):
        with open(subreddits_path, 'w') as f:
            f.write(json.dumps(self.subs), indent=2)

    def exists(self, name):
        if name in self.subs.keys():
            return True
        return False

    def add_subreddit(self, name):
        if (self.exists(name)):
            log.log("Error: /r/" + name + " not added to subreddits.json: \"" +
                    name + "\" already exists.")
            raise AlreadyExistsException

        self.subs[name] = {
            'includeString': None,
            'excludeString': None,
            'includeFlair': None,
            'excludeFlair': None,
            'showUnflaired': True,
            'includeExclude': True
        }

        self.subs.write()
        log.log("Added /r/" + name + " to subreddits.json.")

    def remove_subreddit(self, name):
        if not self.exists(name):
            log.log("Error: /r/" + name + " not removed from " +
                    "subreddits.json: \"" + name + "\" does not exist.")
            raise DoesNotExistException

        del self.subs[name]

        self.subs.write()
        log.log("Removed /r/" + name + " from subreddits.json.")

    def add_filter(self, name, rule, value):
        if not self.exists(name):
            log.log("Error: \"" + rule + "\" for \"" + value + "\" in /r/" +
                    name + " was not added: \"" + name + "\" does not exist.")
            raise DoesNotExistException

        if value in self.subs[name][rule]:
            log.log("Error: \"" + rule + "\" for \"" + value + "\" in /r/" +
                    name + " was not added: \"" + rule + "\" for \"" +
                    value + "\" already exists.")
            raise AlreadyExistsException
        else:
            self.subs[name][rule].append(value)
            log.log("Added \"" + rule + "\" for \"" + value + "\" in /r/" +
                    name + " to subreddits.json.")

        self.subs[name][rule].sort()
        self.write()

    def remove_filter(self, name, rule, value):
        if not self.exists(name):
            log.log("Error: \"" + rule + "\" for \"" + value + "\" in /r/" +
                    name + " was not removed: \"" + name + "\" does not " +
                    "exist.")
            raise DoesNotExistException

        if value not in self.subs[name][rule]:
            log.log("Error: \"" + rule + "\" for \"" + value + "\" in /r/" +
                    name + " was not remove: \"" + rule + "\" for \"" + value +
                    "\" does not exist.")
            raise DoesNotExistException
        else:
            self.subs[name][rule].remove(value)
            log.log("Removed \"" + rule + "\" for \"" + value + "\" in /r/" +
                    name + " from subreddits.json.")

        self.write()

    def toggle_unflaired(self, name):
        self.subs[name]['showUnflaired'] = not self.subs[name]['showUnflaired']

        if self.subs[name]['showUnflaired']:
            log.log("Showing unflaired posts for /r/" + name + ".")
        else:
            log.log("Hiding unflaired posts for /r/" + name + ".")

    def toggle_include(self, name):
        self.subs[name]['includeExclude'] = \
            not self.subs[name]['includeExclude']

        if self.subs[name]['includeExclude']:
            log.log("Toggled include mode for flairs for /r/" + name + ".")
        else:
            log.log("Toggled exclude mode for flairs for /r/" + name + ".")

    def get_subreddits_string(self):
        subreddits_list = [*self.subs]
        subreddits_list.sort()
        subreddit_str = ""
        for name in subreddits_list:
            subreddit_str += "/r/" + name + "\n"
        log.log("Generated a list of all subreddits in subreddits.json")
        return subreddit_str

    def get_rules_string(self):
        rules_str = ""
        for line in self.get_subreddits_string().splitlines():
            name = line[3:]
            rules_str += line + "\n"
            for value in self.subs[name]['includeString']:
                rules_str += "<must include string> \"" + value + "\"\n"
            for value in self.subs[name]['excludeString']:
                rules_str += "<must exclude string> \"" + value + "\"\n"
            for value in self.subs[name]['includeFlair']:
                rules_str += "<includes flair> \"" + value + "\"\n"
            for value in self.subs[name]['excludeFlair']:
                rules_str += "<excludes flair> \"" + value + "\"\n"
            rules_str += "<unflaired posts> " + \
                ("shown" if self.subs[name]['showUnflaired'] else "hidden") + \
                "\n"
            rules_str += "<flair mode> " + \
                ("in" if self.subs[name]['includeExclude'] else "ex") + \
                "clude only\n\n"

    def reset(self):
        self.subs = {}
        self.write
