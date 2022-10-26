from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """The custom exception handler."""

    def get_exception_text():
        """Returns the exception details."""
        try:
            return exc.args[0]
        except IndexError:
            return 'Server error'

    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        status_code = 400
        data = {
            'status_code': status_code,
            'details': get_exception_text(),
        }
        response = Response(data, status=status_code)
    return response
