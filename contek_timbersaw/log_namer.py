class LogNamer:

    def __init__(self, original_name: str, extension: str = 'log') -> None:
        self._original_name = original_name
        self._extension = extension

    def __call__(self, name) -> str:
        prefix = self._original_name + '.'
        return name.replace(prefix, '') + '.' + self._extension
