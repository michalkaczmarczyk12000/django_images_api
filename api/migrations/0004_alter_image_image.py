# Generated by Django 3.2.22 on 2023-10-11 18:33

import api.utils
import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_expiringlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=api.utils.image_upload_path, validators=[api.validators.validate_img_extension]),
        ),
    ]
