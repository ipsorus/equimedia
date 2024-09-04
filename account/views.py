from bootstrap_modal_forms.generic import BSModalLoginView
from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, TemplateView
from django.db import transaction
from django.urls import reverse_lazy

from articles.models import Article
from blog.models import BlogPost
from equi_media_portal import settings
from news.models import NewsPost
from services.mixins import UserIsNotAuthenticated
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm, UserPasswordChangeForm, \
    CustomAuthenticationForm, UserForgotPasswordForm, UserSetNewPasswordForm


User = get_user_model()


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'account/profile_detail.html'
    queryset = model.objects.all().select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context


class ProfileDetailBlogsView(DetailView):
    """
    Представление для просмотра записей блога, созданных пользователем
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'account/profile_blog_list.html'
    queryset = model.objects.all().select_related('user')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_posts = BlogPost.objects.filter(author=self.object.user, is_published=True)
        context['blogs'] = blog_posts
        context['title'] = f'Записи блогов, созданные пользователем: {self.object.user.username}'
        return context


class ProfileDetailNewsView(DetailView):
    """
    Представление для просмотра записей новостей, созданных пользователем
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'account/profile_news_list.html'
    queryset = model.objects.all().select_related('user')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_posts = NewsPost.objects.filter(author=self.object.user, is_published=True)
        context['news'] = news_posts
        context['title'] = f'Записи новостей, созданные пользователем: {self.object.user.username}'
        return context


class ProfileDetailArticlesView(DetailView):
    """
    Представление для просмотра записей статей, созданных пользователем
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'account/profile_articles_list.html'
    queryset = model.objects.all().select_related('user')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles_posts = Article.objects.filter(author=self.object.user, is_published=True)
        context['articles'] = articles_posts
        context['title'] = f'Записи статей, созданные пользователем: {self.object.user.username}'
        return context


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'account/profile_edit.html'
    success_message = 'Ваш профиль обновлен'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class UserRegisterView(UserIsNotAuthenticated, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('main')
    template_name = 'account/registration/user_register.html'
    usable_password = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = Site.objects.get_current().domain
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: {current_site}{activation_url}',
            settings.SERVER_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return redirect('email_confirmation_sent')



# class UserLoginView(BSModalLoginView, SuccessMessageMixin):
#     """
#     Авторизация на сайте
#     """
#     authentication_form = UserLoginForm
#     template_name = 'account/user_login.html'
#     # next_page = 'main'
#     success_url = reverse_lazy('display')
#     success_message = 'Вы успешно авторизовались!'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Авторизация на сайте'
#         return context


class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'account/user_login.html'
    success_message = 'Вы успешно авторизовались'
    success_url = reverse_lazy('display')


class UserLogoutView(SuccessMessageMixin, LogoutView):
    """
    Выход с сайта
    """
    next_page = 'main'
    success_message = 'Вы успешно вышли из системы'


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Изменение пароля пользователя
    """
    model = Profile
    form_class = UserPasswordChangeForm
    template_name = 'account/user_password_change.html'
    success_message = 'Ваш пароль был успешно изменён!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.request.user.profile.slug})


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'account/user_password_reset.html'
    success_url = reverse_lazy('main')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлено на ваш email'
    subject_template_name = 'account/email/password_subject_reset_mail.txt'
    email_template_name = 'account/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'account/user_password_set_new.html'
    success_url = reverse_lazy('main')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'account/registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'account/registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'account/registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context
