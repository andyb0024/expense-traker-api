from django.urls import path
from . import views

urlpatterns = [
    path('expenses', views.ExpenseListAPIView.as_view(), name="expenses"),
    path('daily', views.ExpenseByDay.as_view(), name='day-list-api'),
    path('weekly', views.ExpenseByWeek.as_view(), name='week-list-api'),
    path('income/<int:pk>', views.IncomeListView.as_view(), name="amount-apis"),
    # path('income', views.IncomeListView.as_view(), name='amount-apis'),
]
