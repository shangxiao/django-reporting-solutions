from django.urls import path

from .views import fortnight_sales_totals

urlpatterns = [
    path(
        "fortnight_sales_totals/", fortnight_sales_totals, name="fortnight_sales_totals"
    ),
]
