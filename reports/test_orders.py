import pytest

from .models import Order
from .services import (
    get_order_leaderboard,
    get_order_leaderboard_by_store,
    get_order_leaderboard_with_other,
    get_orders_by_priority,
)

pytestmark = pytest.mark.django_db


def test_order_report():
    """
    The client has asked for a report showing all the outstanding orders orders ordered by importance
    so the user can action the orders requiring attention.

    The priority of order status is:
     - IN_PROGRESS
     - PAID
     - SHIPPED
     - DELIVERED

    Produce a queryset that will order the following orders in this way:

    Hint:
      - There a few ways to order by specific values, but Postgres has a nice array function to do this concisely
        (stupid Django tricks? 😅)
    """
    Order.objects.bulk_create(
        [
            Order(product="UltraComfort Memory Foam Mattress", status="DELIVERED"),
            Order(product="ProSeries Wireless Earbuds", status="IN_PROGRESS"),
            Order(product="Sleek Stainless Steel Coffee Maker", status="SHIPPED"),
            Order(product="Eco-Friendly Bamboo Toothbrush Set", status="DELIVERED"),
            Order(product="Smart LED Desk Lamp with USB Charging", status="PAID"),
            Order(product="Luxury Cotton Bath Towel Set", status="PAID"),
            Order(product="Heavy-Duty Cordless Power Drill", status="IN_PROGRESS"),
            Order(product="Premium Leather Crossbody Bag", status="SHIPPED"),
            Order(product="Bluetooth Fitness Tracker Watch", status="DELIVERED"),
            Order(product="Foldable Portable Laptop Stand", status="DELIVERED"),
        ]
    )

    orders = get_orders_by_priority()

    assert list(orders.values("product", "status")) == [
        {"product": "Heavy-Duty Cordless Power Drill", "status": "IN_PROGRESS"},
        {"product": "ProSeries Wireless Earbuds", "status": "IN_PROGRESS"},
        {"product": "Smart LED Desk Lamp with USB Charging", "status": "PAID"},
        {"product": "Luxury Cotton Bath Towel Set", "status": "PAID"},
        {"product": "Premium Leather Crossbody Bag", "status": "SHIPPED"},
        {"product": "Sleek Stainless Steel Coffee Maker", "status": "SHIPPED"},
        {"product": "Foldable Portable Laptop Stand", "status": "DELIVERED"},
        {"product": "Eco-Friendly Bamboo Toothbrush Set", "status": "DELIVERED"},
        {"product": "Bluetooth Fitness Tracker Watch", "status": "DELIVERED"},
        {"product": "UltraComfort Memory Foam Mattress", "status": "DELIVERED"},
    ]


@pytest.fixture
def mega_sales():
    fixture = [
        ("Melbourne", "UltraComfort Memory Foam Mattress", 18),
        ("Sydney", "UltraComfort Memory Foam Mattress", 12),
        ("Melbourne", "ProSeries Wireless Earbuds", 5),
        ("Sydney", "ProSeries Wireless Earbuds", 15),
        ("Melbourne", "Sleek Stainless Steel Coffee Maker", 24),
        ("Sydney", "Sleek Stainless Steel Coffee Maker", 20),
        ("Melbourne", "Eco-Friendly Bamboo Toothbrush Set", 7),
        ("Sydney", "Eco-Friendly Bamboo Toothbrush Set", 13),
        ("Melbourne", "Smart LED Desk Lamp with USB Charging", 19),
        ("Sydney", "Smart LED Desk Lamp with USB Charging", 9),
        ("Melbourne", "Luxury Cotton Bath Towel Set", 4),
        ("Sydney", "Luxury Cotton Bath Towel Set", 7),
        ("Melbourne", "Heavy-Duty Cordless Power Drill", 15),
        ("Sydney", "Heavy-Duty Cordless Power Drill", 10),
        ("Melbourne", "Premium Leather Crossbody Bag", 26),
        ("Sydney", "Premium Leather Crossbody Bag", 16),
        ("Melbourne", "Bluetooth Fitness Tracker Watch", 25),
        ("Sydney", "Bluetooth Fitness Tracker Watch", 22),
        ("Melbourne", "Foldable Portable Laptop Stand", 8),
        ("Sydney", "Foldable Portable Laptop Stand", 2),
    ]
    Order.objects.bulk_create(
        Order(store=store, product=product, status="DELIVERED")
        for store, product, quantity in fixture
        for _ in range(quantity)
    )


