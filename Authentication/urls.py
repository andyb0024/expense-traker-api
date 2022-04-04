from django.urls import path

from .views import (RegisterView)

urlpatterns = [
     path('create-user', RegisterView.as_view(),name='create'),
     # path('add-expense', AddExpenseView.as_view(), name='add'),
     # path('delete/<int:pk>/', DeleteExpenseView.as_view(),name='delete'),
     # path('week-expense/', ExpenseByWeek.as_view(), name='week-list-apis'),
     # path('day-expense/', ExpenseByDay.as_view(), name='day-list-apis'),
     # path('month-expense/', ExpenseByDay.as_view(), name='month-list-apis'),
     # path('income/', IncomeApiView.as_view(), name='list'),
]