import pytest

from reports.models import Employee
from reports.services import series_1_to_10_recursive, show_reporting_chain

pytestmark = pytest.mark.django_db


def test_series_generation_using_a_recursive_query():
    """
    Generate a series of number from 1 -> 10 using a recursive query.

    Hint: Use a CTE!
    """
    assert series_1_to_10_recursive() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.fixture
def employees():
    Employee.objects.bulk_create(
        [
            Employee(name="Alice"),
            Employee(name="Bob", manager_id="Alice"),
            Employee(name="Carol", manager_id="Alice"),
            Employee(name="Dave", manager_id="Bob"),
            Employee(name="Eve", manager_id="Bob"),
            Employee(name="Frank", manager_id="Carol"),
            Employee(name="Grace", manager_id="Frank"),
        ]
    )


def test_reporting_chain(employees):
    """
    Generate a report of the chain of managers for all employees using a recursive query.

    Eg for the employees above it would look like:

      - Alice
      - Bob -> Alice
      - Carol -> Alice
      - Dave -> Bob -> Alice
      - Eve -> Bob -> Alice
      - Grace -> Frank -> Carol -> Alice
    """
    assert show_reporting_chain() == [
        "Alice",
        "Bob -> Alice",
        "Carol -> Alice",
        "Dave -> Bob -> Alice",
        "Eve -> Bob -> Alice",
        "Frank -> Carol -> Alice",
        "Grace -> Frank -> Carol -> Alice",
    ]
