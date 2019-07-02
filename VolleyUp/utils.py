from calendar import HTMLCalendar
from VolleyUp.models import Training

PL_DAYS = {

    0: 'PON',
    1: 'WT',
    2: 'ŚR',
    3: 'CZW',
    4: 'PT',
    5: 'SOB',
    6: 'NDZ',

}


PL_MONTHS = {

    1: 'Styczeń',
    2: 'Luty',
    3: 'Marzec',
    4: 'Kwiecień',
    5: 'Maj',
    6: 'Czerwiec',
    7: 'Lipiec',
    8: 'Sierpień',
    9: 'Wrzesień',
    10: 'Październik',
    11: 'Listopad',
    12: 'Grudzień',

}


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, trainings):
        trainings_per_day = trainings.filter(start_time__day=day)
        d = ''
        for training in trainings_per_day:
            d += f"<li> {training.get_html_url} </li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, trainings):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, trainings)
        return f"<tr> {week} </tr>"

    def formatmonth(self, request, withyear=True):
        print(request.user.organization.all())
        trainings = Training.objects.filter(start_time__year=self.year, start_time__month=self.month, organization=org)
        for org in request.user.organization.all():
            print(org)
            trainings_for_user = trainings.filter()

            # else:
            #     trainings = Training.objects.filter(start_time__year=self.year, start_time__month=self.month,
            #                                         organization=org).filter(organization=org)
        print("DUPADUPA", trainings_for_user)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, trainings)}\n'
        return cal

    def formatweekday(self, day):
        return '<th class="%s">%s</th>' % (self.cssclasses[day], PL_DAYS[day])

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (PL_MONTHS[themonth], theyear)
        else:
            s = '%s' % PL_MONTHS[themonth]
        return '<tr><th colspan="7" class="month">%s</th></tr>' % s
