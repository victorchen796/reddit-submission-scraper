#! /usr/bin/env python

from datetime import datetime, timedelta

import click
import colorama

import config as cfg
import filters as fltr
import praw_scraper
import submissions as subm
import subreddits as subr
import validator

@click.group()
def rss():
    pass


@rss.command()
@click.option('--list', '-l', is_flag=True, help="")
@click.option('--add', '-a', multiple=True, help="")
@click.option('--remove', '-r', multiple=True, help="")
@click.option('--clear', '-c', is_flag=True, help="") # will be executed first
def subreddits(
        list, 
        add, 
        remove, 
        clear
):
    """"""
    first = True

    if clear:
        if click.confirm("Are you sure you want to remove all subreddits?"):
            subr.clear()
            click.echo("Cleared subreddits.")
        else:
            click.echo("Subreddits were not cleared.")
        first = False
    
    if add or remove:
        if first:
            first = False
        else:
            click.echo()

        if add:
            for name in add:
                # TODO: validate (and correct?) subreddit name
                # TODO: prevent duplicates
                subr.add(name)
                secho_red(name, False)
                click.echo(" has been added.")
        
        if remove:
            for name in remove:
                # TODO: check if subreddit is valid
                subr.remove(name)
                secho_red(name, False)
                click.echo(" has been removed.")
    
    if list:
        if first:
            first = False
        else:
            click.echo()
        for name in subr.list():
            secho_red(name, True)
                

