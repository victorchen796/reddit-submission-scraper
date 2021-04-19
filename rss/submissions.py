from datetime import datetime
import webbrowser

from resources import get_submissions, update_submissions


"""
submissions:
{
    'submissions': [
        {
            'title': '<title>',
            'author': '<author>',
            'datetime': <datetime>,
            'subreddit': '<subreddit>'
            'flair': '<flair>'
            'link': '<link>'
        },
        ...
    ]
    'subreddits': {
        'name': [
            <index>,
            ...
        ],
        ...
    }
}
"""
submissions = get_submissions()


def list():
    return submissions


def clear():
    submissions['submissions'] = []
    submissions['subreddits'] = {}
    update_submissions(submissions)


def add(title, author, datetime, subreddit, flair, link):
    submissions['submissions'].append({
        'title': title,
        'author': author,
        'datetime': datetime,
        'subreddit': subreddit,
        'flair': flair,
        'link': link
    })


def write():
    submissions['submissions'].sort(key=get_datetime, reverse=True)
    for i in range(0, len(submissions['submissions']) - 1):
        name = submissions['submissions'][i]['subreddit']
        if not name in submissions['subreddits'].keys():
            submissions['subreddits'][name] = []
        submissions['subreddits'][name].append(i)
    update_submissions(submissions)


def get_datetime(submission):
    return submission['datetime']


def open(index):
    webbrowser.open_new_tab(submissions['submissions'][index]['link'])