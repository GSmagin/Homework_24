# Generated by Django 5.1 on 2024-08-09 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=50, unique=True, verbose_name="Электронная почта"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.CharField(
                blank=True,
                help_text="Укажите телефон",
                max_length=15,
                null=True,
                verbose_name="Телефон",
            ),
        ),
    ]
