# Generated by Django 4.1.1 on 2022-09-07 19:01

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='resource_list_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='resources.resourcelist'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='resource_list_three',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='resources.resourcelist'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='resource_list_two',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='resources.resourcelist'),
        ),
        migrations.AddField(
            model_name='featuredcontent',
            name='content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='home.feature'),
        ),
        migrations.AddField(
            model_name='featuredcontent',
            name='page',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='featured_content', to='home.homepage'),
        ),
    ]
