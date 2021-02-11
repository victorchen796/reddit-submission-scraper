import sys

if __name__ == "__main__":
    major = sys.version_info[0]
    minor = sys.version_info[1]

    python_version = str(sys.version_info[0]) + "." + \
        str(sys.version_info[1]) + "." + str(sys.version_info[2])

    if major != 3 or minor < 6:
        print("reddit-submission-scraper requires Python 3.6+.\nYou are " +
              "using Python %s, which is not supported by " +
              "reddit-submission-scraper." % (python_version))
        sys.exit(1)

    import reddit_submission_scraper
    reddit_submission_scraper.main()
