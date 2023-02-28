from pyexpat.errors import messages
from .forms import NewLearnerForm
from django.contrib.auth import authenticate, login, logout, forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.backends.utils import logger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import View, generic
from .models import Course, Lesson, User, Learner, Instructor

# Create your views here.
def course_list(request):
    # course = Course.objects.get(pk=1)
    template = "<html>" \
               "<body> The first course we created is %s" \
               "</body>" \
               "</html>"
    return HttpResponse(content=template)

class LoginView(View):

    def login_request(request):
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect("courses:index")
        form = AuthenticationForm()
        return render(request=request, template_name="courses/login.html", context={"login_form": form})

    def logout_request(request):
        logout(request)
        return redirect("courses:index")

    def registration_request(request):
        if request.method == "POST":
            form = NewLearnerForm(request.POST)

            if form.is_valid():
                learner = form.save()
                if learner.is_instructor == 0:
                    learn = Learner.objects.create(username=learner.username, first_name=learner.first_name,
                                                     last_name=learner.last_name, social_link=learner.social_link,
                                                     is_instructor=False)
                else:
                    learn = Instructor.objects.create(username=learner.username, first_name=learner.first_name,
                                                   last_name=learner.last_name, social_link=learner.social_link,
                                                   is_instructor=True)
                login(request, learner)
                return redirect("courses:index")
        form = NewLearnerForm()
        return render(request=request, template_name="courses/registration_learner.html", context={"register_form": form})

class CourseView(View):

    def get(self, request):
        if request.method == 'GET':
            courses = Course.objects.all()
            if courses is None:
                return HttpResponse(status=404, content="Course not found")
            else:
                context = {
                    'course_list': courses
                }
                return render(request, 'courses/index.html', context)
        else:
            return HttpResponse("Request processed")

    def post(self, request):
        pass

class EnrollView(View):

    # Handles post request
    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_id)
        # Increase total enrollment by 1
        course.total_enrollment += 1
        course.save()
        return HttpResponseRedirect(reverse(viewname='courses:course_details', args=(course.id,)))

class CourseDetailsView(View):

    # Handles get request
    def get(self, request, *args, **kwargs):
        context = {}
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        try:
            course = Course.objects.get(pk=course_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            instructors = course.instructors.all()
            context = {'course': course,
                       'course_id': course_id,
                       'lessons': lessons,
                       'instructors': instructors,
                       }
            return render(request, 'courses/coursepage.html', context)
        except Course.DoesNotExist:
            raise Http404("No course matches the given id.")

class LessonView(View):
    # Handles get request
    def get(self, request, *args, **kwargs):
        context = {}
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        lesson_id = kwargs.get('pkl')
        try:
            course = Course.objects.get(pk=course_id)
            lesson = Lesson.objects.get(pk=lesson_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            context = {'course': course,
                       'course_id': course_id,
                       'lesson': lesson,
                       'lessons': lessons,
                       }
            return render(request, 'courses/lessonview.html', context)
        except Course.DoesNotExist:
            raise Http404("No lesson matches the given id.")