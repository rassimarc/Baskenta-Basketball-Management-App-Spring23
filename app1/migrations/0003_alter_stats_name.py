# Generated by Django 3.2.18 on 2023-04-24 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_profile_stats_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stats',
            name='name',
            field=models.ForeignKey(blank=True, limit_choices_to={'usertype': 'Player'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players', to='app1.profile'),
        ),
    ]