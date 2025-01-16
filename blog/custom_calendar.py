from calendar import HTMLCalendar

class BlogHTMLCalendar(HTMLCalendar):

    def __init__(self, year):
        self.year = year
        return super(BlogHTMLCalendar, self).__init__()
    

    def formatyear(self):
        return super().formatyear(self.year)

