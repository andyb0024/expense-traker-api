from rest_framework import serializers
from.models import Expense,Income

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields=["id","user","category","description","amount","updated","timestamp"]
        read_only_field=['user']


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model=Income
        fields=['user','income_amount',"source"]
        read_only_field=['user']