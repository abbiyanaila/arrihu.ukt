"""
Dashboard View Classes
"""
from django.shortcuts import render
from core.views import (
    ViewMixin
)
from apps.member import models as m_model
from apps.exam import models as e_model
from apps.organization import models as o_model
from . import helpers
# Create your views here.


class DashboardView(ViewMixin):
    """
    Dashboard View
    """
    template_name = 'dashboard/dashboard_view.html'

    def get(self, request):
        context = {}
        profiles = m_model.Profile.objects.all()
        context['member_total'] = profiles.exclude(
            user__is_superuser=True).count()
        context['coach_total'] = profiles.filter(
            user__is_staff=True).count()
        context['branch_total'] = m_model.Organization.objects.all().count() - 1
        context['gender_data'] = [
            {
                'label': 'Pria',
                'data': [profiles.filter(gender='pria').count()]
            },
            {
                'label': 'Wanita',
                'data': [profiles.filter(gender='wanita').count()]
            },
        ]
        context['age_data'] = helpers.get_age_degrees(profiles)
        return render(request, self.template_name, context)
