from rest_framework import serializers
from .models import Expense,Income


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'owner', 'timestamp', 'description', 'amount', 'category']



class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model=Income
        fields=['income_amount']
        read_only_field=['user']