@rss.command()
@click.option('--list', '-l', is_flag=True, help="")
@click.option('--add-phrase', '-p', nargs=2, type=str, multiple=True, help="")
@click.option('--remove-phrase', '-P', nargs=2, type=str, multiple=True, help="")
@click.option('--add-flair', '-f', nargs=2, type=str, multiple=True, help="")
@click.option('--remove-flair', '-F', nargs=2, type=str, multiple=True, help="")
@click.option('--include-filtered', '-i', type=str, help="")
@click.option('--exclude-filtered', '-e', type=str, help="")
@click.option('--show-unflaired', '-s', type=str, help="")
@click.option('--hide-unflaired', '-h', type=str, help="")
@click.option('--clear-subreddit', '-c', type=str, multiple=True, help="")
@click.option('--clear-all', '-C', is_flag=True, help="")
def filters(
        list, 
        add_phrase, 
        remove_phrase, 
        add_flair, 
        remove_flair,
        include_filtered, 
        exclude_filtered, 
        show_unflaired, 
        hide_unflaired,
        clear_subreddit, 
        clear_all
):
    """"""
    first = True

    if clear_subreddit and not clear_all:
        for name in clear_subreddit:
            # TODO: check if subreddit is valid
            click.echo("Are you sure you want to clear all filters " \
                    "for ", nl=False)
            secho_red(name, False)
            if click.confirm("?"):
                fltr.clear_subreddit(name)
                click.echo("Cleared all filters for ", nl=False)
                secho_red(name, False)
                click.echo(".")
            else:
                click.echo("Filters for ", nl=False)
                secho_red(name, False)
                click.echo(" were not cleared.")
        first = False
    
    if clear_all:
        if click.confirm("Are you sure you want to clear all filters for " \
                "all subreddits?"):
            fltr.clear_all()
            click.echo("Cleared all filters.")
        else:
            click.echo("All filters were not cleared.")
        first = False
    
    if add_phrase or remove_phrase or add_flair or remove_flair \
            or include_filtered or exclude_filtered or show_unflaired \
            or hide_unflaired:
        if first:
            first = False
        else:
            click.echo()

        if add_phrase:
            for name_phrase in add_phrase:
                # TODO: check if subreddit is valid
                # TODO: prevent duplicates
                fltr.add_phrase(name_phrase[0], name_phrase[1])
                click.echo("Phrase \"", nl=False)
                secho_magenta(name_phrase[1], False)
                click.echo("\" was added for ", nl=False)
                secho_red(name_phrase[0], False)
                click.echo(".")

        if remove_phrase:
            for name_phrase in remove_phrase:
                # TODO: check if subreddit is valid
                # TODO: check if phrase is valid
                fltr.remove_phrase(name_phrase[0], name_phrase[1])
                click.echo("Phrase \"", nl=False)
                secho_magenta(name_phrase[1], False)
                click.echo("\" was removed for ", nl=False)
                secho_red(name_phrase[0], False)
                click.echo(".")
        
        if add_flair:
            for name_flair in add_flair:
                # TODO: check if subreddit is valid
                # TODO: prevent duplicates
                fltr.add_flair(name_flair[0], name_flair[1])
                click.echo("Flair \"", nl=False)
                secho_cyan(name_flair[1], False)
                click.echo("\" was added for ", nl=False)
                secho_red(name_flair[0], False)
                click.echo(".")
        
        if remove_flair:
            for name_flair in remove_flair:
                # TODO: check if subreddit is valid
                # TODO: check if flair is valid
                fltr.remove_flair(name_flair[0], name_flair[1])
                click.echo("Flair \"", nl=False)
                secho_cyan(name_flair[1], False)
                click.echo("\" was removed for ", nl=False)
                secho_red(name_flair[0], False)
                click.echo(".")
        
        if include_filtered:
            # TODO: check if subreddit is valid
            fltr.include_filtered(include_filtered)
            secho_red(include_filtered, False)
            click.echo(" set to only ", nl=False)
            secho_yellow("include filtered", False)
            click.echo(" submissions.")
        
        if exclude_filtered:
            # TODO: check if subreddit is valid
            fltr.exclude_filtered(exclude_filtered)
            secho_red(exclude_filtered, False)
            click.echo(" set to only ", nl=False)
            secho_yellow("exclude filtered", False)
            click.echo(" submissions.")

        if show_unflaired:
            # TODO: cleck if subreddit is valid
            fltr.show_unflaired(show_unflaired)
            secho_red(show_unflaired, False)
            click.echo(" set to ", nl=False)
            secho_yellow("show unflaired", False)
            click.echo(" submissions.")
        
        if hide_unflaired:
            if first:
                first = False
            else:
                click.echo()
            # TODO: check if subreddit is valid
            fltr.hide_unflaired(hide_unflaired)
            secho_red(hide_unflaired, False)
            click.echo(" set to ", nl=False)
            secho_yellow("hide unflaired", False)
            click.echo(" submissions.")
    
    if list:
        if first:
            first = False
        else:
            click.echo()
        
        first_list = True
        for name in subr.list():
            if first_list:
                first_list = False
            else:
                click.echo()
            
            subreddit = fltr.list()[name]
            secho_red(name, True)
            click.echo("Settings")
            if subreddit['include']:
                secho_yellow("  include filtered", True)
            else:
                secho_yellow("  exclude filtered", True)
            if subreddit['unflaired']:
                secho_yellow("  show unflaired", True)
            else:
                secho_yellow("  hide unflaired", True)
            if subreddit['phrases']:
                click.echo("Phrases")
                for phrase in subreddit['phrases']:
                    secho_magenta("  " + phrase, True)
            if subreddit['flairs']:
                click.echo("Flairs")
                for flair in subreddit['flairs']:
                    secho_cyan("  " + flair, True)


