from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractMonth
import calendar
calendar.setfirstweekday(calendar.SUNDAY)  # would like this to be set when init


class BlogHTMLCalendar(calendar.Calendar):
    def __init__(self, year, posts_list):
        self.year = year
        self.posts_list = posts_list
        self.monthly_tally, self.month_list = self.get_monthly_tally()



    def get_monthly_tally(self):
        monthly_tally = self.posts_list \
            .order_by("created_on") \
            .values(month=ExtractMonth("created_on")) \
            .order_by("month") \
            .distinct()

        month_list = [query_pair["month"] for query_pair in monthly_tally]

        return monthly_tally, month_list


    def print_posts_list(self):
        print(self.monthly_tally)
        print(self.month_list)



    def printyear(self):
        month_counter = 1

        cal_html = '<table class="year" border="0" cellpadding="0" cellspacing="0">'

        # Yearly archive link
        cal_html += '<tr><th class="year" colspan="3">'
        cal_html += self.get_yearly_archive()
        cal_html += '</th></tr>'


        for calendar_rows in range(4):  # Three months per row; four rows per year.
            cal_html += '<tr>'

            for cal_row_month in range(3):  # Each month table inside its own <td>.
                cal_html += '<td>'
                cal_html += self.print_month(month_counter)  # Format the monthly calendar here.
                month_counter += 1
                cal_html += '</td>'


            cal_html += '</tr>'

        cal_html += '</table>'

        #self.print_posts_list()

        return cal_html


    def get_yearly_archive(self):
        """
        Formats the year number with a link to that year's archives.
        """
        yearly_archive_url = reverse('archive_year', args=[self.year])
        return '<a href="%s"><h3>%s</h3></a>'%(yearly_archive_url, self.year)
    

    def print_month(self, month_number):
        """
        Formats the month calendar.
        Month name is a link to that month's archives.
        To do: Day is a link to that day's archives, if available.
        """
        month_html = '<table class="month" border="0" cellpadding="0" cellspacing="0">'

        # Monthly archive link
        month_html += '<tr><th class="month" colspan="7">'
        month_html += self.get_monthly_archive(month_number)
        month_html += '</th></tr>'

        # Week header
        month_html += '<tr>'
        month_html += '<th class="day_of_the_week">Sun</th>'
        month_html += '<th class="day_of_the_week">Mon</th>'
        month_html += '<th class="day_of_the_week">Tue</th>'
        month_html += '<th class="day_of_the_week">Wed</th>'
        month_html += '<th class="day_of_the_week">Thu</th>'
        month_html += '<th class="day_of_the_week">Fri</th>'
        month_html += '<th class="day_of_the_week">Sat</th>'
        month_html += '</tr>'

        # weeks of the month
        weeks_of_the_month = calendar.monthcalendar(self.year, month_number)
        for week in weeks_of_the_month:
            
            month_html += '<tr>'

            for day in week:
                month_html += '<td class="day_of_the_month">'

                if day == 0:
                    month_html += '&nbsp;'
                else:
                    month_html += str(day)  # link to the day's archives here

                month_html += '</td>'

            month_html += '</tr>'


        month_html += '</table>'

        return month_html

    def get_monthly_archive(self, month_number):
        if month_number in self.month_list:
            monthly_archive_url = reverse('archive_month', args=[self.year, month_number])
            return '<a href="%s">%s</a>'%(monthly_archive_url, calendar.month_name[month_number])
        else:
            return str(calendar.month_name[month_number])






