from django.shortcuts import render
from django.contrib import messages
from core.views import (
    TemplateViewMixin,
    ListViewMixin,
    CreateViewMixin,
    UpdateViewMixin,
    DeleteViewMixin
)
from .forms import DivisionForm, LevelForm
from apps.member.models import Division, Level
from django.http import HttpResponse
# Create your views here.


class DivisionView(ListViewMixin):
    template_name = 'division/division_view.html'
    model = Division

    def get_context_data(self, **kwargs):
        context = super(DivisionView, self).get_context_data(**kwargs)
        context['div_form'] = DivisionForm(self.request.POST)
        context['lev_form'] = LevelForm(self.request.POST)
        return context


class DivisionCreateView(CreateViewMixin):
    model = Division
    form_class = DivisionForm
    success_url = '/settings/division/'

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS,
                             'Divisi Baru Berhasil Ditambahkan!', extra_tags='success')
        return super(DivisionCreateView, self).form_valid(form)


class DivisionUpdateView(UpdateViewMixin):
    model = Division
    form_class = DivisionForm
    success_url = '/settings/division/'

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS,
                             'Divisi Berhasil Diubah!', extra_tags='success')
        return super(DivisionUpdateView, self).form_valid(form)


class DivisionDeleteView(DeleteViewMixin):
    model = Division
    success_url = '/settings/division/'

    def get(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Divisi Berhasil Di Hapus!', extra_tags='error')
        return self.post(*args, **kwargs)


class DivisionLevelCreateView(CreateViewMixin):
    model = Level
    form_class = LevelForm
    success_url = '/settings/division/'

    def form_valid(self, form):
        object = form.save(commit=False)
        division = Division.objects.get(pk=self.kwargs.get('div_pk'))
        object.division = division
        object.save()

        return super(DivisionLevelCreateView, self).form_valid(form)


class DivisionLevelUpdateView(UpdateViewMixin):
    model = Level
    form_class = LevelForm
    success_url = '/settings/division/'

    def form_valid(self, form):
        object = form.save(commit=False)
        division = Division.objects.get(pk=self.kwargs.get('div_pk'))
        object.division = division
        object.save()
        messages.add_message(self.request, messages.SUCCESS,
                             'Level Pada Divisi {} Berhasil Diubah!'.format(
                                 division.name),
                             extra_tags='success')
        return super(DivisionLevelUpdateView, self).form_valid(form)


class DivisionLevelDeleteView(DeleteViewMixin):
    model = Level
    success_url = '/settings/division/'

    def get(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Level Berhasil Di Hapus!', extra_tags='error')
        return self.post(*args, **kwargs)
