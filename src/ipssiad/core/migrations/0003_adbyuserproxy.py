# Generated by Django 3.0.5 on 2020-06-11 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200610_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdByUserProxy',
            fields=[
                ('ad_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Ad')),
            ],
            bases=('core.ad',),
        ),
    ]
