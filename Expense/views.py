from django.db.models import Sum
from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics,permissions
from rest_framework.views import APIView
from .models import Expense, Income
from .serializers import ExpenseSerializer, IncomeSerializer


# Create your views here.
class ExpenseItemAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user.id
        qs = Expense.objects.all().recent()
        qs_exp = qs.filter(user=user)
        print(qs_exp)
        serializer = ExpenseSerializer(qs_exp, many=True)
        return Response(serializer.data)


class AddExpenseView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class DeleteExpenseView(APIView):
    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk)
        except Expense.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ExpenseSerializer(snippet)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# get the week expenses
class ExpenseByWeek(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Expense.objects.all().recent().by_weeks_range(weeks_ago=10, numbers_of_weeks=10)
        x = Expense.objects.all().by_weeks_range(weeks_ago=10, numbers_of_weeks=10)
        print(x)
        qs_exp = qs.filter(user=request.user.id)
        serializer = ExpenseSerializer(qs_exp, many=True)
        week_sum = qs_exp.aggregate(Sum('amount'))['amount__sum']
        context = {
            'weekly_sum': week_sum if week_sum else 0,
            'objects': serializer.data
        }

        return Response(context)


# get the day expenses
class ExpenseByDay(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    def get(self, request):
        qs = Expense.objects.all().recent()
        qs_exp = qs.filter(user=request.user.id).by_date()
        serializer = ExpenseSerializer(qs_exp, many=True)
        day_sum = qs_exp.aggregate(Sum('amount'))['amount__sum']
        context = {
            'daily_sum': day_sum if day_sum else 0,
            'objects': serializer.data
        }
        return Response(context)


# get the month expenses
class ExpenseByMonth(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [SessionAuthentication]
    def get(self, request):
        qs = Expense.objects.all().recent()
        qs_exp = qs.filter(user=request.user.id).by_month()
        serializer = ExpenseSerializer(qs_exp, many=True)
        month_sum = qs_exp.aggregate(Sum('amount'))['amount__sum']
        context = {
            'month_sum': month_sum if month_sum else 0,
            'objects': serializer.data
        }
        return Response(context)


class IncomeApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        qs = Income.objects.all()
        income_qs = qs.filter(user=request.user)
        serializer = IncomeSerializer(income_qs, many=True)
        return Response(serializer.data)


