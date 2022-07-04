class StrapiError(Exception):
    pass


class JsonParsingError(StrapiError):
    pass


class ForbiddenError(StrapiError):
    pass


class NotFoundError(StrapiError):
    pass


class ValidationError(StrapiError):
    pass


class InternalServerError(StrapiError):
    pass


class RatelimitError(StrapiError):
    pass
