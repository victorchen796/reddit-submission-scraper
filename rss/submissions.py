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
            'date': <date>,
            'time': <time>,
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


def submissions():
    return submissions


def add_submission(title, author, date, timestamp, subreddit, flair, link):
    submissions['submissions'].append({
        'title': title,
        'author': author,
        'date': date
        'datetime': datetime.fromtimestamp(timestamp),
        'subreddit': subreddit,
        'flair': flair,
        'link': link
    })


def write():
    submissions['submissions'].sort(key=get_datetime, reverse=True)
    for i in range(0, submissions['submissions'].len() - 1):
        name = submissions['submissions'][i]['subreddit']
        if not submissions['subreddits'].has_key(name):
            submissions['subreddits'][name] = []
        submissions['subreddits'][name].append(i)
    update_submissions(submissions)


def get_datetime(submission):
    return submission['datetime']


def open(index):
    webbrowser.open(submissions['submissions'][i]['link'])