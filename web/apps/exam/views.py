from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy

from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from core.views import (
    TemplateViewMixin,
    ListViewMixin,
    CreateViewMixin,
    UpdateViewMixin,
    DetailViewMixin,
    DeleteViewMixin,
    ViewMixin
)

from apps.exam.models import AssesmentWeight, Levelling, LevellingInfo
from apps.exam.forms import AssesmentWeightForm, LevellingInfoForm, LevellingForm
from apps.division.models import Level
from apps.member.models import Profile
from apps.settings.helpers import SettingConfigurator
from .helpers_saw import SAWFormula
from .helpers_smart import SMARTFormula
# Create your views here.


class LevellingInfoView(ListViewMixin):
    template_name = 'exam/levelling_info_add.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(LevellingInfoView, self).get_context_data(**kwargs)
        context['levelling_infos'] = LevellingInfo.objects.all().order_by(
            '-date')[:5]
        context['levels'] = Level.objects.all()
        context['form'] = LevellingInfoForm(self.request.POST)
        return context

    def get_queryset(self):
        return Profile.objects.exclude(user__is_superuser=True)


class LevellingInfoCreateView(ViewMixin):
    def post(self, request):
        form = LevellingInfoForm(self.request.POST)
        if form.is_valid():
            lev_info = LevellingInfo()
            lev_info.location = form.cleaned_data['location']

            level = Level.objects.get(pk=request.POST['level'])
            lev_info.level = level.name
            lev_info.division = level.division.name

            exam_weight = AssesmentWeight.objects.get(level=level)
            lev_info.accuracy_weight = exam_weight.accuracy
            lev_info.speed_weight = exam_weight.speed
            lev_info.technique_weight = exam_weight.technique
            lev_info.physic_weight = exam_weight.physic
            lev_info.knowledge_weight = exam_weight.knowledge
            lev_info.mental_weight = exam_weight.mental

            setting = SettingConfigurator.get_setting_by_property(
                'NILAI_KELULUSAN')
            lev_info.pass_score = setting.value

            lev_info.save()

            messages.add_message(self.request, messages.SUCCESS,
                                 'Ujian Berhasil Dibuat!', extra_tags='success')

        return redirect('exam:view')


class LevellingListView(ViewMixin):
    template_name = 'exam/levelling_list.html'

    def get(self, request, lev_info_pk):
        lev_info = LevellingInfo.objects.get(pk=lev_info_pk)
        data = {
            'lev_info': lev_info
        }
        if lev_info.levellings.count() > 0:
            saw_formula = SAWFormula(lev_info)
            saw_result = saw_formula.compute()

            data['saw_results'] = saw_result

            smart_formula = SMARTFormula(lev_info)
            smart_result = smart_formula.compute()

            data['smart_results'] = smart_result

        return render(request, self.template_name, data)


class LevellingAddView(ViewMixin):
    template_name = 'exam/levelling_add.html'

    def get(self, request, lev_info_pk):
        lev_info = LevellingInfo.objects.get(pk=lev_info_pk)

        data = {
            'profiles': Profile.objects.filter(level__name=lev_info.level),
            'lev_info': lev_info,
            'form': LevellingForm(request.POST)
        }

        return render(request, self.template_name, data)


class LevellingCreateView(ViewMixin):
    def post(self, request, lev_info_pk):
        form = LevellingForm(request.POST)
        if form.is_valid():
            levelling = Levelling()

            profile = Profile.objects.get(pk=request.POST['profile'])
            levelling.profile = profile

            lev_info = LevellingInfo.objects.get(pk=lev_info_pk)
            levelling.lev_info = lev_info

            levelling.accuracy_point = form.cleaned_data['accuracy_point']
            levelling.speed_point = form.cleaned_data['speed_point']
            levelling.technique_point = form.cleaned_data['technique_point']
            levelling.physic_point = form.cleaned_data['physic_point']
            levelling.knowledge_point = form.cleaned_data['knowledge_point']
            levelling.mental_point = form.cleaned_data['mental_point']
            levelling.save()

            messages.add_message(self.request, messages.SUCCESS,
                                 'Data UKT Berhasil Disimpan!', extra_tags='success')
            return redirect('exam:lev_list', lev_info_pk)

        else:
            return redirect('exam:lev_add', lev_info_pk)


