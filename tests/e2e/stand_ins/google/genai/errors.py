"""Stand-in for google.genai.errors (tests only)."""


class APIError(Exception):
    def __init__(self, code, message=""):
        super().__init__(message or f"status {code}")
        self.code = code
