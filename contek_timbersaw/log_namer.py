class LogNamer:

    def __init__(self, extension: str = 'log') -> None:
        self._extension = extension

    def __call__(self, name) -> str:
        return name + '.' + self._extension
