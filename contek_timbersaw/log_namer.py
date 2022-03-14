class LogNamer:

    def __init__(self, original_name: str, extension: str = 'log') -> None:
        self._original_name = original_name
        self._extension = extension

    def __call__(self, name) -> str:
        return name.replace(self._original_name, '') + '.' + self._extension
