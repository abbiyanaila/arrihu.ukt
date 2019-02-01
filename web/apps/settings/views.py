from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from vanilla import View
from core.views import (
    TemplateViewMixin,
    ListViewMixin,
    CreateViewMixin,
    UpdateViewMixin,
    DeleteViewMixin,
    FormViewMixin
)

from . import forms
from .helpers import SettingConfigurator
from core.models import Setting
# Create your views here.


class LoginView(View):
    template_name = 'settings/login.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            return redirect('/dashboard/')

        form = forms.UserLoginForm(self.request.POST)
        context_data = {
            'form': form
        }

        return render(request, self.template_name, context_data)

    def post(self, request, **kwargs):
        form = forms.UserLoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth = authenticate(username=username, password=password)
            if auth:
                login(request, auth)

                if 'next' in request.GET:
                    return redirect(request.GET['next'])

                return redirect('/dashboard/')
            else:
                messages.add_message(self.request, messages.ERROR,
                                     'Username dan Password Tidak Ditemukan',
                                     extra_tags='error')
                return self.get(request)


class AccountSettingView(TemplateViewMixin):
    template_name = 'settings/account_setting.html'

    def get_context_data(self, **kwargs):
        context = super(AccountSettingView, self).get_context_data(**kwargs)
        context['form'] = PasswordChangeForm(self.request.POST)

        return context


class AccountSettingUpdateView(FormViewMixin):

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(self.request, messages.SUCCESS,
                                 'Password berhasil Diubah',
                                 extra_tags='success')

        return redirect('settings:view')


class AdditionalSettingListView(ListViewMixin):
    template_name = 'settings/additional_settings.html'
    model = Setting

    def get_context_data(self, **kwargs):
        context = super(AdditionalSettingListView,
                        self).get_context_data(**kwargs)
        context['form'] = forms.SettingForm(self.request.POST)

        return context


class AdditionalSettingCreateView(CreateViewMixin):
    model = Setting
    form_class = forms.SettingForm

    def form_valid(self, form):
        property = form.cleaned_data['property']
        if SettingConfigurator.get_setting_by_property(property):
            messages.add_message(self.request, messages.WARNING,
                                 'Maaf Pengaturan dengan Kata Kunci {} sudah ada'.format(
                                     property),
                                 extra_tags='warning')
        else:
            form.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 'Pengaturan Berhasil Disimpan',
                                 extra_tags='success')

        return redirect('settings:additional_settings')


class AdditionalSettingEditListView(ListViewMixin):
    template_name = 'settings/additional_settings_edit.html'
    model = Setting

    def get_context_data(self, **kwargs):
        context = super(AdditionalSettingEditListView,
                        self).get_context_data(**kwargs)
        setting = SettingConfigurator.get_setting_by_id(self.kwargs.get('pk'))
        context['instance'] = setting
        context['form'] = forms.SettingForm(initial={
            'property': setting.property,
            'value': setting.value,
        })

        return context


class AdditionalSettingUpdateView(UpdateViewMixin):
    model = Setting
    form_class = forms.SettingForm

    def form_valid(self, form):
        property = form.cleaned_data['property']
        setting = SettingConfigurator.get_setting_by_property(property)
        if setting:
            if setting.property != property:
                messages.add_message(self.request, messages.WARNING,
                                     'Maaf Pengaturan dengan Kata Kunci {} sudah ada'.format(
                                         property),
                                     extra_tags='warning')
                return redirect('settings:additional_settings_edit', self.kwargs.get('pk'))

        form.save()
        messages.add_message(self.request, messages.SUCCESS,
                             'Pengaturan Berhasil Disimpan',
                             extra_tags='success')

        return redirect('settings:additional_settings')


class AdditionalSettingDeleteView(DeleteViewMixin):
    model = Setting
    success_url = '/settings/additional_settings/'

    def get(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Pengaturan Berhasil Di Hapus!', extra_tags='error')
        return self.post(*args, **kwargs)
