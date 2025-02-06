from datetime import datetime, timezone

import pytest
from django.urls import reverse
from pytest_django.asserts import assertInHTML

from reports.services import (
    sales_report,
    sales_report_by_fortnight,
    series_1_to_10,
    series_date_range_jan_2025,
    series_even_numbers_to_20,
    sporadic_sales_report,
)

from .models import Sale, Store

pytestmark = pytest.mark.django_db


def test_series_1_to_10():
    """
    Use the database to generate a series of integers from 1 -> 10!
    """
    assert series_1_to_10() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_series_even_numbers_to_20():
    """
    Awesome 🏆, now generate even numbers from 2 -> 20!
    """
    assert series_even_numbers_to_20() == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]


def test_series_date_range_jan_2025():
    """
    Also using the DB, generate timestamps from 1st Jan 2025 -> 31st Jan 2025
    """
    assert series_date_range_jan_2025() == [
        datetime(2025, 1, 1, tzinfo=timezone.utc),
        datetime(2025, 1, 2, tzinfo=timezone.utc),
        datetime(2025, 1, 3, tzinfo=timezone.utc),
        datetime(2025, 1, 4, tzinfo=timezone.utc),
        datetime(2025, 1, 5, tzinfo=timezone.utc),
        datetime(2025, 1, 6, tzinfo=timezone.utc),
        datetime(2025, 1, 7, tzinfo=timezone.utc),
        datetime(2025, 1, 8, tzinfo=timezone.utc),
        datetime(2025, 1, 9, tzinfo=timezone.utc),
        datetime(2025, 1, 10, tzinfo=timezone.utc),
        datetime(2025, 1, 11, tzinfo=timezone.utc),
        datetime(2025, 1, 12, tzinfo=timezone.utc),
        datetime(2025, 1, 13, tzinfo=timezone.utc),
        datetime(2025, 1, 14, tzinfo=timezone.utc),
        datetime(2025, 1, 15, tzinfo=timezone.utc),
        datetime(2025, 1, 16, tzinfo=timezone.utc),
        datetime(2025, 1, 17, tzinfo=timezone.utc),
        datetime(2025, 1, 18, tzinfo=timezone.utc),
        datetime(2025, 1, 19, tzinfo=timezone.utc),
        datetime(2025, 1, 20, tzinfo=timezone.utc),
        datetime(2025, 1, 21, tzinfo=timezone.utc),
        datetime(2025, 1, 22, tzinfo=timezone.utc),
        datetime(2025, 1, 23, tzinfo=timezone.utc),
        datetime(2025, 1, 24, tzinfo=timezone.utc),
        datetime(2025, 1, 25, tzinfo=timezone.utc),
        datetime(2025, 1, 26, tzinfo=timezone.utc),
        datetime(2025, 1, 27, tzinfo=timezone.utc),
        datetime(2025, 1, 28, tzinfo=timezone.utc),
        datetime(2025, 1, 29, tzinfo=timezone.utc),
        datetime(2025, 1, 30, tzinfo=timezone.utc),
        datetime(2025, 1, 31, tzinfo=timezone.utc),
    ]


