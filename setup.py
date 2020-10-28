from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="reddit-submission-scraper",
    version="1.0",
    description="Gets the most recent reddit posts from specified subreddits",
    author="Victor Chen",
    author_email="victor.w.chen@rutgers.edu",
    url="https://github.com/victorchen796/reddit-submission-scraper",
    license="MIT",
    install_requires=requirements,
    packages=["rs_scraper"]
)
