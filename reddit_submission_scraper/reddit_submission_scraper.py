"""Documentation not yet added..."""

from PyInquirer import prompt

import config
import log
import scraper
import submissions
import subreddits

# TODO: check to make sure config is correct when program runs or when
#       config is updated
# TODO: add validator for client_id, client_secret, and user_agent (also
#       to prevent empty inputs)
# # temporarily keep next line
# config.reset()
praw_config = [
    {
        'type': 'input',
        'name': 'client_id',
        'message': "Client ID:",
        'filter': lambda val: None if not val else val
    },
    {
        'type': 'input',
        'name': 'client_secret',
        'message': 'Client Secret:',
        'filter': lambda val: None if not val else val
    },
    {
        'type': 'input',
        'name': 'user_agent',
        'message': "User Agent:",
        'filter': lambda val: None if not val else val
    }
]

answers = {}
choose_option = [
    {
        'type': 'list',
        'name': 'option',
        'message': "What would you like to do?",
        'choices': [
            "View all subreddits",
            "View all subreddits and filters",
            "View PRAW configuration values",
            "Change PRAW configuration values",
            "Add or remove a subreddit",
            "Add or remove a phrase filter",
            "Add or remove a flair filter",
            "Change flair filter settings",
            "Get new submissions",
            "Open a submission link",
            "Clear the log",
            "Reset a subreddit",
            "Reset all settings",
            "Exit"
            # Show hints
        ]
    },
    {
        'type': 'list',
        'name': 'add_rm_subreddit',
        'message': "Would you like to add or remove a subreddit?",
        'choices': [
            "Add a subreddit",
            "Remove a subreddit"
        ],
        'when': lambda answers: answers['option'] == "Add or remove a " +
                                                     "subreddit"
    },
    {
        # TODO: add validator to check if the subreddit exists
        'type': 'input',
        'name': 'subreddit',
        'message': "What is the name of the subreddit?",
        'when': lambda answers:
            answers['option'] == "Add or remove a subreddit"
    },
    {
        # TODO: add validator to check if the subreddit is valid
        'type': 'input',
        'name': 'subreddit',
        'message': "What subreddit would you like to add or remove a " +
            "phrase filter for?",
        'when': lambda answers:
            answers['option'] == "Add or remove a phrase filter"
    },
    {
        'type': 'list',
        'name': 'add_rm_phrase',
        'message': "Would you like to add or remove a phrase filter?",
        'choices': [
            "Add a phrase filter",
            "Remove a phrase filter"
        ],
        'when': lambda answers:
            answers['option'] == "Add or remove a phrase filter"
    },
    {
        'type': 'list',
        'name': 'includeExclude',
        'message': "What does this phrase filter do?",
        'choices': [
            "Submissions must include this phrase",
            "Submissions must exclude this phrase"
        ],
        'when': lambda answers:
            answers['option'] == "Add or remove a phrase filter"
    },
    {
        # TODO: add validator to check if the phrase isn't blank
        'type': 'input',
        'name': 'phrase',
        'message': "What is the phrase?",
        'when': lambda answers:
            answers['option'] == "Add or remove a phrase filter"
    },
    {
        # TODO: add validator to check if the subreddit is valid
        'type': 'input',
        'name': 'subreddit',
        'message': "What subreddit would you like to add or remove a " +
            "flair filter for?",
        'when': lambda answers:
            answers['option'] == "Add or remove a flair filter"
    },
    {
        'type': 'list',
        'name': 'add_rm_flair',
        'message': "Would you like to add or remove a flair filter?",
        'choices': [
            "Add a flair filter",
            "Remove a flair filter"
        ],
        'when': lambda answers:
            answers['option'] == "Add or remove a flair filter"
    },
    {
        'type': 'list',
        'name': 'includeExclude',
        'message': "What does this flair filter do?",
        'choices': [
            "Submissions must include this flair",
            "Submissions must exclude this flair"
        ],
        'when': lambda answers:
            answers['option'] == "Add or remove a flair filter"
    },
    {
        # TODO: add validator to check if the flair isn't blank
        'type': 'input',
        'name': 'flair',
        'message': "What is the flair?",
        'when': lambda answers:
            answers['option'] == "Add or remove a flair filter"
    },
    {
        # TODO: add validator to check if the subreddit exists
        'type': 'input',
        'name': 'subreddit',
        'message': "What subreddit would you like to change flair filter " +
            "settings for?",
        'when': lambda answers:
            answers['option'] == "Change flair filter settings"
    },
    {
        'type': 'checkbox',
        'name': 'flair_settings',
        'message': "What are your desired flair filter settings?\n" +
            "(default: Show unflaired posts=on, " +
            "Toggle include/exclude filter=off)",
        'choices': [
            {
                'name': "Show unflaired posts",
                'checked': True
            },
            {
                'name': "Toggle include/exclude (on/off) filter"
            }
        ],
        'when': lambda answers:
            answers['option'] == "Change flair filter settings"
    },
    {
        # TODO: add validator to check if the time number is valid
        'type': 'input',
        'name': 'time',
        'message': "Show posts from how many minutes ago to now? " +
            "(A limit of 25 submissions will be shown)",
        'filter': lambda val: int(val),
        'when': lambda answers:
            answers['option'] == "Get new submissions"
    },
    {
        # TODO: add validator to check if the subreddit is valid
        'type': 'input',
        'name': 'subreddit',
        'message': "What is the subreddit of the submission?",
        'when': lambda answers:
            answers['option'] == "Open a submission link"
    },
    {
        # TODO: add validator to check if the submission number is valid
        'type': 'input',
        'name': 'submission_number',
        'message': "What is the submission number?",
        'filter': lambda val: int(val),
        'when': lambda answers:
            answers['option'] == "Open a submission link"
    },
    {
        'type': 'confirm',
        'name': 'clear_logs',
        'message': "Are you sure you want to clear the log?",
        'when': lambda answers:
            answers['option'] == "Clear the log"
    },
    {
        # TODO: add validator to check if the subreddit is valid
        'type': 'input',
        'name': 'subreddit',
        'message': "Which subreddit do you want to reset?",
        'when': lambda answers:
            answers['option'] == "Reset a subreddit"
    },
    {
        'type': 'confirm',
        'name': 'reset_subreddit',
        'message': "Are you sure you want to reset this subreddit?",
        'when': lambda answers:
            answers['option'] == "Reset a subreddit"
    },
    {
        'type': 'confirm',
        'name': 'reset_settings',
        'message': "Are you sure you want to reset all settings?",
        'when': lambda answers:
            answers['option'] == "Reset all settings"
    }
]


