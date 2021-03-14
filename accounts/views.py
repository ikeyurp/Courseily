from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, RedirectView, ListView, DetailView, UpdateView

from courses.models import Category, Lesson, Course, Chapter, TextBlock
from enroll.models import Enroll
from .models import User
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm

from pprint import pprint

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/form.html'
    success_url = '/login'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):

        user_form = self.form_class(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/form.html', {'form': user_form})


class LoginView(FormView):
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/form.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)


class EnrolledCoursesListView(ListView):
    model = Enroll
    template_name = 'courses/enrolled_courses.html'
    context_object_name = 'enrolls'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('course').filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class StartLessonView(DetailView):
    model = Lesson
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        queryset = queryset.filter(course=course)
        try:
            obj = queryset[:1].get()
            url = obj.video_url
            url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        all_chap = Chapter.objects.filter(course = course)
        lesson_chapters = {}
        textlesson_chapters = {}
        for chap in all_chap:
            chap_lessons = Lesson.objects.filter(chapter = chap)
            chap_text_lessons = TextBlock.objects.filter(chapter = chap)

            lesson_chapters[chap] = chap_lessons
            if chap_text_lessons:
                textlesson_chapters[chap] = chap_text_lessons
        context['textlesson_chapters'] = textlesson_chapters
        context['lesson_chapters'] = lesson_chapters
        return context


class LessonView(DetailView):
    model = Lesson
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'lesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lesson_id = self.kwargs['id']
        queryset = queryset.filter(id=lesson_id)
        try:
            obj = queryset.get()
            url = obj.video_url
            url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/")
            obj.video_url = url
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        all_chap = Chapter.objects.filter(course = course)
        lesson_chapters = {}
        textlesson_chapters = {}
        for chap in all_chap:
            chap_lessons = Lesson.objects.filter(chapter = chap)
            chap_text_lessons = TextBlock.objects.filter(chapter = chap)

            lesson_chapters[chap] = chap_lessons
            if chap_text_lessons:
                textlesson_chapters[chap] = chap_text_lessons
        context['textlesson_chapters'] = textlesson_chapters
        context['lesson_chapters'] = lesson_chapters
        return context

class TextLessonView(DetailView):
    model = TextBlock
    template_name = 'lessons/lessons_by_course.html'
    context_object_name = 'textlesson'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        lesson_id = self.kwargs['id']
        queryset = queryset.filter(id=lesson_id)
        obj = queryset.get()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["lessons"] = self.model.objects.filter(course=course)
        context["course"] = course
        all_chap = Chapter.objects.filter(course = course)
        lesson_chapters = {}
        textlesson_chapters = {}
        for chap in all_chap:
            chap_lessons = Lesson.objects.filter(chapter = chap)
            chap_text_lessons = TextBlock.objects.filter(chapter = chap)

            lesson_chapters[chap] = chap_lessons
            if chap_text_lessons:
                textlesson_chapters[chap] = chap_text_lessons
        context['textlesson_chapters'] = textlesson_chapters
        context['lesson_chapters'] = lesson_chapters
        context['istext'] = True
        return context


class ProfileUpdateView(UpdateView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("accounts:my-profile")

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_initial(self):
        return {"first_name": self.request.user.first_name, "last_name": self.request.user.last_name}

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)