@pytest.fixture
def setup_sales():
    bourke = Store.objects.create(city="Melbourne", address="Bourke St")
    collins = Store.objects.create(city="Melbourne", address="Collins St")
    george = Store.objects.create(city="Sydney", address="George St")
    # no sales at all for Oxford St, it was closed for maintenance!
    Store.objects.create(city="Sydney", address="Oxford St")
    fixture = [
        # Bourke St store
        (bourke, "2025-01-01T08:30:00Z", 150),
        (bourke, "2025-01-01T12:15:00Z", 200),
        (bourke, "2025-01-01T15:45:00Z", 120),
        # no data for 2nd!
        (bourke, "2025-01-03T09:00:00Z", 190),
        (bourke, "2025-01-03T13:30:00Z", 220),
        (bourke, "2025-01-03T16:00:00Z", 180),
        (bourke, "2025-01-04T11:15:00Z", 160),
        (bourke, "2025-01-04T15:00:00Z", 140),
        (bourke, "2025-01-04T19:00:00Z", 250),
        (bourke, "2025-01-05T08:45:00Z", 210),
        (bourke, "2025-01-05T12:30:00Z", 180),
        (bourke, "2025-01-05T17:00:00Z", 190),
        (bourke, "2025-01-06T10:15:00Z", 170),
        (bourke, "2025-01-06T13:00:00Z", 185),
        (bourke, "2025-01-06T16:30:00Z", 210),
        (bourke, "2025-01-07T09:45:00Z", 200),
        (bourke, "2025-01-07T14:15:00Z", 220),
        (bourke, "2025-01-07T18:00:00Z", 230),
        (bourke, "2025-01-08T08:30:00Z", 240),
        (bourke, "2025-01-08T11:00:00Z", 170),
        (bourke, "2025-01-08T14:30:00Z", 220),
        (bourke, "2025-01-09T10:45:00Z", 160),
        (bourke, "2025-01-09T13:30:00Z", 180),
        (bourke, "2025-01-09T18:45:00Z", 200),
        (bourke, "2025-01-10T09:30:00Z", 150),
        (bourke, "2025-01-10T13:00:00Z", 210),
        (bourke, "2025-01-10T16:15:00Z", 190),
        (bourke, "2025-01-11T10:00:00Z", 175),
        (bourke, "2025-01-11T14:00:00Z", 230),
        (bourke, "2025-01-11T19:30:00Z", 250),
        (bourke, "2025-01-12T08:15:00Z", 180),
        (bourke, "2025-01-12T12:30:00Z", 210),
        (bourke, "2025-01-12T15:45:00Z", 220),
        (bourke, "2025-01-13T09:00:00Z", 200),
        (bourke, "2025-01-13T13:15:00Z", 220),
        (bourke, "2025-01-13T16:30:00Z", 190),
        (bourke, "2025-01-14T10:30:00Z", 160),
        (bourke, "2025-01-14T14:45:00Z", 175),
        (bourke, "2025-01-14T18:00:00Z", 230),
        (bourke, "2025-01-15T08:00:00Z", 190),
        (bourke, "2025-01-15T12:00:00Z", 210),
        (bourke, "2025-01-15T15:30:00Z", 220),
        # no data for 16th!
        (bourke, "2025-01-17T08:30:00Z", 200),
        (bourke, "2025-01-17T12:45:00Z", 210),
        (bourke, "2025-01-17T17:00:00Z", 180),
        (bourke, "2025-01-18T09:00:00Z", 240),
        (bourke, "2025-01-18T13:30:00Z", 220),
        (bourke, "2025-01-18T18:15:00Z", 210),
        (bourke, "2025-01-19T10:00:00Z", 150),
        (bourke, "2025-01-19T13:45:00Z", 230),
        (bourke, "2025-01-19T17:30:00Z", 190),
        (bourke, "2025-01-20T08:15:00Z", 200),
        (bourke, "2025-01-20T12:00:00Z", 220),
        (bourke, "2025-01-20T16:30:00Z", 230),
        (bourke, "2025-01-21T09:30:00Z", 170),
        (bourke, "2025-01-21T14:15:00Z", 185),
        (bourke, "2025-01-21T18:00:00Z", 250),
        (bourke, "2025-01-22T10:00:00Z", 190),
        (bourke, "2025-01-22T14:30:00Z", 220),
        (bourke, "2025-01-22T17:45:00Z", 200),
        (bourke, "2025-01-23T09:00:00Z", 150),
        (bourke, "2025-01-23T12:15:00Z", 170),
        (bourke, "2025-01-23T16:00:00Z", 210),
        (bourke, "2025-01-24T08:30:00Z", 240),
        (bourke, "2025-01-24T11:45:00Z", 180),
        (bourke, "2025-01-24T15:30:00Z", 190),
        (bourke, "2025-01-25T09:00:00Z", 200),
        (bourke, "2025-01-25T13:15:00Z", 230),
        (bourke, "2025-01-25T18:00:00Z", 210),
        (bourke, "2025-01-26T10:30:00Z", 190),
        (bourke, "2025-01-26T14:00:00Z", 220),
        (bourke, "2025-01-26T17:30:00Z", 230),
        (bourke, "2025-01-27T09:45:00Z", 160),
        (bourke, "2025-01-27T13:30:00Z", 175),
        (bourke, "2025-01-27T16:00:00Z", 250),
        (bourke, "2025-01-28T08:15:00Z", 180),
        (bourke, "2025-01-28T12:00:00Z", 200),
        (bourke, "2025-01-28T17:30:00Z", 210),
        (bourke, "2025-01-29T10:00:00Z", 160),
        (bourke, "2025-01-29T14:30:00Z", 220),
        (bourke, "2025-01-29T18:15:00Z", 250),
        (bourke, "2025-01-30T09:30:00Z", 170),
        (bourke, "2025-01-30T13:00:00Z", 180),
        (bourke, "2025-01-30T16:45:00Z", 230),
        (bourke, "2025-01-31T08:45:00Z", 240),
        (bourke, "2025-01-31T12:30:00Z", 220),
        (bourke, "2025-01-31T15:30:00Z", 210),
        # Collins St store
        (collins, "2025-01-01T08:00:00Z", 120),
        (collins, "2025-01-01T12:00:00Z", 220),
        (collins, "2025-01-01T15:00:00Z", 150),
        (collins, "2025-01-02T09:30:00Z", 180),
        (collins, "2025-01-02T13:30:00Z", 210),
        (collins, "2025-01-02T17:30:00Z", 200),
        (collins, "2025-01-03T08:45:00Z", 170),
        (collins, "2025-01-03T12:45:00Z", 240),
        (collins, "2025-01-03T16:30:00Z", 180),
        (collins, "2025-01-04T10:00:00Z", 130),
        (collins, "2025-01-04T14:15:00Z", 210),
        (collins, "2025-01-04T18:30:00Z", 230),
        (collins, "2025-01-05T09:00:00Z", 190),
        (collins, "2025-01-05T13:15:00Z", 150),
        (collins, "2025-01-05T17:00:00Z", 220),
        (collins, "2025-01-06T09:30:00Z", 180),
        (collins, "2025-01-06T13:00:00Z", 170),
        (collins, "2025-01-06T16:30:00Z", 190),
        (collins, "2025-01-07T08:15:00Z", 220),
        (collins, "2025-01-07T12:30:00Z", 240),
        (collins, "2025-01-07T16:45:00Z", 210),
        (collins, "2025-01-08T09:00:00Z", 250),
        (collins, "2025-01-08T12:15:00Z", 180),
        (collins, "2025-01-08T16:00:00Z", 200),
        (collins, "2025-01-09T09:45:00Z", 160),
        (collins, "2025-01-09T13:00:00Z", 210),
        (collins, "2025-01-09T17:15:00Z", 230),
        (collins, "2025-01-10T08:30:00Z", 150),
        (collins, "2025-01-10T12:30:00Z", 220),
        (collins, "2025-01-10T16:00:00Z", 190),
        (collins, "2025-01-11T09:30:00Z", 170),
        (collins, "2025-01-11T13:15:00Z", 230),
        (collins, "2025-01-11T17:30:00Z", 200),
        (collins, "2025-01-12T08:00:00Z", 220),
        (collins, "2025-01-12T12:45:00Z", 240),
        (collins, "2025-01-12T16:00:00Z", 210),
        (collins, "2025-01-13T09:15:00Z", 180),
        (collins, "2025-01-13T13:30:00Z", 200),
        (collins, "2025-01-13T17:00:00Z", 220),
        (collins, "2025-01-14T08:30:00Z", 170),
        (collins, "2025-01-14T13:00:00Z", 180),
        (collins, "2025-01-14T16:45:00Z", 250),
        (collins, "2025-01-15T09:00:00Z", 190),
        (collins, "2025-01-15T12:30:00Z", 220),
        (collins, "2025-01-15T16:15:00Z", 200),
        (collins, "2025-01-16T08:45:00Z", 160),
        (collins, "2025-01-16T13:30:00Z", 240),
        (collins, "2025-01-16T17:45:00Z", 210),
        (collins, "2025-01-17T09:00:00Z", 180),
        (collins, "2025-01-17T12:45:00Z", 220),
        (collins, "2025-01-17T17:15:00Z", 230),
        (collins, "2025-01-18T09:15:00Z", 200),
        (collins, "2025-01-18T13:30:00Z", 210),
        (collins, "2025-01-18T17:00:00Z", 240),
        (collins, "2025-01-19T08:30:00Z", 250),
        (collins, "2025-01-19T13:15:00Z", 170),
        (collins, "2025-01-19T17:30:00Z", 220),
        (collins, "2025-01-20T09:00:00Z", 190),
        (collins, "2025-01-20T13:30:00Z", 200),
        (collins, "2025-01-20T17:00:00Z", 230),
        (collins, "2025-01-21T09:45:00Z", 220),
        (collins, "2025-01-21T13:00:00Z", 240),
        (collins, "2025-01-21T16:30:00Z", 210),
        (collins, "2025-01-22T08:00:00Z", 180),
        (collins, "2025-01-22T12:15:00Z", 230),
        (collins, "2025-01-22T16:30:00Z", 250),
        (collins, "2025-01-23T09:00:00Z", 200),
        (collins, "2025-01-23T12:30:00Z", 180),
        (collins, "2025-01-23T16:00:00Z", 220),
        (collins, "2025-01-24T09:30:00Z", 240),
        (collins, "2025-01-24T13:00:00Z", 210),
        (collins, "2025-01-24T16:45:00Z", 190),
        (collins, "2025-01-25T08:15:00Z", 230),
        (collins, "2025-01-25T12:30:00Z", 200),
        (collins, "2025-01-25T17:00:00Z", 220),
        (collins, "2025-01-26T09:00:00Z", 210),
        (collins, "2025-01-26T13:30:00Z", 180),
        (collins, "2025-01-26T17:15:00Z", 250),
        (collins, "2025-01-27T09:30:00Z", 160),
        (collins, "2025-01-27T13:00:00Z", 220),
        (collins, "2025-01-27T16:45:00Z", 240),
        (collins, "2025-01-28T08:45:00Z", 180),
        (collins, "2025-01-28T12:30:00Z", 210),
        (collins, "2025-01-28T16:00:00Z", 200),
        (collins, "2025-01-29T09:00:00Z", 170),
        (collins, "2025-01-29T13:15:00Z", 220),
        (collins, "2025-01-29T16:30:00Z", 230),
        (collins, "2025-01-30T09:00:00Z", 200),
        (collins, "2025-01-30T13:30:00Z", 180),
        (collins, "2025-01-30T16:45:00Z", 240),
        (collins, "2025-01-31T08:00:00Z", 250),
        (collins, "2025-01-31T12:00:00Z", 230),
        (collins, "2025-01-31T15:30:00Z", 210),
        # George St store
        (george, "2025-01-01T08:00:00Z", 135),
        (george, "2025-01-01T12:00:00Z", 210),
        (george, "2025-01-01T15:00:00Z", 180),
        (george, "2025-01-02T09:30:00Z", 190),
        (george, "2025-01-02T13:30:00Z", 230),
        (george, "2025-01-02T17:30:00Z", 170),
        (george, "2025-01-03T08:45:00Z", 160),
        (george, "2025-01-03T12:45:00Z", 240),
        (george, "2025-01-03T16:30:00Z", 180),
        (george, "2025-01-04T10:00:00Z", 220),
        (george, "2025-01-04T14:15:00Z", 185),
        (george, "2025-01-04T18:30:00Z", 210),
        (george, "2025-01-05T09:00:00Z", 250),
        (george, "2025-01-05T13:15:00Z", 150),
        (george, "2025-01-05T17:00:00Z", 200),
        (george, "2025-01-06T09:30:00Z", 190),
        (george, "2025-01-06T13:00:00Z", 180),
        (george, "2025-01-06T16:30:00Z", 220),
        (george, "2025-01-07T08:15:00Z", 210),
        (george, "2025-01-07T12:30:00Z", 240),
        (george, "2025-01-07T16:45:00Z", 185),
        (george, "2025-01-08T09:00:00Z", 170),
        (george, "2025-01-08T12:15:00Z", 200),
        (george, "2025-01-08T16:00:00Z", 180),
        (george, "2025-01-09T09:45:00Z", 240),
        (george, "2025-01-09T13:00:00Z", 210),
        (george, "2025-01-09T17:15:00Z", 250),
        (george, "2025-01-10T08:30:00Z", 160),
        (george, "2025-01-10T12:30:00Z", 190),
        (george, "2025-01-10T16:00:00Z", 220),
        (george, "2025-01-11T09:30:00Z", 230),
        (george, "2025-01-11T13:15:00Z", 210),
        (george, "2025-01-11T17:30:00Z", 180),
        (george, "2025-01-12T08:00:00Z", 190),
        (george, "2025-01-12T12:45:00Z", 220),
        (george, "2025-01-12T16:00:00Z", 170),
        (george, "2025-01-13T09:15:00Z", 210),
        (george, "2025-01-13T13:30:00Z", 180),
        (george, "2025-01-13T17:00:00Z", 250),
        (george, "2025-01-14T08:30:00Z", 240),
        (george, "2025-01-14T13:00:00Z", 220),
        (george, "2025-01-14T16:45:00Z", 190),
        (george, "2025-01-15T09:00:00Z", 200),
        (george, "2025-01-15T12:30:00Z", 210),
        (george, "2025-01-15T16:15:00Z", 230),
        (george, "2025-01-16T08:45:00Z", 150),
        (george, "2025-01-16T13:30:00Z", 240),
        (george, "2025-01-16T17:45:00Z", 210),
        (george, "2025-01-17T09:00:00Z", 180),
        (george, "2025-01-17T12:45:00Z", 220),
        (george, "2025-01-17T17:15:00Z", 240),
        (george, "2025-01-18T09:15:00Z", 250),
        (george, "2025-01-18T13:30:00Z", 210),
        (george, "2025-01-18T17:00:00Z", 180),
        (george, "2025-01-19T08:30:00Z", 170),
        (george, "2025-01-19T13:15:00Z", 230),
        (george, "2025-01-19T17:30:00Z", 210),
        (george, "2025-01-20T09:00:00Z", 240),
        (george, "2025-01-20T13:30:00Z", 200),
        (george, "2025-01-20T17:00:00Z", 180),
        (george, "2025-01-21T09:45:00Z", 210),
        (george, "2025-01-21T13:00:00Z", 220),
        (george, "2025-01-21T16:30:00Z", 200),
        (george, "2025-01-22T08:00:00Z", 250),
        (george, "2025-01-22T12:15:00Z", 180),
        (george, "2025-01-22T16:30:00Z", 240),
        (george, "2025-01-23T09:00:00Z", 220),
        (george, "2025-01-23T12:30:00Z", 200),
        (george, "2025-01-23T16:00:00Z", 230),
        (george, "2025-01-24T09:30:00Z", 180),
        (george, "2025-01-24T13:00:00Z", 210),
        (george, "2025-01-24T16:45:00Z", 250),
        (george, "2025-01-25T08:15:00Z", 190),
        (george, "2025-01-25T12:30:00Z", 240),
        (george, "2025-01-25T17:00:00Z", 220),
        (george, "2025-01-26T09:00:00Z", 170),
        (george, "2025-01-26T13:30:00Z", 200),
        (george, "2025-01-26T17:15:00Z", 230),
        (george, "2025-01-27T09:30:00Z", 180),
        (george, "2025-01-27T13:00:00Z", 250),
        (george, "2025-01-27T16:45:00Z", 220),
        (george, "2025-01-28T08:45:00Z", 240),
        (george, "2025-01-28T12:30:00Z", 210),
        (george, "2025-01-28T16:00:00Z", 200),
        (george, "2025-01-29T09:00:00Z", 220),
        (george, "2025-01-29T13:15:00Z", 180),
        (george, "2025-01-29T16:30:00Z", 250),
        (george, "2025-01-30T09:00:00Z", 230),
        (george, "2025-01-30T13:30:00Z", 210),
        (george, "2025-01-30T16:45:00Z", 190),
        (george, "2025-01-31T08:00:00Z", 200),
        (george, "2025-01-31T12:00:00Z", 240),
        (george, "2025-01-31T15:30:00Z", 220),
    ]
    Sale.objects.bulk_create(
        Sale(store=store, timestamp=timestamp, sale=sale)
        for store, timestamp, sale in fixture
    )


