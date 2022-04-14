import datetime

from django.db import models
from django.utils import timezone

from Authentication.models import MyUser

# Create your models here.
CATEGORY_OPTIONS = [
    ('ONLINE_SERVICES', 'os'),
    ('TRAVEL', 'tr'),
    ('FOOD', 'foo'),
    ('RENT', 're'),
    ('OTHERS', 'oth')
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


class ExpenseManager(models.Manager):
    def get_queryset(self):
        return ExpenseQueryManager(self.model, using=self.db)


class Expense(models.Model):
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=MyUser, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExpenseManager()

    class Meta:
        ordering: ['-updated_at']

    def __str__(self):
        return str(self.owner) + 's income'


class Income(models.Model):
    owner = models.ForeignKey(to=MyUser, null=True, on_delete=models.CASCADE)
    income_amount=models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return "income:%s"% (self.income_amount)