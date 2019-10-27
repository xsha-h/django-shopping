# Generated by Django 2.2.6 on 2019-10-10 03:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='收货人姓名')),
                ('tel', models.CharField(max_length=20, verbose_name='联系方式')),
                ('addr', models.CharField(max_length=255, verbose_name='详细地址')),
                ('postal', models.IntegerField(verbose_name='邮政编码')),
                ('is_default', models.BooleanField(default=False, verbose_name='默认地址')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '收获地址',
            },
        ),
    ]
