class InvalidTaskFormat(Exception):
    """Raised when some of the tasks do not have the expected format."""

    def __init__(self, msg: str = None):
        self.msg = msg
