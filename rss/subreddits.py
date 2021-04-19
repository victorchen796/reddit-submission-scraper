from resources import get_subreddits, update_subreddits


"""
subreddits:
{
    '<subreddit name>': {
        'phrases': [
            '<phrases>'
        ],
        'flairs': [
            '<flairs>'
        ],
        'include': <boolean>,
        'unflaired': <boolean>
    },
    ...
}
"""
subreddits = get_subreddits()


def list():
    return subreddits.keys()


def add(name):
    subreddits[name] = {
        'phrases': [],
        'flairs': [],
        'include': False,
        'unflaired': True
    }
    update_subreddits(subreddits)


def remove(name):
    del subreddits[name]
    update_subreddits(subreddits)


def clear():
    subreddits.clear()
    update_subreddits(subreddits)