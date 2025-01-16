from calendar import HTMLCalendar
from django.urls import reverse


class BlogHTMLCalendar(HTMLCalendar):
    def __init__(self, year):
        self.year = year
        super(BlogHTMLCalendar, self).__init__()
        super(BlogHTMLCalendar, self).setfirstweekday(6)


    def formatyear(self):
        return super().formatyear(self.year)


    def printyear(self):
        month_counter = 1

        cal_html = '<table class="year" border="0" cellpadding="0" cellspacing="0">'
        cal_html += '	<tr><th class="year" colspan="3">'
        cal_html += self.get_yearly_archive()  # format the calendar year link here
        cal_html += '</th></tr>'


        for calendar_rows in range(4):  # three months per row, four rows per year
            cal_html += '<tr>'

            for cal_row_month in range(3):  # each month table inside its own td
                cal_html += '<td>'
                cal_html += super().formatmonth(self.year, month_counter, withyear=False)
                month_counter += 1
                cal_html += '</td>'


            cal_html += '</tr>'
        cal_html += '</table>'

        return cal_html


    def get_yearly_archive(self):
        yearly_archive_url = reverse('archive_year', args=[self.year])
        return '<a href="%s"><h3>%s</h3></a>'%(yearly_archive_url, self.year)


