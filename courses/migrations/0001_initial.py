# Generated by Django 2.2 on 2020-06-07 23:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_name', models.CharField(max_length=20)),
                ('chapter_created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, primary_key=True, serialize=False, unique=True)),
                ('short_description', models.TextField(max_length=60)),
                ('description', models.TextField()),
                ('outcome', models.CharField(max_length=200)),
                ('requirements', models.CharField(max_length=200)),
                ('language', models.CharField(max_length=200)),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(9.99)])),
                ('level', models.CharField(max_length=20)),
                ('thumbnail', models.ImageField(upload_to='thumbnails/')),
                ('video_url', models.CharField(max_length=100)),
                ('is_published', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('rating', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('rating_count', models.PositiveIntegerField(default=52)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.Category')),
                ('instructor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.Instructor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TextBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Chapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_lessons', to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('duration', models.FloatField(validators=[django.core.validators.MinValueValidator(0.3), django.core.validators.MaxValueValidator(60.0)])),
                ('video_url', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('chapter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.Chapter')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.Course')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
    ]