# Generated by Django 5.1.4 on 2025-03-27 07:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_quiztopic_delete_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiztopic',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.quizcategory'),
        ),
        migrations.AlterField(
            model_name='quizsubtopic',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.quiztopic'),
        ),
    ]
