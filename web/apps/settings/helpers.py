from core.models import Setting
import json


class SettingConfigurator:

    @staticmethod
    def get_setting_by_id(id):
        setting = Setting.objects.filter(pk=id).first()
        if setting:
            return setting
        return None

    @staticmethod
    def get_setting_by_property(property):
        setting = Setting.objects.filter(property=property).first()
        if setting:
            return setting
        return None

    @staticmethod
    def get_value_by_property(property):
        setting = Setting.objects.filter(property=property).first()
        if setting:
            return setting.value
        return None
