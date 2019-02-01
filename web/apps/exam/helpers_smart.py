import numpy as np
import pandas as pd

from apps.exam.models import Profile
from .models import AssesmentWeight
from apps.settings.helpers import SettingConfigurator


class SMARTEntity:
    id = ''
    pk = ''
    nik = ''
    accuracy = 0
    speed = 0
    technique = 0
    physic = 0
    mental = 0
    knowledge = 0
    utility = 0
    total = 0
    status = ''


class SMARTFormula:

    def __init__(self, levelling_info):
        self.__PASSED_SCORE = SettingConfigurator.get_value_by_property(
            'NILAI_KELULUSAN')

        self.__levelling_info = levelling_info
        self.__weight = AssesmentWeight.objects.get(
            level__name=levelling_info.level)
        self.__weight_normalization = []
        self.__df = []
        self.__df2 = []

    def __queryset_to_dataframe(self):
        # Get specific record from table Levelling
        queryset = self.__levelling_info.levellings.values(
            'id',
            'profile__user__username',
            'accuracy_point',
            'speed_point',
            'technique_point',
            'physic_point',
            'mental_point',
            'knowledge_point'
        )
        # Convert django queryset to pandas dataframe
        self.__df = pd.DataFrame.from_records(queryset)

    # Normalize data by division with max value in column
    def __compute_each_score(self):
        self.__weight_normalization = np.array([
            self.__weight.accuracy,
            self.__weight.speed,
            self.__weight.technique,
            self.__weight.physic,
            self.__weight.mental,
            self.__weight.knowledge
        ]) / 100

        self.__queryset_to_dataframe()

        self.__df2 = self.__df[[
            'accuracy_point',
            'speed_point',
            'technique_point',
            'physic_point',
            'mental_point',
            'knowledge_point'
        ]]

        df3 = self.__df2.multiply(self.__weight_normalization)
        return df3

    def __compute_each_utility(self, df):
        d_max = df.max(axis=1)
        d_min = df.min(axis=1)
        d_int = d_max - d_min

        res = df.subtract(d_max, axis=0).abs()
        n_res = res.divide(d_int, axis=0)
        n_res = n_res.multiply(self.__weight_normalization)
        return n_res

    def compute(self):
        total = self.__compute_each_score()
        utility = self.__compute_each_utility(self.__df2)
        utility['total'] = utility.sum(axis=1)
        utility['id'] = self.__df['id']
        utility['profile__user__username'] = self.__df['profile__user__username']

        # self.__df['total'] = total.sum(axis=1)
        # self.__df['status'] = np.where(
        #     self.__df['total'] >= float(self.__PASSED_SCORE), 'LULUS', 'TIDAK LULUS')
        # self.__df['utility'] = utility.sum(axis=1)

        id = 1
        results = []
        for i, df in utility.iterrows():
            # Assign dataframe value(row by row) into entity object
            smart_entity = SMARTEntity()
            smart_entity.id = id
            smart_entity.pk = df['id']
            smart_entity.nik = df['profile__user__username']
            smart_entity.accuracy = df['accuracy_point']
            smart_entity.speed = df['speed_point']
            smart_entity.technique = df['technique_point']
            smart_entity.physic = df['physic_point']
            smart_entity.mental = df['mental_point']
            smart_entity.knowledge = df['knowledge_point']
            smart_entity.total = df['total']
            # smart_entity.status = df['status']
            # smart_entity.utility = df['utility']

            # Assign entity object into list of results
            results.append(smart_entity)
            id += 1

        return results