class LevellingDeleteView(DeleteViewMixin):
    model = Levelling

    def get(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Nilai Levelling Berhasil Di Hapus!', extra_tags='error')
        return self.post(*args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('exam:lev_list', kwargs={
            'lev_info_pk': self.kwargs.get('lev_info_pk'),
        })


class ExamWeightView(ListViewMixin):
    template_name = 'exam/weight/weight_list.html'
    model = AssesmentWeight

    def get_context_data(self, **kwargs):
        context = super(ExamWeightView, self).get_context_data(**kwargs)
        context['levels'] = Level.objects.exclude(
            assesmentweight__isnull=False)

        context['form'] = AssesmentWeightForm(self.request.POST or None)
        list_data = []
        for assw in AssesmentWeight.objects.all():
            data_as_dict = {
                'id': assw.id,
                'division': assw.level.division.name,
                'level': assw.level.name,
                'accuracy': assw.accuracy,
                'speed': assw.speed,
                'technique': assw.technique,
                'knowledge': assw.knowledge,
                'physic': assw.physic,
                'mental': assw.mental,
                'total': sum(
                    [assw.accuracy, assw.speed, assw.technique,
                        assw.knowledge, assw.physic, assw.mental]
                ),
            }
            list_data.append(data_as_dict)

        context['object_list'] = list_data

        return context


class ExamWeightCreateView(CreateViewMixin):
    model = AssesmentWeight
    form_class = AssesmentWeightForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        level = Level.objects.get(pk=self.request.POST['level'])
        obj.level = level
        obj.save()

        messages.add_message(self.request, messages.SUCCESS,
                             'Bobot Berhasil Ditambahkan!', extra_tags='success')

        return redirect('exam:w_view')

    def form_invalid(self, form):
        return HttpResponse(form.errors)


class ExamWeightEditView(ListViewMixin):
    template_name = 'exam/weight/weight_list_edit.html'
    model = AssesmentWeight

    def get_context_data(self, **kwargs):
        context = super(ExamWeightEditView, self).get_context_data(**kwargs)
        context['levels'] = Level.objects.all()

        context['object'] = self.get_object()

        data = {
            'technique': self.get_object().technique,
            'speed': self.get_object().speed,
            'accuracy': self.get_object().accuracy,
            'physic': self.get_object().physic,
            'knowledge': self.get_object().knowledge,
            'mental': self.get_object().mental,
        }
        context['form'] = AssesmentWeightForm(initial=data)

        list_data = []
        for assw in AssesmentWeight.objects.all():
            data_as_dict = {
                'id': assw.id,
                'division': assw.level.division.name,
                'level': assw.level.name,
                'accuracy': assw.accuracy,
                'speed': assw.speed,
                'technique': assw.technique,
                'knowledge': assw.knowledge,
                'physic': assw.physic,
                'mental': assw.mental,
                'total': sum(
                    [assw.accuracy, assw.speed, assw.technique,
                        assw.knowledge, assw.physic, assw.mental]
                ),
            }
            list_data.append(data_as_dict)

        context['object_list'] = list_data

        return context

    def get_object(self):
        return AssesmentWeight.objects.get(pk=self.kwargs.get('pk'))


class ExamWeightUpdateView(UpdateViewMixin):
    model = AssesmentWeight
    form_class = AssesmentWeightForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        level = Level.objects.get(pk=self.request.POST['level'])
        obj.level = level
        obj.save()

        messages.add_message(self.request, messages.SUCCESS,
                             'Bobot Berhasil Di ubah!', extra_tags='success')

        return redirect('exam:w_view')

    def form_invalid(self, form):
        return HttpResponse(form.errors)


class ExamWeightDeleteView(DeleteViewMixin):
    model = AssesmentWeight
    success_url = '/exam/weight'

    def get(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Bobot Berhasil Di Hapus!', extra_tags='error')
        return self.post(*args, **kwargs)
