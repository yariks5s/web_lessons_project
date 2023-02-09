from pyexpat.errors import messages

from django.contrib.auth import authenticate, login, logout, forms
from django.contrib.auth.forms import UserCreationForm
from django.db.backends.utils import logger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import View, generic
from .models import Course, Lesson, User

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
        context = {}
        # Handles POST request
        if request.method == "POST":
            # Get username and password from request.POST dictionary
            username = request.POST['username']
            password = request.POST['psw']
            # Try to check if provide credential can be authenticated
            user = authenticate(username=username, password=password)
            if user is not None:
                # If user is valid, call login method to login current user
                login(request, user)
                return redirect('courses:index')
            else:
                # If not, return to login page again
                return render(request, 'courses/login.html', context)
        else:
            return render(request, 'courses/login.html', context)

    def logout_request(request):
        logout(request)
        return redirect("courses:index")

    def registration_request(request):
        context = {}
        # If it is a GET request, just render the registration page
        if request.method == 'GET':
            return render(request, 'courses/registration.html', context)
        # If it is a POST request
        elif request.method == 'POST':
            # Get user information from request.POST
            username = request.POST['username']
            password = request.POST['psw']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            user_exist = False
            try:
                # Check if user already exists
                User.objects.get(username=username)
                user_exist = True
            except:
                # If not, simply log this is a new user
                logger.debug("{} is new user".format(username))
            # If it is a new user
            if not user_exist:
                # Create user in auth_user table
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                password=password, email=email)
                user.save()
                # Login the user and redirect to course list page
                login(request, user)
                return redirect("courses:index")
            else:
                return render(request, 'courses/registration.html', context)

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
        return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))

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