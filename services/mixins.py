from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class AuthorRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if not request.user.is_superuser and not request.user.is_staff and request.user != self.get_object().author:
                messages.error(request, 'Изменение и удаление записи доступно только автору или администратору')
                return redirect('main')
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if not request.user.is_superuser and not request.user.is_staff:
                messages.error(request, 'Добавление записи доступно только администратору')
                return redirect('main')
        return super().dispatch(request, *args, **kwargs)


class UserIsNotAuthenticated(UserPassesTestMixin):
    def test_func(self):
        print(self.request.user.is_authenticated)
        if self.request.user.is_authenticated:
            messages.info(self.request, 'Вы уже авторизованы. Вы не можете посетить эту страницу.')
            return False
        return True

    def handle_no_permission(self):
        return redirect('main')
