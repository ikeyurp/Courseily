from django.contrib import admin
from .models import Category, Course, Lesson,Chapter,TextBlock
from django_summernote.admin import SummernoteModelAdmin

class CourseAdmin(admin.ModelAdmin):
    exclude = ('slug',)

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)

class TextBlockAdmin(SummernoteModelAdmin): 
    summernote_fields = '__all__'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Chapter)
admin.site.register(TextBlock, TextBlockAdmin)