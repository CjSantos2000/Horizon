from django.urls import path

from . import views

urlpatterns = [
    path("", views.BusinessView.as_view(), name="business"),
    path("add-business/", views.AddBusinessView.as_view(), name="add-business"),
    path(
        "add-business/add-users/",
        views.AddBusinessUsersView.as_view(),
        name="add-business-users",
    ),
    path("<pk>/", views.BusinessDetailView.as_view(), name="business-detail"),
    path(
        "<pk>/add-income/",
        views.AddBusinessIncomeView.as_view(),
        name="add-business-income",
    ),
    path(
        "<pk>/add-expense/",
        views.AddBusinessExpenseView.as_view(),
        name="add-business-expense",
    ),
    path(
        "<pk>/business-chart-data/",
        views.BusinessChartDataView.as_view(),
        name="business-chart-data",
    ),
]
