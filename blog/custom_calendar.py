from calendar import HTMLCalendar

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
        cal_html += str(self.year)  # format the calendar year link here
        cal_html += '!'  # FOR TESTING PURPOSE
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


