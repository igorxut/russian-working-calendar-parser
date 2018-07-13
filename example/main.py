from russian_working_calendar_parser import RussianWorkingCalendarParser


if __name__ == '__main__':
    calendar = RussianWorkingCalendarParser('data-20180410T1145-structure-20180410T1145.csv')

    print('all:')
    print(calendar.get())
    print('\n2018 year:')
    print(calendar.get(2018))
