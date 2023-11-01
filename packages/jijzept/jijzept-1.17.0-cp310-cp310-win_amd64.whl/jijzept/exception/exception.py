from __future__ import annotations


class JijZeptClientError(Exception):
    __name__ = "JijZeptClientError"


class ConfigError(JijZeptClientError):
    __name__ = "ConfigError"


class JijZeptClientValidationError(JijZeptClientError):
    __name__ = "JijZeptClientValidationError"


class JijZeptSolvingError(RuntimeError):
    __name__ = "JijZeptSolvingError"

    def __init__(self, *args):
        super().__init__(*args)


class JijZeptSolvingFailedError(JijZeptSolvingError):
    __name__ = "JijZeptSolvingFailedError"
    note = "Failed to solve the problem. The following error occurred in the solving process."

    def __init__(self, message, *args):
        JijZeptSolvingError.__init__(self, self.note, message, *args)


class JijZeptSolvingUnknownError(JijZeptSolvingError):
    __name__ = "JijZeptSolvingUnknownError"
    note = "Unknown error occurred in the solving process. Please contact us at jijzept@j-ij.com."

    def __init__(self, message, *args):
        JijZeptSolvingError.__init__(self, self.note, message, *args)


class JijZeptSolvingValidationError(JijZeptSolvingError):
    __name__ = "JijZeptSolvingValidationError"
    note = "Validation error occurred in the solving process. Please contact us at jijzept@j-ij.com."

    def __init__(self, message, *args):
        JijZeptSolvingError.__init__(self, self.note, message, *args)