def main():
    while True:
        print("""==================================================
 _ __ ___ ___
| '__/ __/ __|
| |  \\__ \\__ \\
|_|  |___/___/
""")

        if not config.check_config():
            print("PRAW client ID, client secret, and user agent not found.")
            print("Please input your PRAW configuration values.")
            configs = prompt(praw_config)
            config.set_config(configs['client_id'], configs['client_secret'],
                              configs['user_agent'])
            print("")

        answers = prompt(choose_option)
        option = answers['option']

        if (option == "Exit"):
            break
        elif (option == "View all subreddits"):
            if len(list(subreddits.subreddits)) == 0:
                print("You have no subreddits added.\n")
                continue
            for name in list(subreddits.subreddits):
                print("/r/" + name)
        elif (option == "View all subreddits and filters"):
            if len(list(subreddits.subreddits)) == 0:
                print("You have no subreddits added.\n")
                continue
            for name in list(subreddits.subreddits):
                print("/r/" + name)
                print("==================================================")
            if len(subreddits.subreddits[name]['includePhrase']) > 0:
                print("Posts must include these phrase(s):")
                for phrase in subreddits.subreddits[name]['includePhrase']:
                    print(" \"" + phrase + "\"")
            if len(subreddits.subreddits[name]['excludePhrase']) > 0:
                print("Posts must exclude these phrase(s):")
                for phrase in subreddits.subreddits[name]['excludePhrase']:
                    print(" \"" + phrase + "\"")
            if len(subreddits.subreddits[name]['includeFlair']) > 0:
                print("Posts must include these flair(s):")
                for flair in subreddits.subreddits[name]['includeFlair']:
                    print(" \"" + flair + "\"")
            if len(subreddits.subreddits[name]['excludeFlair']) > 0:
                print("Posts must exclude these flairs(s):")
                for flair in subreddits.subreddits[name]['excludeFlair']:
                    print(" \"" + flair + "\"")
            print("Showing unflaired posts: " +
                  ("on" if subreddits.subreddits[name]['showUnflaired']
                   else "off"))
            print("Including/excluding flairs: only " +
                  ("in" if subreddits.subreddits[name]['includeExclude']
                   else "ex") + "cluding flairs")
        elif (option == "View PRAW configuration values"):
            configs = config.get_config()
            print("Client ID: " + configs['client_id'])
            print("Client Secret: " + configs['client_secret'])
            print("User Agent: " + configs['user_agent'])
        elif (option == "Change PRAW configuration values"):
            print("Please input your PRAW configuration values.")
            configs = prompt(praw_config)
            config.set_config(configs['client_id'], configs['client_secret'],
                              configs['user_agent'])
        elif (option == "Add or remove a subreddit"):
            if (answers['add_rm_subreddit'] == "Add a subreddit"):
                subreddits.add_subreddit(answers['subreddit'])
            else:
                subreddits.remove_subreddit(answers['subreddit'])
        elif (option == "Add or remove a phrase filter"):
            if (answers['add_rm_phrase'] == "Add a phrase filter"):
                if (answers['includeExclude'] ==
                        "Submissions must include this phrase"):
                    subreddits.add_rule(answers['subreddit'], 'includePhrase',
                                        answers['phrase'])
                else:
                    subreddits.add_rule(answers['subreddit'], 'excludePhrase',
                                        answers['phrase'])
            else:
                if (answers['includeExclude'] ==
                        "Submissions must include this phrase"):
                    subreddits.remove_rule(answers['subreddit'],
                                           'includePhrase', answers['phrase'])
                else:
                    subreddits.remove_rule(answers['subreddit'],
                                           'excludePhrase', answers['phrase'])
        elif (option == "Add or remove a flair filter"):
            if (answers['add_rm_flair'] == "Add a flair filter"):
                if (answers['includeExclude'] ==
                        "Submissions must include this flair"):
                    subreddits.add_rule(answers['subreddit'], 'includeFlair',
                                        answers['flair'])
                else:
                    subreddits.add_rule(answers['subreddit'], 'excludeFlair',
                                        answers['flair'])
            else:
                if (answers['includeExclude'] ==
                        "Submissions must include this flair"):
                    subreddits.remove_rule(answers['subreddit'],
                                           'includeFlair', answers['flair'])
                else:
                    subreddits.remove_rule(answers['subreddit'],
                                           'excludeFlair', answers['flair'])
        elif (option == "Change flair filter settings"):
            if "Show unflaired posts" in answers['flair_settings']:
                subreddits.toggle_unflaired(answers['subreddit'], True)
            else:
                subreddits.toggle_unflaired(answers['subreddit'], False)
            if "Toggle include/exclude (on/off) filter" in \
                    answers['flair_settings']:
                subreddits.toggle_include(answers['subreddit'], True)
            else:
                subreddits.toggle_include(answers['subreddit'], False)
        elif (option == "Get new submissions"):
            scraper.scrape(answers['time'])
            if len(list(subreddits.subreddits)) == 0:
                print("You have no subreddits added.\n")
                continue
            for name in list(subreddits.subreddits):
                if name in submissions.submissions:
                    print("/r/" + name)
                    print("=============================================" +
                          "=====")
                    for i in range(0, len(submissions.submissions[name])):
                        post = submissions.submissions[name][i]
                        print("[" + str(i + 1) + "] " + post['title'])
                        if post['flair'] is not None:
                            print("\tFlair: " + post['flair'])
                        print("\tSubmitted by " + post['author'] +
                              " at " + post['time'])
        elif (option == "Open a submission link"):
            submissions.open_submission(answers['subreddit'],
                                        answers['submission_number'])
        elif (option == "Clear the log"):
            if answers['clear_logs']:
                log.clear()
        elif (option == "Reset a subreddit"):
            if answers['reset_subreddit']:
                subreddits.reset_subreddit(answers['subreddit'])
        elif (option == "Reset all settings"):
            if answers['reset_settings']:
                config.reset()
                log.clear()
                submissions.clear()
                subreddits.reset()
