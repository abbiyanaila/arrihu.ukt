import pandas as pd
import numpy as np

from apps.exam.models import Profile
from .models import AssesmentWeight
from apps.settings.helpers import SettingConfigurator


class SAWEntity:
    id = ''
    pk = ''
    nik = ''
    accuracy = 0
    speed = 0
    technique = 0
    physic = 0
    mental = 0
    knowledge = 0
    total = 0
    status = ''


class SAWFormula:
    def __init__(self, levelling_info):
        self.__levelling_info = levelling_info
        self.__PASSED_SCORE = SettingConfigurator.get_value_by_property(
            'NILAI_KELULUSAN')
        self.__weight = AssesmentWeight.objects.get(
            level__name=levelling_info.level)

        self.__df = []
        self.__final_df = []

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
    def __normalize(self, df, cols=[]):
        df_cols = df[cols]
        col_max = df_cols.max()
        self.__final_df = df_cols / col_max

    # Method to do normalize by excecuting __normalize method
    def __do_normalize(self):
        cols = [
            'accuracy_point',
            'speed_point',
            'technique_point',
            'physic_point',
            'mental_point',
            'knowledge_point'
        ]
        self.__normalize(self.__df, cols)

    # Normalize weight
    def __weight_normalization(self):
        weight = np.array([
            self.__weight.accuracy,
            self.__weight.speed,
            self.__weight.technique,
            self.__weight.physic,
            self.__weight.mental,
            self.__weight.knowledge
        ])/100
        self.__final_df = self.__final_df * weight

    # Create column total and assign it value
    def __count_total(self):
        self.__final_df['total'] = self.__final_df.sum(axis=1)
        self.__final_df['total'] *= 100

    # Final calculation and reshape the structure of dataframe
    def compute(self):
        self.__queryset_to_dataframe()
        self.__do_normalize()
        self.__weight_normalization()
        self.__count_total()

        self.__df['total'] = self.__final_df['total']
        self.__df['status'] = np.where(
            self.__final_df['total'] >= float(self.__PASSED_SCORE), 'LULUS', 'TIDAK LULUS')

        # Convert pandas dataframe into list
        id = 1
        results = []
        for i, df in self.__df.iterrows():
            # Assign dataframe value(row by row) into entity object
            saw_entity = SAWEntity()
            saw_entity.id = id
            saw_entity.pk = df['id']
            saw_entity.nik = df['profile__user__username']
            saw_entity.accuracy = df['accuracy_point']
            saw_entity.speed = df['speed_point']
            saw_entity.technique = df['technique_point']
            saw_entity.physic = df['physic_point']
            saw_entity.mental = df['mental_point']
            saw_entity.knowledge = df['knowledge_point']
            saw_entity.total = df['total']
            saw_entity.status = df['status']

            # Assign entity object into list of results
            results.append(saw_entity)

            id += 1
        return results
