from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class AuthorRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if request.user != self.get_object().author or not request.user.is_staff:
                messages.info(request, 'Изменение и удаление записи блога доступно только автору')
                return redirect('main')
        return super().dispatch(request, *args, **kwargs)


class UserIsNotAuthenticated(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            raise PermissionDenied
        return True

    def handle_no_permission(self):
        return redirect('main')
