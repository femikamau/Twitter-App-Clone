# Generated by Django 4.2.3 on 2023-07-06 23:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0003_remove_like_post_remove_like_user_alter_comment_post_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="images",
            new_name="image",
        ),
    ]