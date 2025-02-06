import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("store", models.CharField()),
                ("product", models.CharField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("IN_PROGRESS", "In Progress"),
                            ("PAID", "Paid"),
                            ("SHIPPED", "Shipped"),
                            ("DELIVERED", "Delivered"),
                        ]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Store",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField()),
                ("address", models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("name", models.CharField(primary_key=True, serialize=False)),
                (
                    "manager",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reports.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Sale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                ("sale", models.IntegerField()),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="reports.store"
                    ),
                ),
            ],
        ),
    ]
