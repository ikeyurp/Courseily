from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from accounts.models import User,Instructor
from random import randrange

class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

class Course(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=200, unique=True, primary_key=True, auto_created=False)
    short_description = models.TextField(blank=False, max_length=60)
    description = models.TextField(blank=False)
    outcome = models.CharField(max_length=200)
    requirements = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    price = models.FloatField(validators=[MinValueValidator(9.99)])
    level = models.CharField(max_length=20)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video_url = models.CharField(max_length=100)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    instructor = models.ForeignKey(Instructor,on_delete=models.CASCADE,default=1)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],default=randrange(1,6))
    rating_count = models.PositiveIntegerField(default=randrange(50,150))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def ytb_preview(self):
        url = self.video_url
        url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
        return url

class Chapter(models.Model):
    chapter_name = models.CharField(max_length=20)
    chapter_created_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return "{}:{}".format(self.chapter_name,self.course)

class TextBlock(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='text_lessons')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return "{}-[{}]".format(self.title,self.chapter)

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    duration = models.FloatField(validators=[MinValueValidator(0.30), MaxValueValidator(60.00)])
    video_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title

    def split_duration(self):
        dur = str(self.duration).split('.')
        if len(dur[1]) == 1:
            dur[1]+='0'
        return "{}:{}".format(dur[0],dur[1])