def test_sales_report(setup_sales):
    """
    The client has asked for a sales report that shows total sales in a 2D matrix of shop vs date.

    The resulting report would look something like:

    |----------------------+--------+--------+-------+-----|
    |                      | 1 Jan  | 2 Jan  | 3 Jan | ... |
    |----------------------+--------+--------+-------+-----|
    | Collins St Melbourne | $1,234 | $4,567 | etc   | ... |
    | George St Sydney     | $7,654 | $4,321 | etc   | ... |
    | ...                  |        |        |       |     |
    |----------------------+--------+--------+-------+-----|

    Produce a query that will do this for the month of January 2025!

    Notes:
     - Not every day will have a sale recorded, there may be gaps
     - Not every store will have sales: Oxford St is closed for maintenance!
     - Feel free to hardcode the date range in the query.

    Hints:
     - generate_series() & GROUP BY are your friend here.
     - Start by generating a 2D matrix of store x timestamp, see how you go from there!
    """
    results = sales_report()

    assert results == [
        {
            "date": "2025-01-01",
            "store": "Bourke St Melbourne",
            "total": 470,
        },
        {
            "date": "2025-01-02",
            "store": "Bourke St Melbourne",
            "total": 0,
        },
        {
            "date": "2025-01-03",
            "store": "Bourke St Melbourne",
            "total": 590,
        },
        {
            "date": "2025-01-04",
            "store": "Bourke St Melbourne",
            "total": 550,
        },
        {
            "date": "2025-01-05",
            "store": "Bourke St Melbourne",
            "total": 580,
        },
        {
            "date": "2025-01-06",
            "store": "Bourke St Melbourne",
            "total": 565,
        },
        {
            "date": "2025-01-07",
            "store": "Bourke St Melbourne",
            "total": 650,
        },
        {
            "date": "2025-01-08",
            "store": "Bourke St Melbourne",
            "total": 630,
        },
        {
            "date": "2025-01-09",
            "store": "Bourke St Melbourne",
            "total": 540,
        },
        {
            "date": "2025-01-10",
            "store": "Bourke St Melbourne",
            "total": 550,
        },
        {
            "date": "2025-01-11",
            "store": "Bourke St Melbourne",
            "total": 655,
        },
        {
            "date": "2025-01-12",
            "store": "Bourke St Melbourne",
            "total": 610,
        },
        {
            "date": "2025-01-13",
            "store": "Bourke St Melbourne",
            "total": 610,
        },
        {
            "date": "2025-01-14",
            "store": "Bourke St Melbourne",
            "total": 565,
        },
        {
            "date": "2025-01-15",
            "store": "Bourke St Melbourne",
            "total": 620,
        },
        {
            "date": "2025-01-16",
            "store": "Bourke St Melbourne",
            "total": 0,
        },
        {
            "date": "2025-01-17",
            "store": "Bourke St Melbourne",
            "total": 590,
        },
        {
            "date": "2025-01-18",
            "store": "Bourke St Melbourne",
            "total": 670,
        },
        {
            "date": "2025-01-19",
            "store": "Bourke St Melbourne",
            "total": 570,
        },
        {
            "date": "2025-01-20",
            "store": "Bourke St Melbourne",
            "total": 650,
        },
        {
            "date": "2025-01-21",
            "store": "Bourke St Melbourne",
            "total": 605,
        },
        {
            "date": "2025-01-22",
            "store": "Bourke St Melbourne",
            "total": 610,
        },
        {
            "date": "2025-01-23",
            "store": "Bourke St Melbourne",
            "total": 530,
        },
        {
            "date": "2025-01-24",
            "store": "Bourke St Melbourne",
            "total": 610,
        },
        {
            "date": "2025-01-25",
            "store": "Bourke St Melbourne",
            "total": 640,
        },
        {
            "date": "2025-01-26",
            "store": "Bourke St Melbourne",
            "total": 640,
        },
        {
            "date": "2025-01-27",
            "store": "Bourke St Melbourne",
            "total": 585,
        },
        {
            "date": "2025-01-28",
            "store": "Bourke St Melbourne",
            "total": 590,
        },
        {
            "date": "2025-01-29",
            "store": "Bourke St Melbourne",
            "total": 630,
        },
        {
            "date": "2025-01-30",
            "store": "Bourke St Melbourne",
            "total": 580,
        },
        {
            "date": "2025-01-31",
            "store": "Bourke St Melbourne",
            "total": 670,
        },
        {
            "date": "2025-01-01",
            "store": "Collins St Melbourne",
            "total": 490,
        },
        {
            "date": "2025-01-02",
            "store": "Collins St Melbourne",
            "total": 590,
        },
        {
            "date": "2025-01-03",
            "store": "Collins St Melbourne",
            "total": 590,
        },
        {
            "date": "2025-01-04",
            "store": "Collins St Melbourne",
            "total": 570,
        },
        {
            "date": "2025-01-05",
            "store": "Collins St Melbourne",
            "total": 560,
        },
        {
            "date": "2025-01-06",
            "store": "Collins St Melbourne",
            "total": 540,
        },
        {
            "date": "2025-01-07",
            "store": "Collins St Melbourne",
            "total": 670,
        },
        {
            "date": "2025-01-08",
            "store": "Collins St Melbourne",
            "total": 630,
        },
        {
            "date": "2025-01-09",
            "store": "Collins St Melbourne",
            "total": 600,
        },
        {
            "date": "2025-01-10",
            "store": "Collins St Melbourne",
            "total": 560,
        },
        {
            "date": "2025-01-11",
            "store": "Collins St Melbourne",
            "total": 600,
        },
        {
            "date": "2025-01-12",
            "store": "Collins St Melbourne",
            "total": 670,
        },
        {
            "date": "2025-01-13",
            "store": "Collins St Melbourne",
            "total": 600,
        },
        {
            "date": "2025-01-14",
            "store": "Collins St Melbourne",
            "total": 600,
        },
        {
            "date": "2025-01-15",
            "store": "Collins St Melbourne",
            "total": 610,
        },
        {
            "date": "2025-01-16",
            "store": "Collins St Melbourne",
            "total": 610,
        },
        {
            "date": "2025-01-17",
            "store": "Collins St Melbourne",
            "total": 630,
        },
        {
            "date": "2025-01-18",
            "store": "Collins St Melbourne",
            "total": 650,
        },
        {
            "date": "2025-01-19",
            "store": "Collins St Melbourne",
            "total": 640,
        },
        {
            "date": "2025-01-20",
            "store": "Collins St Melbourne",
            "total": 620,
        },
        {
            "date": "2025-01-21",
            "store": "Collins St Melbourne",
            "total": 670,
        },
        {
            "date": "2025-01-22",
            "store": "Collins St Melbourne",
            "total": 660,
        },
        {
            "date": "2025-01-23",
            "store": "Collins St Melbourne",
            "total": 600,
        },
        {
            "date": "2025-01-24",
            "store": "Collins St Melbourne",
            "total": 640,
        },
        {
            "date": "2025-01-25",
            "store": "Collins St Melbourne",
            "total": 650,
        },
        {
            "date": "2025-01-26",
            "store": "Collins St Melbourne",
            "total": 640,
        },
        {
            "date": "2025-01-27",
            "store": "Collins St Melbourne",
            "total": 620,
        },
        {
            "date": "2025-01-28",
            "store": "Collins St Melbourne",
            "total": 590,
        },
        {
            "date": "2025-01-29",
            "store": "Collins St Melbourne",
            "total": 620,
        },
        {
            "date": "2025-01-30",
            "store": "Collins St Melbourne",
            "total": 620,
        },
        {
            "date": "2025-01-31",
            "store": "Collins St Melbourne",
            "total": 690,
        },
        {
            "date": "2025-01-01",
            "store": "George St Sydney",
            "total": 525,
        },
        {
            "date": "2025-01-02",
            "store": "George St Sydney",
            "total": 590,
        },
        {
            "date": "2025-01-03",
            "store": "George St Sydney",
            "total": 580,
        },
        {
            "date": "2025-01-04",
            "store": "George St Sydney",
            "total": 615,
        },
        {
            "date": "2025-01-05",
            "store": "George St Sydney",
            "total": 600,
        },
        {
            "date": "2025-01-06",
            "store": "George St Sydney",
            "total": 590,
        },
        {
            "date": "2025-01-07",
            "store": "George St Sydney",
            "total": 635,
        },
        {
            "date": "2025-01-08",
            "store": "George St Sydney",
            "total": 550,
        },
        {
            "date": "2025-01-09",
            "store": "George St Sydney",
            "total": 700,
        },
        {
            "date": "2025-01-10",
            "store": "George St Sydney",
            "total": 570,
        },
        {
            "date": "2025-01-11",
            "store": "George St Sydney",
            "total": 620,
        },
        {
            "date": "2025-01-12",
            "store": "George St Sydney",
            "total": 580,
        },
        {
            "date": "2025-01-13",
            "store": "George St Sydney",
            "total": 640,
        },
        {
            "date": "2025-01-14",
            "store": "George St Sydney",
            "total": 650,
        },
        {
            "date": "2025-01-15",
            "store": "George St Sydney",
            "total": 640,
        },
        {
            "date": "2025-01-16",
            "store": "George St Sydney",
            "total": 600,
        },
        {
            "date": "2025-01-17",
            "store": "George St Sydney",
            "total": 640,
        },
        {
            "date": "2025-01-18",
            "store": "George St Sydney",
            "total": 640,
        },
        {
            "date": "2025-01-19",
            "store": "George St Sydney",
            "total": 610,
        },
        {
            "date": "2025-01-20",
            "store": "George St Sydney",
            "total": 620,
        },
        {
            "date": "2025-01-21",
            "store": "George St Sydney",
            "total": 630,
        },
        {
            "date": "2025-01-22",
            "store": "George St Sydney",
            "total": 670,
        },
        {
            "date": "2025-01-23",
            "store": "George St Sydney",
            "total": 650,
        },
        {
            "date": "2025-01-24",
            "store": "George St Sydney",
            "total": 640,
        },
        {
            "date": "2025-01-25",
            "store": "George St Sydney",
            "total": 650,
        },
        {
            "date": "2025-01-26",
            "store": "George St Sydney",
            "total": 600,
        },
        {
            "date": "2025-01-27",
            "store": "George St Sydney",
            "total": 650,
        },
        {
            "date": "2025-01-28",
            "store": "George St Sydney",
            "total": 650,
        },
        {
            "date": "2025-01-29",
            "store": "George St Sydney",
            "total": 650,
        },
        {
            "date": "2025-01-30",
            "store": "George St Sydney",
            "total": 630,
        },
        {
            "date": "2025-01-31",
            "store": "George St Sydney",
            "total": 660,
        },
        {
            "date": "2025-01-01",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-02",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-03",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-04",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-05",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-06",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-07",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-08",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-09",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-10",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-11",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-12",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-13",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-14",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-15",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-16",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-17",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-18",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-19",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-20",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-21",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-22",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-23",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-24",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-25",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-26",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-27",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-28",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-29",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-30",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-31",
            "store": "Oxford St Sydney",
            "total": 0,
        },
    ]


