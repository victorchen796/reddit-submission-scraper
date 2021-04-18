from resources import get_subreddits, update_subreddits
from subreddits import list as subreddit_list


"""
subreddits:
{
    '<subreddit name>': {
        'phrases': [
            '<phrase>',
            ...
        ],
        'flairs': [
            '<flair>',
            ...
        ],
        'include': <boolean>,
        'unflaired': <boolean>
    },
    ...
}
"""
subreddits = get_subreddits()


def list():
    return subreddits


def add_phrase(name, phrase):
    subreddits[name]['phrases'].append(phrase)
    subreddits[name]['phrases'].sort()
    update_subreddits(subreddits)


def remove_phrase(name, phrase):
    subreddits[name]['phrases'].remove(phrase)
    update_subreddits(subreddits)


def add_flair(name, flair):
    subreddits[name]['flairs'].append(flair)
    subreddits[name]['flairs'].sort()
    update_subreddits(subreddits)


def remove_flair(name, flair):
    subreddits[name]['flairs'].remove(flair)
    update_subreddits(subreddits)


def include_filtered(name):
    if not subreddits[name]['include']:
        subreddits[name]['include'] = True
        update_subreddits(subreddits)

def exclude_filtered(name):
    if subreddits[name]['include']:
        subreddits[name]['include'] = False
        update_subreddits(subreddits)


def show_unflaired(name):
    if not subreddits[name]['unflaired']:
        subreddits[name]['unflaired'] = True
        update_subreddits(subreddits)


def hide_unflaired(name):
    if subreddits[name]['unflaired']:
        subreddits[name]['unflaired'] = False
        update_subreddits(subreddits)


def clear_subreddit(name):
    subreddits[name].clear()
    update_subreddits(subreddits)


def clear_all():
    for name in subreddit_list():
        subreddits[name].clear()
    update_subreddits(subreddits)