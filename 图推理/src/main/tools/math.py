# -*- coding:utf-8 -*-

"""
数学工具：提供判断两个数的大于、大于等于、小于、小于等于、等于的判断
"""


class MathTools:
    @staticmethod
    def bigger_than(value, base, tolerance=1e-5):
        """
        判断 value 是否大于 base
        :param value:
        :param base:
        :param tolerance:
        :return:
        """
        if value > base + tolerance:
            return True
        else:
            return False

    @staticmethod
    def equals_or_bigger_than(value, base, tolerance=1e-5):
        """
        判断 value 是否大于或等于 base
        :param value:
        :param base:
        :param tolerance:
        :return:
        """
        if value > base + tolerance:
            return True
        elif abs(value - base) < tolerance:
            return True
        else:
            return False

    @staticmethod
    def smaller_than(value, base, tolerance=1e-5):
        """
        判断 value 是否小于 base
        :param value:
        :param base:
        :param tolerance:
        :return:
        """

        if value < base - tolerance:
            return True
        else:
            return False

    @staticmethod
    def equal_or_smaller_than(value, base, tolerance=1e-5):
        """
        判断 value 是否小于或等于 base
        :param value:
        :param base:
        :param tolerance:
        :return:
        """
        if value < base - tolerance:
            return True
        elif abs(value - base) < tolerance:
            return True
        else:
            return False

    @staticmethod
    def is_equal(value, base, tolerance=1e-5):
        """
        判断 value 是否等于 base
        :param value:
        :param base:
        :param tolerance:
        :return:
        """

        if abs(value - base) < tolerance:
            return True
        else:
            return False

    @staticmethod
    def is_in_region(value, lower_bound, upper_bound, tolerance=1e-5):
        if MathTools.equals_or_bigger_than(value, lower_bound, tolerance=tolerance) and \
                MathTools.equal_or_smaller_than(value, upper_bound, tolerance):
            return True
        else:
            return False
