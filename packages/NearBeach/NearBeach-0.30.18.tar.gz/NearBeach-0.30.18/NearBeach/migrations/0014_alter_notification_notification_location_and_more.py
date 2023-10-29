# Generated by Django 4.2.4 on 2023-10-27 09:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("NearBeach", "0013_documentpermission_new_object"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="notification_location",
            field=models.CharField(
                choices=[
                    ("all", "All Options"),
                    ("dashboard", "Dashboard Screen"),
                    ("login", "Login Screen"),
                ],
                default="All",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="objectassignment",
            name="link_relationship",
            field=models.CharField(
                blank=True,
                choices=[
                    ("block", "Block"),
                    ("duplicate", "Duplicate"),
                    ("relate", "Relate"),
                    ("subobject", "Subobject"),
                ],
                default="",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="objectassignment",
            name="meta_object_status",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="objectassignment",
            name="meta_object_title",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="objectassignment",
            name="parent_link",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="requestforchange",
            name="rfc_version_number",
            field=models.CharField(blank=True, default="", max_length=25),
        ),
    ]
