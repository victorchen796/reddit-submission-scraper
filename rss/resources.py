import json
import os


script_path = os.path.abspath(__file__)
script_dir = os.path.split(script_path)[0]


def get_config():
    rel_path = 'resources/config.json'
    path = os.path.join(script_dir, rel_path)
    with open(path, 'r') as f:
        config = json.loads(f.read())
    return config


def get_submissions():
    rel_path = 'resources/submissions.json'
    path = os.path.join(script_dir, rel_path)
    with open(path, 'r') as f:
        submissions = json.loads(f.read())
    return submissions


def get_subreddits():
    rel_path = 'resources/subreddits.json'
    path = os.path.join(script_dir, rel_path)
    with open(path, 'r') as f:
        subreddits = json.loads(f.read())
    return subreddits


def update_config(config):
    rel_path = 'resources/config.json'
    path = os.path.join(script_dir, rel_path)
    with open(path, 'w') as f:
        f.write(json.dumps(config, indent=2))


def update_submissions(submissions):
    rel_path = 'resources/submissions.json'
    path = os.path.join(script_dir, rel_path)
    with open(path, 'w') as f:
        f.write(json.dumps(submissions, indent=2, default=str))


def update_subreddits(subreddits):
    rel_path = 'resources/subreddits.json'
    path = os.path.join(script_dir, rel_path)
    with open(path, 'w') as f:
        f.write(json.dumps(subreddits, indent=2))