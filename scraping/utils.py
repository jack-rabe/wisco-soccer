import logging

def extract_contents(tag):
    if hasattr(tag, 'contents') and len(tag.contents) > 0:
        try:
            return tag.contents[0].strip()
        except Exception as e:
            logging.error(f"Can't extract contents of {tag}")
    else:
        return None

