from .filters import FIELD_TYPES


def validate_query_string(request):
    """
    Checks incoming query parameters for validity.
    Raises a RuntimeError if any parameters in the request are invalid.
    """
    if request.GET:
        for key in request.GET:
            if key not in FIELD_TYPES:
                raise RuntimeError('Invalid query parameter: {}'.format(key))
