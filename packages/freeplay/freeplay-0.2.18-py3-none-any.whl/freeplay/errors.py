class FreeplayError(Exception):
    pass


class APITypeMissingError(Exception):
    pass


class APIVersionMissingError(Exception):
    pass


class APIEngineMissingError(Exception):
    pass


class APIKeyMissingError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class TemplateNotFoundError(Exception):
    pass
