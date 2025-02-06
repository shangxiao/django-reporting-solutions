# django-reporting
Reporting exercises with Django &amp; SQL (PostgreSQL)


### Setup

```
pip install -r requirements.txt
```

and then run tests with:

```
pytest --reuse-db <path/to/test.py>
```

alternatively watch tests with:

```
ptw -c -- --reuse-db <path/to/test.py>
```


### Exercises

There are 3 test suites to run:

 1. `reports/test_orders.py` covering:
   - ordering by specific values
   - extended group by features
   - nested queries
   - `row_number()`
 2. `reports/test_sales.py` covering:
   - sequence generation
   - Django template tags to generate the UI
   - Gaps & Islands problem
 3. `reports/test_employees.py` covering:
   - recursive queries

Each test in a suite is an exercise and will build upon previous exercises.
Make each test pass one-by-one and then move onto the next.

The tests call stubbed services in `reports/services.py` and one view with a stubbed template.

The answers with correct implementation will be provided at the end of the session so we can compare solutions.


### Objectives

The exercises are geared towards demonstrating often overlooked database/SQL oriented solutions to common data
aggregation problems used in real life. The goal here is to show how SQL can be a viable alternative and provide a
possibly simpler solution to aggregating in Python.

Some of these solutions are not yet possible in the Django ORM and require raw SQL... the objective is not to say raw
SQL is superior, just a possible alternative that you may wish to use in projects moving forward.


### Testing in the shell/browser

`django-extensions` is included, feel free to open `shell_plus` and copy & paste test fixtures into the shell to fiddle
around with a queryset or user `psql` to fiddle with raw SQL.


### Useful Reminder

Use the following graphic to remind you the order in which queries are processed (author Julia Evans, ref:
https://jvns.ca/blog/2019/10/03/sql-queries-don-t-start-with-select/)

![SQL query order](https://jvns.ca/images/sql-queries.jpeg "SQL query order")
