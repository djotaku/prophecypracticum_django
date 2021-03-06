# Generated by Django 3.1.7 on 2021-03-19 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prophecy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prophecy_text', models.TextField()),
                ('feedback_rating', models.PositiveIntegerField()),
                ('feedback_text', models.TextField()),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('prophet', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='my_prophecies', to=settings.AUTH_USER_MODEL)),
                ('supplicant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='received_prophecies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
