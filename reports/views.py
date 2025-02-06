from django.shortcuts import render

from .services import sales_report_by_fortnight


def fortnight_sales_totals(request):
    sales = sales_report_by_fortnight()
    return render(
        request,
        "reports/fortnight_sales_totals.html",
        context={
            # A convenience thing to render the report header
            "dates": list(dict.fromkeys(r["date"] for r in sales)),
            "sales": sales,
        },
    )
