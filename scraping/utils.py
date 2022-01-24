import logging
import json
import os

def extract_contents(tag):
    if hasattr(tag, 'contents') and len(tag.contents) > 0:
        try:
            return tag.contents[0].strip()
        except Exception as e:
            logging.error(f"Can't extract contents of {tag}")
    else:
        return None

# note file path is relative to root of repo
def get_teams_by_conference(conference):
    with open(os.path.join('scraping', 'teams.json')) as file:
        all_teams = json.load(file)
        return all_teams[conference]

