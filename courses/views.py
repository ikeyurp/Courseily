from django.http import Http404
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from cart.cart import Cart
from courses.models import Course, Category, Chapter, Lesson,TextBlock
from enroll.models import Enroll
import datetime

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/details.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object(self.get_queryset())
        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, user_id=self.request.user.id).exists():
                context['is_enrolled'] = True
            else:
                cart = Cart(self.request)
                context['is_in_cart'] = cart.has_course(course)
        else:
            cart = Cart(self.request)
            context['is_in_cart'] = cart.has_course(course)
        all_courses = Course.objects.all()
        instructor_courses = 0
        for i in all_courses:
            if i.instructor == course.instructor:
                instructor_courses += 1
        context['instructor_courses'] = instructor_courses
        tot_enrolled = Enroll.objects.all()
        instructor_enrolled = 0
        for i in tot_enrolled:
            if i.course.instructor == course.instructor:
                instructor_enrolled += 1
        context['instructor_enrolled'] = instructor_enrolled

        all_chap = Chapter.objects.filter(course = course)
        lesson_chapters = {}
        for chap in all_chap:
            chap_lessons = Lesson.objects.filter(chapter = chap)
            chap_text_lessons = TextBlock.objects.filter(chapter = chap)
            duration = 0
            minutes = 0
            seconds = 0
            for les in chap_lessons:
                m,s = str(les.duration).split('.')
                minutes += int(m)
                seconds += int(s)
            total_seconds = minutes*60 + seconds
            total_time = str(datetime.timedelta(seconds=total_seconds))
            if total_time.split(':')[0] == '0':
                total_time = ':'.join(total_time.split(':')[1:])
            if chap_text_lessons:
                lesson_chapters[chap] = [chap_lessons,total_time,chap_text_lessons]
            else:
                lesson_chapters[chap] = [chap_lessons,total_time]
        context['lesson_chapters'] = lesson_chapters
        return context

class CoursesByCategoryListView(ListView):
    model = Course
    template_name = 'courses/courses_by_category.html'
    context_object_name = 'courses'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category_id=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context