import os
import json
from datetime import date
from django.contrib import messages
from django.core.files import File
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseNotFound
from django.core.urlresolvers import reverse_lazy
from core.views import (
    TemplateViewMixin,
    ListViewMixin,
    CreateViewMixin,
    UpdateViewMixin,
    DetailViewMixin,
    DeleteViewMixin,
    ViewMixin
)
from apps.member.models import Profile, Physic
from .forms import (
    ProfileForm,
    PhysicForm
)
from . import helpers

# from .helpers import write_image_from_url_to_disk
# Create your views here.


class MemberListView(ListViewMixin):
    template_name = 'profile/profile_list.html'
    model = Profile

    def get_queryset(self):
        return Profile.objects.all().exclude(user__is_superuser=True)


class MemberAddView(TemplateViewMixin):
    template_name = 'profile/profile_add.html'

    def get_context_data(self, **kwargs):
        context = super(MemberAddView, self).get_context_data(**kwargs)
        context['user_form'] = UserCreationForm(self.request.POST)
        context['profile_form'] = ProfileForm(
            self.request.POST, self.request.FILES)
        context['physic_form'] = PhysicForm(self.request.POST)
        return context


class MemberCreateView(CreateViewMixin):
    model = Profile
    form_class = ProfileForm

    def form_valid(self, form):
        # qrcodeurl = self.request.POST['qrcodeurl']
        # img = write_image_from_url_to_disk(qrcodeurl)

        object = form.save(commit=False)

        u_form = UserCreationForm(self.request.POST)
        phy_form = PhysicForm(self.request.POST)
        if u_form.is_valid():
            user = u_form.save()
            object.user = user
            object.gender = form.cleaned_data['gender']
            if phy_form.is_valid():
                physic = phy_form.save()
                object.physic = physic

            # object.qrcode.save('qrcode.jpg', File(img), save=True)

                object.save()
                messages.add_message(self.request, messages.SUCCESS,
                                     'Tambah Anggota Baru Berhasil', extra_tags='success')
                return redirect('member:view')
            else:
                return HttpResponse(phy_form.errors)
        else:
            return HttpResponse(u_form.errors)

    def form_invalid(self, form):
        return HttpResponse(form.errors)


class MemberDetailView(DetailViewMixin):
    template_name = 'profile/profile_detail.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)

        try:
            profile = Profile.objects.get(pk=self.kwargs.get('pk'))
        except Profile.DoesNotExist:
            return HttpResponseNotFound()

        return context


class MemberEditView(TemplateViewMixin):
    template_name = 'profile/profile_edit.html'

    def get_context_data(self, **kwargs):
        context = super(MemberEditView, self).get_context_data(**kwargs)

        profile = Profile.objects.filter(pk=self.kwargs.get('pk')).first()
        profile_data = {
            'name': profile.name,
            'address': profile.address,
            'gender': profile.gender,
            'born_place': profile.born_place,
            'born_date': profile.born_date,
            'religion': profile.religion,
            'identity_number': profile.identity_number,
            'phone': profile.phone,
            'email': profile.email,
            'level': profile.level,
            'organization': profile.organization,
            'picture': profile.picture,
            # 'qrcode': profile.qrcode
        }
        physic_data = {
            'body_height': profile.physic.body_height,
            'body_weight': profile.physic.body_weight,
            'arm_span': profile.physic.arm_span,
            'full_draw': profile.physic.full_draw,
            'over_draw': profile.physic.over_draw,
            'blood_group': profile.physic.blood_group,
            'hospital_history': profile.physic.hospital_history,
        }

        context['profile'] = profile
        context['profile_form'] = ProfileForm(initial=profile_data)
        context['physic_form'] = PhysicForm(initial=physic_data)
        context['password_form'] = PasswordChangeForm(
            profile.user, self.request.POST)
        return context


class MemberUpdateView(UpdateViewMixin):
    template_name = 'profile/profile_edit.html'
    model = Profile
    form_class = ProfileForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.get_object().user
        obj.gender = form.cleaned_data['gender']

        phy_form = PhysicForm(
            self.request.POST, instance=self.get_object().physic)
        if phy_form.is_valid():
            obj.physic = phy_form.save()

            obj.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 'Ubah Data Anggota Berhasil', extra_tags='success')
            return redirect('member:view')
        return HttpResponse('Failed')

    def form_invalid(self, form):
        return HttpResponse(form.errors)

    def get_object(self):
        return Profile.objects.get(pk=self.kwargs.get('pk'))


class MemberDeleteView(ViewMixin):
    def get(self, request, pk):
        profile = Profile.objects.filter(pk=pk).first()
        if profile:
            profile.delete()
            return redirect('member:view')


class MemberPasswordChangeView(ViewMixin):
    template_name = 'profile/profile_edit.html'

    def post(self, request, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs.get('pk'))
        form = PasswordChangeForm(profile.user, request.POST)
        if form.is_valid():
            user = profile.user
            user.set_password(form.cleaned_data['new_password2'])
            user.save()
            messages.add_message(self.request, messages.SUCCESS,
                                 'Password Anda Berhasil Diubah!', extra_tags='success')
            return reverse_lazy('member:edit', kwargs={'pk': profile.pk})
        else:
            return HttpResponse(form.error_messages)
