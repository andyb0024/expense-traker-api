from django.conf import settings
from django.db import models
import datetime
from Authentication.models import MyUser
from django.db.models import Sum, Avg, Count
from django.utils import timezone


# Create your models here.
#EXPENSE
CATEGORY_OPTIONS = [
    ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
    ('TRAVEL', 'TRAVEL'),
    ('TRANSPORT', 'TRANSPORT'),
    ('FOOD', 'FOOD'),
    ('RENT', 'RENT'),
    ('OTHERS', 'OTHERS')
]
#INCOME
SOURCE_OPTIONS = [
    ('SALARY', 'SALARY'),
    ('BUSINESS', 'BUSINESS'),
    ('SIDE-HUSTLES', 'SIDE-HUSTLES'),
    ('OTHERS', 'OTHERS')
]


class ExpenseQueryManager(models.query.QuerySet):
    def recent(self):
        return self.order_by('-timestamp')

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(timestamp__gte=start_date)
        return self.filter(timestamp__gte=start_date).filter(timestamp__lte=end_date)

    def by_weeks_range(self, weeks_ago=1, numbers_of_weeks=1):
        if numbers_of_weeks > weeks_ago:
            numbers_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7
        days_ago_end = days_ago_start - (numbers_of_weeks * 7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date, end_date=end_date)

    def by_date(self):
        now = timezone.now()
        return self.filter(timestamp__day=now.day)

    def by_month(self):
        now = timezone.now()
        return self.filter(timestamp__month=now.month)


class ExpenseManager(models.Manager):
    def get_queryset(self):
        return ExpenseQueryManager(self.model, using=self.db)


class Expense(models.Model):
    user = models.ForeignKey(MyUser, default=1, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    description = models.CharField(max_length=1000)
    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)

    objects = ExpenseManager()

    def __str__(self):
        return self.category


class Income(models.Model):
    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255,default=False)
    user = models.ForeignKey(MyUser, default=1, on_delete=models.CASCADE)
    income_amount = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "income:%s" % (self.income_amount)
