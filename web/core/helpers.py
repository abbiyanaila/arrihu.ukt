CONSTANTS = 100


class BaseFormula:

    @staticmethod
    def accuracy_formula(kwargs):
        point_target = kwargs['point_target']
        point_achievement = kwargs['point_achievement']
        result = (point_achievement / point_target) * CONSTANTS
        if result > 100:
            return 100
        return result

    @staticmethod
    def speed_formula(kwargs):
        time_target = kwargs['time_target']
        time_achievement = kwargs['time_achievement']

        hit_target = kwargs['hit_target']
        hit_achievement = kwargs['hit_achievement']

        time_raw_result = (time_target / time_achievement) * CONSTANTS
        time_result = time_raw_result * (0.6)

        hit_raw_result = (hit_achievement / hit_target) * CONSTANTS
        hit_result = hit_raw_result * (0.4)

        result = time_result + hit_result
        if result > 100:
            return 100
        return result

    @staticmethod
    def technique_formula(kwargs):
        score_target = kwargs['score_target']

        kwargs.pop('score_target')

        print(kwargs)
        if kwargs['khatra_ft'] == 0:
            kwargs.pop('khatra_ft')

        total = sum(kwargs.values())
        average = total / len(kwargs)

        result = (average / score_target) * CONSTANTS
        if result > 100:
            return 100
        return result

    @staticmethod
    def physic_formula(kwargs):
        time_target = kwargs['time_target']
        quantity_target = kwargs['quantity_target']
        technique_target = kwargs['technique_target']

        time_achievement = kwargs['time_achievement']
        quantity_achievement = kwargs['quantity_achievement']
        technique_achievement = kwargs['technique_achievement']

        target_raw_total = quantity_target / time_target
        achievement_raw_total = quantity_achievement / time_achievement
        achievement_total = (achievement_raw_total /
                             target_raw_total) * CONSTANTS

        technique_total = (technique_achievement /
                           technique_target) * CONSTANTS
        result = (achievement_total * 0.5) + (technique_total * 0.5)
        if result > 100:
            return 100
        return result
