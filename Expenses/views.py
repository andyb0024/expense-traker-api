from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from Expenses.models import Expense, Income
from Expenses.serializers import ExpenseSerializer, IncomeSerializer
from.permissions import IsOwner

class ExpenseListAPIView(ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwner)
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all().recent()


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


# get the day expenses
class ExpenseByDay(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwner)

    def get(self, request):
        qs = Expense.objects.all().recent()
        qs_exp = qs.filter(owner=request.user).by_date()
        serializer = ExpenseSerializer(qs_exp, many=True)
        day_sum = qs_exp.aggregate(Sum('amount'))['amount__sum']
        return Response({'daily_sum': day_sum if day_sum else 0, 'objects': serializer.data})

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseByWeek(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)

    # authentication_classes = [SessionAuthentication]
    def get(self, request):
        qs = Expense.objects.all().recent().by_weeks_range(weeks_ago=10, numbers_of_weeks=10)
        qs_exp = qs.filter(owner=request.user)
        serializer = ExpenseSerializer(qs_exp, many=True)
        week_sum = qs_exp.aggregate(Sum('amount'))['amount__sum']
        return Response({'weekly_sum': week_sum if week_sum else 0, 'objects': serializer.data})


class IncomeListView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)

    def get_object(self, pk):
        try:
            return Income.objects.get(pk=pk)
        except Income.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = IncomeSerializer(qs)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = IncomeSerializer(qs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
