from datetime import datetime, timedelta

import praw

import config
import filters
import submissions
import subreddits


config = config.list()
filters = filters.list()
subreddits = subreddits.list()


def scrape(time):
    reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent']
    )
    
    submissions.clear()

    min_time = datetime.now() - timedelta(minutes=time)
    for name in subreddits:
        for submission in reddit.subreddit(name).new(limit=None):
            submission_time = datetime.fromtimestamp(submission.created_utc)
            if min_time > submission_time:
                break
            if not filter(name, submission):
                continue
            submissions.add(
                    submission.title,
                    submission.author.name,
                    submission_time,
                    name,
                    submission.link_flair_text,
                    submission.url
                    )
                    
    submissions.write()
                        

def filter(name, submission):
    title = submission.title.lower()
    if submission.link_flair_text is not None:
        flair = submission.link_flair_text.lower()
    else:
        flair = None

    if filters[name]['include']:
        for phrase in filters[name]['phrases']:
            if title.find(phrase) == -1:
                return False
        if flair is None:
            if filters[name]['unflaired']:
                return True
            else:
                return False
        if flair not in filters[name]['flairs']:
            return False
        return True
    else:
        for phrase in filters[name]['phrases']:
            if title.find(phrase) != -1:
                return False
        if flair is None:
            if filters[name]['unflaired']:
                return True
            else:
                return False
        if flair in filters[name]['flairs']:
            return False
        return True