def test_sales_report_by_fortnight(setup_sales):
    """
    The above report is all very well and good but management want to see sales based on their
    fortnightly business cycles.

    They're also not happy about having Melbourne stores appear in the list before Sydney stores
    are they're headquartered in Sydney xD.

    Redo the query to:
     - group by fortnight assuming their fortnight cycle starts on Wed 1st Jan
     - order the report by location (Sydney, then Melbourne), then by the address
    """
    results = sales_report_by_fortnight()

    assert results == [
        {
            "date": "2025-01-01",
            "store": "George St Sydney",
            "total": 8445,
        },
        {
            "date": "2025-01-15",
            "store": "George St Sydney",
            "total": 8890,
        },
        {
            "date": "2025-01-29",
            "store": "George St Sydney",
            "total": 1940,
        },
        {
            "date": "2025-01-01",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-15",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-29",
            "store": "Oxford St Sydney",
            "total": 0,
        },
        {
            "date": "2025-01-01",
            "store": "Bourke St Melbourne",
            "total": 7565,
        },
        {
            "date": "2025-01-15",
            "store": "Bourke St Melbourne",
            "total": 7910,
        },
        {
            "date": "2025-01-29",
            "store": "Bourke St Melbourne",
            "total": 1880,
        },
        {
            "date": "2025-01-01",
            "store": "Collins St Melbourne",
            "total": 8270,
        },
        {
            "date": "2025-01-15",
            "store": "Collins St Melbourne",
            "total": 8830,
        },
        {
            "date": "2025-01-29",
            "store": "Collins St Melbourne",
            "total": 1930,
        },
    ]