@rss.command()
@click.option('--scrape', '-s', type=int, help="")
@click.option('--list', '-l', is_flag=True, help="")
@click.option('--subreddits', '-g', is_flag=True, help="")
@click.option('--open', '-o', type=int, multiple=True, help="")
@click.option('--clear', '-c', is_flag=True, help="")
def submissions(
        scrape,
        list, 
        subreddits, 
        open,
        clear
):
    """"""
    first = True

    if open:
        for index in open:
            subm.open(index)
            click.echo("Opened link for submission (", nl=False)
            secho_yellow(str(index), False)
            click.echo(").")
        first = False

    if clear:
        if first:
            first = False
        else:
            click.echo()
        if click.confirm("Are you sure you want to clear your scraped submissions?"):
            subm.clear()
            click.echo("Cleared submissions.")
        else:
            click.echo("Submissions were not cleared.")
    
    if scrape:
        if first:
            first = False
        else:
            click.echo()
        # TODO: check if inputted amount of time is valid
        click.echo("Scraping submissions from Reddit...")
        praw_scraper.scrape(scrape)
        click.echo("Finished scraping submissions.")
    
    if list:
        submission_list = subm.list()['submissions']
        if not subreddits:
            if first:
                first = False
            else:
                click.echo()
            if len(submission_list) == 0:
                click.echo("No submissions were found.")
            else:
                for index in range(0, len(submission_list) - 1):
                    submission = submission_list[index]
                    click.echo("(", nl=False)
                    secho_yellow(str(index), False)
                    click.echo(") ", nl=False)
                    if submission['flair'] is not None:
                        click.echo("[", nl=False)
                        secho_cyan(submission['flair'], False)
                        click.echo("] ", nl=False)
                    secho_blue(submission['title'], True)
                    for i in range(0, len(str(index)) + 3):
                        click.echo(" ", nl=False)
                    click.echo("by ", nl=False)
                    secho_red(submission['author'], False)
                    click.echo(" on ", nl=False)
                    date = str(submission['datetime']).split()[0]
                    time = str(submission['datetime']).split()[1]
                    secho_red(date, False)
                    click.echo(" at ", nl=False)
                    secho_red(time, False)
                    click.echo(" in ", nl=False)
                    secho_red(submission['subreddit'], True)
                    for i in range(0, len(str(index)) + 3):
                        click.echo(" ", nl=False)
                    secho_green(submission['link'], True)
        else:
            subreddit_list = subm.list()['subreddits']
            for name in subreddit_list.keys():
                if first:
                    first = False
                else:
                    click.echo()
                secho_red(name, True)
                for index in subreddit_list[name]:
                    submission = submission_list[index]
                    click.echo("(", nl=False)
                    secho_yellow(str(index), False)
                    click.echo(") ", nl=False)
                    if submission['flair'] is not None:
                        click.echo("[", nl=False)
                        secho_cyan(submission['flair'], False)
                        click.echo("] ", nl=False)
                    secho_blue(submission['title'], True)
                    for i in range(0, len(str(index)) + 3):
                        click.echo(" ", nl=False)
                    click.echo("by ", nl=False)
                    secho_red(submission['author'], False)
                    click.echo(" on ", nl=False)
                    date = str(submission['datetime']).split()[0]
                    time = str(submission['datetime']).split()[1]
                    secho_red(date, False)
                    click.echo(" at ", nl=False)
                    secho_red(time, True)
                    for i in range(0, len(str(index)) + 3):
                        click.echo(" ", nl=False)
                    secho_green(submission['link'], True)


@rss.command()
@click.option('--view', '-v', is_flag=True, help="")
@click.option('--edit', '-e', nargs=3, type=str, help="")
@click.option('--clear', '-c', is_flag=True, help="")
def config(
        view, 
        edit, 
        clear
):
    """"""
    first = True

    if clear:
        if click.confirm("Are you sure you want to clear your PRAW configuration values?"):
            cfg.clear()
            click.echo("Cleared PRAW configuration values.")
        else:
            click.echo("PRAW configuration values were not cleared.")
        first = False
    
    if edit:
        if first:
            first = False
        else:
            click.echo()
        # TODO: check if config values are valid
        cfg.edit(edit[0], edit[1], edit[2])
        click.echo("PRAW configuration values were set.")
    
    if view:
        if first:
            first = False
        else:
            click.echo()
        values = cfg.list()
        click.echo("Client ID")
        secho_yellow("  " + values['client_id'], True)
        click.echo("Client Secret")
        secho_yellow("  " + values['client_secret'], True)
        click.echo("User Agent")
        secho_yellow("  " + values['user_agent'], True)


@rss.command()
def reset():
    """"""
    pass


def secho_blue(text, nl):
    click.secho(text, fg='blue', bold=True, nl=nl)


def secho_cyan(text, nl):
    click.secho(text, fg='cyan', bold=True, nl=nl)
    

def secho_green(text, nl):
    click.secho(text, fg='green', bold=True, nl=nl)


def secho_magenta(text, nl):
    click.secho(text, fg='magenta', bold=True, nl=nl)


def secho_red(text, nl):
    click.secho(text, fg='red', bold=True, nl=nl)


def secho_yellow(text, nl):
    click.secho(text, fg='yellow', bold=True, nl=nl)


if __name__ == '__main__': 
    rss()