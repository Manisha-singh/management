import datetime

from django.db import models
from django.utils import timezone

from user_management.models import UserDetail


class Book(models.Model):
    name = models.CharField(max_length=350)
    author = models.CharField(max_length=350)
    book_number = models.CharField(max_length=13)
    issued_status = models.BooleanField(default=False)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.name


class Issue(models.Model):
    user_detail = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=False)
    issued = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    returned = models.BooleanField(default=False)
    return_date = models.DateTimeField(auto_now=False, auto_created=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return "{}_{} book issue request".format(self.user_detail, self.book)

    def days_no(self):
        if self.issued:
            y, m, d = str(timezone.now().date()).split('-')
            today = datetime.date(int(y), int(m), int(d))
            y2, m2, d2 = str(self.return_date.date()).split('-')
            lastdate = datetime.date(int(y2), int(m2), int(d2))
            if lastdate > today:
                return "left"
            else:
                return "passed"
        else:
            return ""
