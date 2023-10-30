"""Wrapper helpers."""

from vpnetbox.exceptions import NbParserError


def strict_value(method):
    """Wrap method to check value in strict manner, returned value is mandatory.

    :param method: The method to be decorated.
    :return: The decorated function.
    """

    def wrapper(self, *args, **kwargs):
        """Wrap."""
        strict_actual = self.strict
        self.strict = True

        result = method(self, *args, **kwargs)

        self.strict = strict_actual
        if not result:
            keys = "/".join(args)
            raise NbParserError(f"{keys=} expected in {self._source()}.")

        return result

    return wrapper
