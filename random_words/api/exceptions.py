from rest_framework.response import Response
from rest_framework.views import exception_handler


class ExceptionMixin:
    error_status_code = 400

    def get_exception_handler_context(self):
        """
        Добавляет ключ статус кода ответа, при возникновении
        исключения во `View`.
        """
        context: dict = super().get_exception_handler_context()
        context['error_status_code'] = self.error_status_code
        return context


def custom_exception_handler(exc, context):
    """
    Функция для отлавливания ошибок, которые вызываются
    во `View`.
    """

    def get_exception_text():
        """Возвращает текст исключения."""
        try:
            return exc.args[0]
        except IndexError:
            return 'Server error'

    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        status_code = context.get('error_status_code', 400)
        data = {
            'status_code': status_code,
            'detail': get_exception_text(),
        }
        response = Response(data, status=status_code)
    return response