def test_order_leaderboard(mega_sales):
    """
    The client would like a leaderboard of the top 5 products sold, with the grand total at the top.

    Using a single SQL query, produce this leaderboard!

    The format should be something like:

        Total Sales: xxx
        Product 1: xxx
        ...
        Product 5: xxx

    Hint: There's a handy SQL GROUP BY feature which allows you to do this with 1 additional line! 😮
          (Django doesn't support this yet, a Stupid Django Trick is in the works to hack this though)
    """
    leaderboard = get_order_leaderboard()

    assert leaderboard == [
        {
            "category": "Total",
            "total": 277,
        },
        {
            "category": "Bluetooth Fitness Tracker Watch",
            "total": 47,
        },
        {
            "category": "Sleek Stainless Steel Coffee Maker",
            "total": 44,
        },
        {
            "category": "Premium Leather Crossbody Bag",
            "total": 42,
        },
        {
            "category": "UltraComfort Memory Foam Mattress",
            "total": 30,
        },
        {
            "category": "Smart LED Desk Lamp with USB Charging",
            "total": 28,
        },
    ]


def test_order_leaderboard_with_other(mega_sales):
    """
    The client was impressed with your leaderboard and has placed a wager that you can also just as easily
    add an "Other section" in the same query.

    The format should now updated as the following:

        Total Sales: xxx
        Product 1: xxx
        ...
        Product 5: xxx
        Other: xxx

    Hints:
     - Build upon the previous query
     - You'll need 2 GROUP BYs
     - row_number() is super handy here! 🤫
    """
    leaderboard = get_order_leaderboard_with_other()

    assert leaderboard == [
        {
            "category": "Total",
            "total": 277,
        },
        {
            "category": "Bluetooth Fitness Tracker Watch",
            "total": 47,
        },
        {
            "category": "Sleek Stainless Steel Coffee Maker",
            "total": 44,
        },
        {
            "category": "Premium Leather Crossbody Bag",
            "total": 42,
        },
        {
            "category": "UltraComfort Memory Foam Mattress",
            "total": 30,
        },
        {
            "category": "Smart LED Desk Lamp with USB Charging",
            "total": 28,
        },
        {
            "category": "Other",
            "total": 86,
        },
    ]


def test_order_leaderboard_by_store(mega_sales):
    """
    EXPERT LEVEL 😅

    The client has 2 stores: One in Melbourne and the other in Sydney.

    They'd like to know which store is performing better; produce a leaderboard that shows:
     - Grand total
     - Subtotals per store
     - Top 3 items sold at each store
     - The winning store is listed first

    The format should be something like:

      Total Sales: xxx
      Melbourne: xxx
      Product 1: xxx
      Product 2: xxx
      Product 3: xxx
      Sydney: xxx
      Product 1: xxx
      Product 2: xxx
      Product 3: xxx

    Hints:
      - This uses the same SQL feature for the previous leaderboards!
      - The secret sauce:
        - Use a window function to partition by store and order by that store's total sales
    """
    leaderboard = get_order_leaderboard_by_store()

    assert leaderboard == [
        {
            "category": "Total",
            "total": 277,
        },
        {
            "category": "Melbourne Total",
            "total": 151,
        },
        {
            "category": "Premium Leather Crossbody Bag",
            "total": 26,
        },
        {
            "category": "Bluetooth Fitness Tracker Watch",
            "total": 25,
        },
        {
            "category": "Luxury Cotton Bath Towel Set",
            "total": 4,
        },
        {
            "category": "Sydney Total",
            "total": 126,
        },
        {
            "category": "Bluetooth Fitness Tracker Watch",
            "total": 22,
        },
        {
            "category": "Sleek Stainless Steel Coffee Maker",
            "total": 20,
        },
        {
            "category": "Foldable Portable Laptop Stand",
            "total": 2,
        },
    ]
