from django.db import connection, models
from django.db.models.expressions import Func

from .models import Order


def get_orders_by_priority():
    return Order.objects.all()


def get_orders_by_priority():  # noqa F811
    return Order.objects.order_by(
        Func(
            ["IN_PROGRESS", "PAID", "SHIPPED", "DELIVERED"],
            "status",
            function="array_position",
        )
    )


def get_order_leaderboard():
    class OrderTotals(models.Model):
        category = models.CharField(primary_key=True)
        total = models.IntegerField()

    totals = OrderTotals.objects.raw(
        """\
        select 'Total' as category, 0 as total
        """
    )

    return [{"category": o.category, "total": o.total} for o in totals]


def get_order_leaderboard():  # noqa F811
    class OrderTotals(models.Model):
        category = models.CharField(primary_key=True)
        total = models.IntegerField()

    totals = OrderTotals.objects.raw(
        """\
        select coalesce(product, 'Total') as category,
               count(product) as total
        from reports_order
        group by rollup(product)
        order by total desc
        limit 6
        """
    )

    return [{"category": o.category, "total": o.total} for o in totals]


def get_order_leaderboard_with_other():
    class OrderTotals(models.Model):
        category = models.CharField(primary_key=True)
        total = models.IntegerField()

    totals = OrderTotals.objects.raw(
        """\
        select 'Total' as category, 0 as total
        """
    )

    return [{"category": o.category, "total": o.total} for o in totals]


def get_order_leaderboard_with_other():  # noqa F811
    class OrderTotals(models.Model):
        category = models.CharField(primary_key=True)
        total = models.IntegerField()

    totals = OrderTotals.objects.raw(
        """\
        select category,
               sum(total)::integer as total
        from (
            select case when row_number() over () > 6 then 'Other'
                        else initial_board.category
                   end as category,
                   initial_board.total
            from (
                select coalesce(product, 'Total') as category,
                       count(product) as total
                from reports_order
                group by rollup(product)
                order by total desc
            ) initial_board
        ) final_board
        group by category
        order by category = 'Other', total desc
        """
    )

    return [{"category": o.category, "total": o.total} for o in totals]


def get_order_leaderboard_by_store():
    class OrderTotals(models.Model):
        category = models.CharField(primary_key=True)
        total = models.IntegerField()

    totals = OrderTotals.objects.raw(
        """\
        select 'Total' as category, 0 as total
        """
    )

    return [{"category": o.category, "total": o.total} for o in totals]


def get_order_leaderboard_by_store():  # noqa F811
    class OrderTotals(models.Model):
        category = models.CharField(primary_key=True)
        total = models.IntegerField()

    totals = OrderTotals.objects.raw(
        """\
        select category,
               total
        from (
            select *,
                   row_number() over (partition by store) as i
            from (
                select *,
                       max(total) over (partition by store) as store_total
                from (
                    SELECT store,
                           case when store is null and product is null then 'Total'
                                when product is null then concat_ws(' ', store, 'Total')
                                else product
                           end as category,
                           count(*) AS total
                    FROM reports_order
                    GROUP BY rollup(store, product)
                )
                order by store_total desc, total desc
            )
        )
        where i <= 4
        order by store_total desc, total desc
        """
    )

    return [{"category": o.category, "total": o.total} for o in totals]


