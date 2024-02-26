# Generated by Django 5.0 on 2024-02-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название блога')),
                ('slug', models.CharField(blank=True, max_length=200, null=True, verbose_name='slug')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Содержимое блога')),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Изображение')),
                ('date_created', models.DateField(blank=True, null=True, verbose_name='Дата создания')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликован')),
                ('view_count', models.IntegerField(default=0, verbose_name='Количество просмотров')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блоги',
            },
        ),
    ]
