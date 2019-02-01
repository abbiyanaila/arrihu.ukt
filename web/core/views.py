from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.template.loader import get_template

from vanilla import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    View,
    FormView
)

from braces.views import (
    LoginRequiredMixin,
    SuperuserRequiredMixin,
    StaffuserRequiredMixin
)


class TemplateViewMixin(LoginRequiredMixin, StaffuserRequiredMixin, TemplateView):
    login_url = '/login/'


class ListViewMixin(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    login_url = '/login/'


class CreateViewMixin(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):
    login_url = '/login/'


class UpdateViewMixin(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):
    login_url = '/login/'


class DetailViewMixin(LoginRequiredMixin, StaffuserRequiredMixin, DetailView):
    login_url = '/login/'


class DeleteViewMixin(LoginRequiredMixin, StaffuserRequiredMixin, DeleteView):
    login_url = '/login/'


class ViewMixin(LoginRequiredMixin, StaffuserRequiredMixin, View):
    login_url = '/login/'


class FormViewMixin(LoginRequiredMixin, StaffuserRequiredMixin, FormView):
    login_url = '/login/'


def serviceworker(request, js):
    template = get_template('sw.js')
    return HttpResponse(template.render(), content_type="application/x-javascript")


def offline_page(request, page):
    template = get_template('info/offline.html')
    return HttpResponse(template.render())
