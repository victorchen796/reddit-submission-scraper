#! /usr/bin/env python

import click
import colorama

import config
import filters
import submissions
import subreddits

@click.group()
def rss():
    pass


@rss.command()
@click.option('--list', '-l', is_flag=True, help="")
@click.option('--add', '-s', '-a', multiple=True, help="")
@click.option('--remove', '-S', '-r', multiple=True, help="")
@click.option('--clear', '-c', is_flag=True, help="") # will be executed first
def subreddits(list, add, remove, clear):
    """"""
    click.secho("anime", fg="red", bold=True)
    click.secho("buildapcsales", fg="red", bold=True)
    click.secho("csMajors", fg="red", bold=True)
    click.secho("ErgoMechKeyboards", fg="red", bold=True)
    click.secho("GlobalOffensive", fg="red", bold=True)
    click.secho("leagueoflegends", fg="red", bold=True)
    click.secho("malefashionadvice", fg="red", bold=True)
    click.secho("manga", fg="red", bold=True)
    click.secho("MechanicalKeyboards", fg="red", bold=True)
    click.secho("osugame", fg="red", bold=True)
    click.secho("rutgers", fg="red", bold=True)
    click.secho("THE_PACK", fg="red", bold=True)
    click.secho("wallstreetbets", fg="red", bold=True)
    if click.confirm("Are you sure you want to clear the subreddit list?"):
        # removed_subreddits = subreddits.clear -> RETURN NAMES OF ALL REMOVED SUBREDDITS
        # for subreddit in removed_subreddits:
        click.echo("ayo wtf man why would you do that")
                


@rss.command()
@click.option('--list', '-l', is_flag=True, help="")
@click.option('--add-phrase', '-a', nargs=2, type=str, multiple=True, help="")
@click.option('--remove-phrase', '-r', nargs=2, type=str, multiple=True, help="")
@click.option('--add-flair', '-A', nargs=2, type=str, multiple=True, help="")
@click.option('--remove-flair', '-R', nargs=2, type=str, multiple=True, help="")
@click.option('--include-filtered', '-i', type=str, help="")
@click.option('--exclude-filtered', '-e', type=str, help="")
@click.option('--show-unflaired', '-s', type=str, help="")
@click.option('--hide-unflaired', '-h', type=str, help="")
@click.option('--clear-subreddit', '-c', type=str, help="")
@click.option('--clear-all', '-C', is_flag=True, help="")
def filters(list, add_phrase, remove_phrase, add_flair, remove_flair,
        include_filtered, exclude_filtered, show_unflaired, hide_unflaired,
        clear_subreddit, clear_all):
    """"""
    click.secho("anime", fg="red", bold=True)
    click.echo("settings")
    click.secho("    include filtered", fg='yellow', bold=True)
    click.secho("    show unflaired", fg='yellow', bold=True)
    click.echo("phrases")
    click.secho("    cthulhu", fg="magenta", bold=True)
    click.secho("    Keycult No. 2", fg="magenta", bold=True)
    click.secho("    frankenswitch", fg='magenta', bold=True)
    click.echo("flairs")
    click.secho("    Buying", fg="cyan", bold=True)
    click.secho("    Selling", fg="cyan", bold=True)
    click.echo()
    click.secho("manga", fg="red", bold=True)
    click.echo("settings")
    click.secho("    exclude filtered", fg='yellow', bold=True)
    click.secho("    hide unflaired", fg='yellow', bold=True)
    click.echo("phrases")
    click.secho("    testing one two three", fg="magenta", bold=True)
    click.secho("    coloredautoreset", fg="magenta", bold=True)
    click.echo("flairs")
    click.secho("    Art", fg="cyan", bold=True)
    click.secho("    Meta", fg="cyan", bold=True)
    click.secho("    News", fg="cyan", bold=True)


@rss.command()
@click.option('--scrape', '-s', is_flag=True, help="")
@click.option('--view', '-v', is_flag=True, help="")
@click.option('--subreddits', '-g', is_flag=True, help="")
@click.option('--open', '-o', multiple=True, help="")
def submissions(scrape, view, subreddits, open):
    """"""
    click.echo("(", nl=False)
    click.secho("3", bold=True, fg="yellow", nl=False)
    click.echo(") [", nl=False)
    click.secho("News", bold = True, fg="cyan", nl=False)
    click.echo("] ", nl=False)
    click.secho("Funimation: The WONDER EGG PRIORITY special episode will be headed exclusively to Funimation on June 30"[:100] + "...", bold=True, fg="blue")
    click.echo("    by ", nl=False)
    click.secho("Turbostrider27", bold=True, fg="red", nl=False)
    click.echo(" on ", nl=False)
    click.secho("2021-03-31", bold=True, fg="red", nl=False)
    click.echo(" at ", nl=False)
    click.secho("09:00:15", bold=True, fg="red", nl=False)
    click.echo(" in ", nl=False)
    click.secho("anime", bold=True, fg="red")
    click.secho("    https://www.reddit.com/r/anime/comments/mhk4uz/funimation_the_wonder_egg_priority_special/", bold=True, fg="green")


@rss.command()
@click.option('--view', '-v', is_flag=True, help="")
@click.option('--edit', '-e', nargs=3, type=str, help="")
@click.option('--clear', '-c', is_flag=True, help="")
def config(view, edit, clear):
    """"""
    click.echo("client id")
    click.secho("    _ssY0hxD2lZz1Q", bold=True, fg='yellow')
    click.echo("client secret")
    click.secho("    LFq3lWZ7P_T3osOlmYVFBECs7k8", bold=True, fg='yellow')
    click.echo("user agent")
    click.secho("    reddit-submission-scraper", bold=True, fg='yellow')


@rss.command()
def reset():
    """"""
    pass


if __name__ == '__main__': 
    rss()