def test_render_sales_report_by_fortnight(client, setup_sales):
    """
    Management are keen to see your Django & HTML prowess… show them how easily you can convert the DB results into a table.

    Hint: There's a template tag specifically for this.
    """

    response = client.get(reverse("fortnight_sales_totals"))

    assert response.status_code == 200
    assertInHTML(
        """\
        <table border="1">
          <thead>
            <tr>
              <th></th>
              <th>2025-01-01</th>
              <th>2025-01-15</th>
              <th>2025-01-29</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>George St Sydney</td>
              <td>$8,445</td>
              <td>$8,890</td>
              <td>$1,940</td>
            </tr>
            <tr>
              <td>Oxford St Sydney</td>
              <td>$0</td>
              <td>$0</td>
              <td>$0</td>
            </tr>
            <tr>
              <td>Bourke St Melbourne</td>
              <td>$7,565</td>
              <td>$7,910</td>
              <td>$1,880</td>
            </tr>
            <tr>
              <td>Collins St Melbourne</td>
              <td>$8,270</td>
              <td>$8,830</td>
              <td>$1,930</td>
            </tr>
          </tbody>
        </table>
        """,
        response.content.decode("utf-8"),
    )


@pytest.fixture
def setup_sporadic_sales():
    coober_pedy = Store.objects.create(city="Coober Pedy", address="Main St")
    fixture = [
        ("2025-01-01", 150),
        ("2025-01-02", 230),
        ("2025-01-03", 180),
        ("2025-01-07", 450),
        ("2025-01-10", 310),
        ("2025-01-11", 290),
        ("2025-01-12", 360),
        ("2025-01-17", 520),
        ("2025-01-22", 470),
        ("2025-01-23", 390),
        ("2025-01-29", 580),
    ]
    Sale.objects.bulk_create(
        Sale(store=coober_pedy, timestamp=timestamp, sale=sale)
        for timestamp, sale in fixture
    )


def test_sporadic_sales_report(setup_sporadic_sales):
    """
    A tourist store in Coober Pedy only sells items when the bus arrives full of tourists.

    Generate a report that shows these periods of sales with the total amount sold like so:

    |--------------------------+-------|
    | Date range               | Total |
    |--------------------------+-------|
    | 2025-01-01 -> 2025-01-03 | 560   |
    | 2025-01-07               | 450   |
    | ...                      |       |
    |--------------------------+-------|

    Hint: This problem is known as "Gaps and Islands"
    """
    results = sporadic_sales_report()

    assert results == [
        {
            "date_range": "2025-01-01 -> 2025-01-03",
            "total": 560,
        },
        {
            "date_range": "2025-01-07",
            "total": 450,
        },
        {
            "date_range": "2025-01-10 -> 2025-01-12",
            "total": 960,
        },
        {
            "date_range": "2025-01-17",
            "total": 520,
        },
        {
            "date_range": "2025-01-22 -> 2025-01-23",
            "total": 860,
        },
        {
            "date_range": "2025-01-29",
            "total": 580,
        },
    ]
