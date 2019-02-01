from django.shortcuts import render, redirect
from django.contrib import messages
from core.views import (
    TemplateViewMixin,
    ListViewMixin,
    CreateViewMixin,
    UpdateViewMixin,
    DeleteViewMixin
)
from apps.member.models import Organization
from .forms import OrganizationForm
# Create your views here.


class OrganizationView(ListViewMixin):
    template_name = 'organization/organization_add.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationView, self).get_context_data(**kwargs)
        context['form'] = OrganizationForm(self.request.POST)
        return context


class OrganizationCreateView(CreateViewMixin):
    model = Organization
    form_class = OrganizationForm
    success_url = '/setup/organization/'

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS,
                             'Organisasi Baru Berhasil Ditambahkan!', extra_tags='success')
        return super(OrganizationCreateView, self).form_valid(form)


class OrganizationEditView(ListViewMixin):
    template_name = 'organization/organization_edit.html'
    model = Organization

    def get_context_data(self, **kwargs):
        context = super(OrganizationEditView, self).get_context_data(**kwargs)
        context['form'] = OrganizationForm(initial={
            'name': self.get_object().name,
            'description': self.get_object().description
        })
        context['object'] = self.get_object()
        return context

    def get_object(self):
        return Organization.objects.get(pk=self.kwargs.get('pk'))


class OrganizationUpdateView(UpdateViewMixin):
    model = Organization
    form_class = OrganizationForm
    success_url = '/setup/organization/'

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS,
                             'Organisasi Berhasil Diubah!', extra_tags='success')
        return super(OrganizationUpdateView, self).form_valid(form)


class OrganizationDeleteView(ListViewMixin):
    def get(self, request, pk):
        org = Organization.objects.get(pk=pk)
        if org:
            org.delete()
            messages.add_message(self.request, messages.ERROR,
                                 'Organisasi Berhasil Dihapus!', extra_tags='error')
            return redirect('org:view')
