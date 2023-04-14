import re


class Utility:

    @staticmethod
    def extract_user_id(text: str):
        match = re.search(r'\d+', text)
        if match:
            return int(match.group(0))
        return None
