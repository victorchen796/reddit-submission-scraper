"""
submission_scraper module

This module contains the main logic to scrape new submissions from reddit
using PRAW.
"""

from datetime import datetime, timedelta
import praw

import config
from log import log
import submissions
import subreddits


class InvalidTimeException(Exception):
    """Raised when the inputted time is not a positive value"""


def scrape(time):
    if (time < 1):
        log("ERROR: submissions posted in the last " + str(time) +
            " minutes not scraped: " + str(time) + " is not a positive value")
        raise InvalidTimeException

    configs = config.get_config()
    reddit = praw.Reddit(client_id=configs['client_id'],
                         client_secret=configs['client_secret'],
                         user_agent=configs['user_agent'])

    subs = subreddits.subreddits
    submissions.clear()
    for name in subs.keys():
        submissions_added = 0
        for submission in reddit.subreddit(name).new(limit=25):
            submission_time = datetime.fromtimestamp(submission.created_utc)
            if datetime.now() - timedelta(minutes=time) > \
                    submission_time:
                continue
            if filter(subs, name, submission):
                submissions_added += 1
                submissions.add_submission(
                    name,
                    submission.title,
                    "https://www.reddit.com" + submission.permalink,
                    "/u/" + submission.author.name,
                    submission_time.strftime("%I:%M %p on %B %d, %Y"),
                    submission.link_flair_text
                )
        log("Added " + str(submissions_added) + " new submission" +
            ("" if submissions_added == 1 else "s") + " to /r/" + name + ".")

    log("New submissions posted in the last " + str(time) + " minutes were " +
        "scraped")


def filter(subs, name, submission):
    for string in subs[name]['includeString']:
        if submission.title.find(string) == -1:
            return False
    for string in subs[name]['excludeString']:
        if submission.title.find(string) != -1:
            return False
    if submission.link_flair_text is None:
        if subs[name]['showUnflaired']:
            return True
        else:
            return False
    if subs[name]['includeExclude']:
        if submission.link_flair_text not in subs[name]['includeFlair']:
            return False
    else:
        if submission.link_flair_text in subs[name]['excludeFlair']:
            return False
    return True
