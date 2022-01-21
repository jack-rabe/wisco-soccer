import logging
import json

def extract_contents(tag):
    if hasattr(tag, 'contents') and len(tag.contents) > 0:
        try:
            return tag.contents[0].strip()
        except Exception as e:
            logging.error(f"Can't extract contents of {tag}")
    else:
        return None

def get_teams_by_conference(conference):
    with open('teams.json') as file:
        all_teams = json.load(file)
        return all_teams[conference]

