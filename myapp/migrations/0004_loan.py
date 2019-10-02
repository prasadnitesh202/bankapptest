# Generated by Django 2.2.5 on 2019-10-02 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20191002_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('loan_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('acc_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Account')),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Branch')),
            ],
        ),
    ]
