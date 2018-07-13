import csv
import os
import string

from typing import (
    Dict,
    Optional
)


class RussianWorkingCalendarParser(object):
    """
    Класс реализует парсинг csv-файла открытых данных производственного календаря Российской Федерации.
    https://data.gov.ru/opendata/7708660670-proizvcalendar
    """

    def __init__(
        self,
        path_to_file,  # type: str
    ):
        """
        :param path_to_file: путь к csv-файлу
        :type path_to_file: str
        """

        if not os.path.isfile(path_to_file):
            raise IOError('Файл по указанному пути не существует: {}.'.format(path_to_file))

        self._data = {}

        with open(path_to_file, mode='r', encoding='utf-8', newline='') as reading_file:
            next(reading_file)  # пропускаем первую строку

            reader = csv.reader(reading_file, delimiter=',', quotechar='\"')

            for (
                year,  # год
                january,  # январь
                february,  # февраль
                march,  # март
                april,  # апрель
                may,  # май
                june,  # июнь
                july,  # июль
                august,  # август
                september,  # сентябрь
                october,  # октябрь
                november,  # ноябрь
                december,  # декабрь
                workdays_counter,  # всего рабочих дней
                holidays_counter,  # всего праздничных и выходных дней
                working_hours_40,  # количество рабочих часов при 40-часовой рабочей неделе
                working_hours_36,  # количество рабочих часов при 36-часовой рабочей неделе
                working_hours_24,  # количество рабочих часов при 24-часовой рабочей неделе
            ) in reader:
                year_parsed = int(year)

                self._data[year_parsed] = {
                    'months': {},
                    'workdays_counter': int(workdays_counter),
                    'holidays_counter': int(holidays_counter),
                    'working_hours_40': float(working_hours_40),
                    'working_hours_36': float(working_hours_36),
                    'working_hours_24': float(working_hours_24),
                }

                self._data[year_parsed]['months'] = self._parse_months(
                    january,
                    february,
                    march,
                    april,
                    may,
                    june,
                    july,
                    august,
                    september,
                    october,
                    november,
                    december,
                )

    @staticmethod
    def _parse_days(
        month,  # type: str
    ):
        # type: (...) -> Dict

        """
        Метод предназначен для получения словаря со списками чисел для конкретного месяца.

        :param month: строка вида "3,4+,30*", отражающая конкретные числа месяца
        Суффиксы:
            '+' — перенесенный выходной
            '*' — сокращенный рабочий день
        :type month: str

        :return: возвращает словарь, где ключи:
            'holidays_and_weekends' — множество, содержащее целочисленные значения (праздники и выходные)
            'shortened_days' — множество, содержащее целочисленные значения (сокращенные рабочие дни)
        :rtype: Dict
        """

        holidays_and_weekends = set()
        shortened_days = set()

        days = month.split(',')
        for day in days:
            flag_shortened = False  # является ли день сокращенным рабочим днем

            if '*' in day:
                flag_shortened = True

            day_translated = int(day.translate(str.maketrans('', '', string.punctuation)))

            if flag_shortened:
                shortened_days.add(day_translated)
            else:
                holidays_and_weekends.add(day_translated)

        return {
            'holidays_and_weekends': holidays_and_weekends,
            'shortened_days': shortened_days,
        }

    def _parse_months(
        self,
        *months,  # type: str
    ):
        # type: (...) -> Dict

        """
        Метод предназначен для получения словаря с данными по месяцам конкретного года.

        :param *months: набор строк вида "3,4+,30*", отражающих конкретные числа месяцев по порядку от января до декабря
        Суффиксы:
            '+' — перенесенный выходной
            '*' — сокращенный рабочий день
        :type *months: str

        :return: возвращает словарь, где ключи
            1-12 — номер месяца по порядку от января до декабря,
            а значение — словарь (см. метод '_parse_days')
        :rtype: Dict
        """

        result = {}

        for (index, month) in enumerate(months, start=1):
            result[index] = self._parse_days(month)

        return result

    def get(
        self,
        year=None,  # type: Optional[int]
    ):
        # type: (...) -> Dict

        """
        Метод возвращает распарсенные данные производственного календаря.

        :param year: год
        :type year: Optional[int]

        :return: словарь с данными произвеодственного календаря
        :rtype: Dict
        """

        if year is None:
            return self._data

        return self._data.get(year)