def get_set_from_db(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return [row[0] for row in cursor.fetchall()]


def series_1_to_10():
    return get_set_from_db("select generate_series(1, 10, 1)")


def series_even_numbers_to_20():
    return get_set_from_db("select generate_series(2, 20, 2)")


def series_date_range_jan_2025():
    return get_set_from_db(
        "select generate_series('2025-01-01'::timestamptz, '2025-01-31'::timestamptz, '1 day'::interval)"
    )


def sales_report():
    class Sales(models.Model):
        # doesn't matter about uniqueness, just need to set a primary_key to stop Django from complaining
        date = models.DateField(primary_key=True)
        store = models.CharField()
        total = models.IntegerField()

    qs = Sales.objects.raw(
        """\
        select '2025-01-01'::date as date,
               '???' as store,
               0 as total
        """
    )

    return [
        {"date": s.date.strftime("%Y-%m-%d"), "store": s.store, "total": s.total}
        for s in qs
    ]


def sales_report():  # noqa F811
    class Sales(models.Model):
        # doesn't matter about uniqueness, just need to set a primary_key to stop Django from complaining
        date = models.DateField(primary_key=True)
        store = models.CharField()
        total = models.IntegerField()

    qs = Sales.objects.raw(
        """\
        select matrix.date,
               matrix.store,
               coalesce(sum(reports_sale.sale), 0) as total
        from (
            select series.timestamptz as date,
                   reports_store.id as store_id,
                   concat_ws(' ', reports_store.address, reports_store.city) as store
            from generate_series('2025-01-01'::timestamptz, '2025-01-31'::timestamptz, '1 day'::interval) series,
                 reports_store
        ) matrix
        left join reports_sale on (
            reports_sale.timestamp::date = matrix.date and reports_sale.store_id = matrix.store_id
        )
        group by matrix.date, matrix.store
        order by matrix.store, matrix.date
        """
    )

    return [
        {"date": s.date.strftime("%Y-%m-%d"), "store": s.store, "total": s.total}
        for s in qs
    ]


def sales_report_by_fortnight():
    class Sales(models.Model):
        # doesn't matter about uniqueness, just need to set a primary_key to stop Django from complaining
        date = models.DateField(primary_key=True)
        store = models.CharField()
        total = models.IntegerField()

    qs = Sales.objects.raw(
        """\
        select '2025-01-01'::date as date,
               '???' as store,
               0 as total
        """
    )

    return [
        {"date": s.date.strftime("%Y-%m-%d"), "store": s.store, "total": s.total}
        for s in qs
    ]


def sales_report_by_fortnight():  # noqa F811
    class Sales(models.Model):
        # doesn't matter about uniqueness, just need to set a primary_key to stop Django from complaining
        date = models.DateField(primary_key=True)
        store = models.CharField()
        total = models.IntegerField()

    qs = Sales.objects.raw(
        """\
        select matrix.date,
               concat_ws(' ', matrix.address, matrix.city) as store,
               coalesce(sum(reports_sale.sale), 0) as total
        from (
            select series.timestamptz as date,
                   reports_store.id as store_id,
                   reports_store.city,
                   reports_store.address
            from generate_series('2025-01-01'::timestamptz, '2025-01-31'::timestamptz, '14 days'::interval) series,
                 reports_store
        ) matrix
        left join reports_sale on (
            matrix.date <= reports_sale.timestamp and reports_sale.timestamp < (matrix.date + '14 days'::interval) and reports_sale.store_id = matrix.store_id
        )
        group by matrix.date, matrix.city, matrix.address
        order by matrix.city = 'Sydney' desc, matrix.city = 'Melbourne' desc, matrix.address, matrix.date
        """
    )

    return [
        {"date": s.date.strftime("%Y-%m-%d"), "store": s.store, "total": s.total}
        for s in qs
    ]


def sporadic_sales_report():
    class Sales(models.Model):
        start_date = models.DateField(primary_key=True)
        end_date = models.DateField()
        total = models.IntegerField()

    qs = Sales.objects.raw(
        """\
        select '2025-01-01'::date as start_date,
               '2025-01-01'::date as end_date,
               0 as total
        """
    )

    return [
        {
            "date_range": s.start_date.strftime("%Y-%m-%d")
            + " -> "
            + s.end_date.strftime("%Y-%m-%d"),
            "total": s.total,
        }
        for s in qs
    ]


def sporadic_sales_report():  # noqa F811
    class Sales(models.Model):
        start_date = models.DateField(primary_key=True)
        end_date = models.DateField()
        total = models.IntegerField()

    qs = Sales.objects.raw(
        """\
        select
            min(date) as start_date,
            max(date) as end_date,
            sum(sale) as total
        from (
            select timestamp::date as date,
                   sale,
                   row_number() over (order by timestamp) as i
            from reports_sale
            order by i
        )
        group by date - make_interval(days => i::int)
        order by start_date
        """
    )

    return [
        {
            "date_range": (
                s.start_date.strftime("%Y-%m-%d")
                + (
                    " -> " + s.end_date.strftime("%Y-%m-%d")
                    if s.end_date != s.start_date
                    else ""
                )
            ),
            "total": s.total,
        }
        for s in qs
    ]


def series_1_to_10_recursive():
    return get_set_from_db("select limit 0")


def series_1_to_10_recursive():  # noqa F811
    return get_set_from_db(
        """\
        with recursive series as (
            select 1 as counter
            union
            select counter + 1 from series
            where counter < 10
        )
        select * from series
        """
    )


def show_reporting_chain():
    return get_set_from_db("select limit 0")


def show_reporting_chain():  # noqa F811
    return get_set_from_db(
        """\
        with recursive org_chart as (
            select name,
                   name as path
            from reports_employee where manager_id is null

            union

            select reports_employee.name,
                   concat_ws(' -> ', reports_employee.name, org_chart.path)
            from reports_employee
            inner join org_chart on reports_employee.manager_id = org_chart.name
        )
        select path from org_chart
        """
    )
