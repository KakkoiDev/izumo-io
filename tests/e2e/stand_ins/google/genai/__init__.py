"""Stand-in for the google-genai client, so scripts/translate_content.py runs offline in the e2e tests.

It "translates" by tagging the text with the target language: a Markdown lesson comes back with
`[<language>] ` before its title and its first heading, a short field comes back as `[<language>] <text>`.
Every call is appended to the file named by STAND_IN_LOG (one line: the first line of the prompt).
The key "rejected-key" makes every call fail with a 401, like an invalid or expired key.
"""

import os
import re
from types import SimpleNamespace

from .errors import APIError

_TARGET = re.compile(r"from English to (?P<lang>.+?)\.\n")


class _Models:
    def __init__(self, api_key):
        self._api_key = api_key

    def generate_content(self, model, contents):
        log = os.environ.get("STAND_IN_LOG")
        if log:
            with open(log, "a", encoding="utf-8") as stream:
                stream.write(contents.splitlines()[0] + "\n")
        if self._api_key == "rejected-key":
            raise APIError(401, "API key not valid. Please pass a valid API key.")
        if contents == "ping":
            return SimpleNamespace(text="pong")
        lang = _TARGET.search(contents)["lang"]
        source = contents.split("Source:\n", 1)[1]
        if contents.startswith("Translate the following markdown"):
            text = re.sub(r'^title: "?(.*?)"?$', rf'title: "[{lang}] \1"', source, count=1, flags=re.M)
            text = re.sub(r"^# (.*)$", rf"# [{lang}] \1", text, count=1, flags=re.M)
            return SimpleNamespace(text=text)
        return SimpleNamespace(text=f"[{lang}] {source.strip()}")


class Client:
    def __init__(self, api_key):
        self.models = _Models(api_key)
