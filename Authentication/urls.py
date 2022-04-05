from django.urls import path

from .views import (RegisterView,VerifyEmail)

urlpatterns = [
     path('register', RegisterView.as_view(),name='register'),
     path('email-verify', VerifyEmail.as_view(), name='email-verify'),
     # path('add-expense', AddExpenseView.as_view(), name='add'),
     # path('delete/<int:pk>/', DeleteExpenseView.as_view(),name='delete'),
     # path('week-expense/', ExpenseByWeek.as_view(), name='week-list-apis'),
     # path('day-expense/', ExpenseByDay.as_view(), name='day-list-apis'),
     # path('month-expense/', ExpenseByDay.as_view(), name='month-list-apis'),
     # path('income/', IncomeApiView.as_view(), name='list'),
]