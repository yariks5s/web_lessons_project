from pyexpat.errors import messages
from .forms import NewLearnerForm
from django.contrib.auth import authenticate, login, logout, forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.backends.utils import logger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import View, generic
from .models import Course, Lesson, User, Learner, Instructor, LessonsLearnerRelations, CoursesLearnerRelations, Enrollment, QuestModel
from django.contrib.auth.decorators import login_required

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

    # @login_required
    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('pkc')
        user_id = request.user.id
        # We get URL parameter pk from keyword argument list as course_id
        try:
            temp_course = Course.objects.get(pk=course_id)
            temp_user = Learner.objects.get(pk=user_id-5)
            new_enrollment = Enrollment()
            new_enrollment.course = temp_course
            new_enrollment.learner = temp_user

            new_enrollment.save()
            return redirect("courses:course_details", course_id)
        except:
            raise InterruptedError("There is an unexpected error. Please, try again.")

class CourseDetailsView(View):

    # Handles get request
    def get(self, request, *args, **kwargs):
        context = {}
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        user_id = request.user.id - 5
        try:
            course = Course.objects.get(pk=course_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            instructors = course.instructors.all()
            users = User.objects.get(pk=user_id)
            exists = Enrollment.objects.filter(course_id=course_id, learner_id=user_id)
            context = {'course': course,
                       'course_id': course_id,
                       'lessons': lessons,
                       'instructors': instructors,
                       'users': users,
                       'exists': exists,
                       }
            return render(request, 'courses/coursepage.html', context)
        except Course.DoesNotExist:
            raise Http404("No course matches the given id.")

class CourseProgressView(View):

    # Handles get request
    def get(self, request, *args, **kwargs):
        context = {}
        done_lessons = []
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        user_id = request.user.id - 5
        try:
            course = Course.objects.get(pk=course_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            for i in range(len(lessons)):
                if LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=user_id).exists():
                    done_lessons.append(LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=request.user.id-5))
                    print(done_lessons)
            instructors = course.instructors.all()
            users = User.objects.get(pk=user_id)
            exists = Enrollment.objects.filter(course_id=course_id, learner_id=user_id)
            num_of_lessons = len(lessons)
            num_of_done_lessons = len(done_lessons)
            percent_of_done_lessons = (num_of_done_lessons / num_of_lessons * 100).__round__(1)
            context = {'course': course,
                       'course_id': course_id,
                       'lessons': lessons,
                       'done_lessons': done_lessons,
                       'instructors': instructors,
                       'users': users,
                       'exists': exists,
                       'num_of_lessons': num_of_lessons,
                       'num_of_done_lessons': num_of_done_lessons,
                       'percent_of_done_lessons': percent_of_done_lessons,
                       }
            return render(request, 'courses/courseprogress.html', context)
        except Course.DoesNotExist:
            raise Http404("No course matches the given id.")

class LessonView(View):
    # Handles get request
    def get(self, request, *args, **kwargs):
        done_lessons = []
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        lesson_id = kwargs.get('pkl')
        # print(request.POST['option'])
        try:
            user_id = request.user.id - 5
            learner = Learner.objects.get(id=request.user.id - 5)
            course = Course.objects.get(pk=course_id)
            lesson = Lesson.objects.get(pk=lesson_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            quiz = QuestModel.objects.get(pk=lesson.questions_id)
            is_done = LessonsLearnerRelations.objects.filter(learner=learner, lesson=lesson).exists()
            num_of_lessons = len(lessons)
            for i in range(len(lessons)):
                if LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=user_id).exists():
                    done_lessons.append(LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=request.user.id-5))
                    print(done_lessons)
            num_of_done_lessons = len(done_lessons)
            percent_of_done_lessons = (num_of_done_lessons / num_of_lessons * 100).__round__(1)
            print(percent_of_done_lessons)
            if percent_of_done_lessons == 100.0 and not CoursesLearnerRelations.objects.filter(course_id=course_id, learner_id=user_id).exists():
                rel = CoursesLearnerRelations.objects.create(learner=learner, course=course)
            context = {'course': course,
                       'course_id': course_id,
                       'lesson': lesson,
                       'lessons': lessons,
                       'quiz': quiz,
                       'is_done': is_done,
                       }
            return render(request, 'courses/lessonview.html', context)
        except Course.DoesNotExist:
            raise Http404("No lesson matches the given id.")

    def post(self, request, *args, **kwargs):
        done_lessons = []
        is_done = False
        # We get URL parameter pk from keyword argument list as course_id
        course_id = kwargs.get('pk')
        lesson_id = kwargs.get('pkl')
        print(request.POST['option'])
        try:
            user_id = request.user.id - 5
            learner = Learner.objects.get(id=request.user.id - 5)
            course = Course.objects.get(pk=course_id)
            lesson = Lesson.objects.get(pk=lesson_id)
            lessons = Lesson.objects.filter(course_id=course_id)
            num_of_lessons = len(lessons)

            for i in range(len(lessons)):
                if LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=user_id).exists():
                    done_lessons.append(LessonsLearnerRelations.objects.filter(lesson_id=lessons[i].id, learner_id=request.user.id-5))
                    print(done_lessons)
            num_of_done_lessons = len(done_lessons)
            percent_of_done_lessons = (num_of_done_lessons / num_of_lessons * 100).__round__(1)
            if percent_of_done_lessons == 100.0 and not CoursesLearnerRelations.objects.filter(course_id=course_id, learner_id=user_id).exists():
                rel = CoursesLearnerRelations.objects.create(learner=learner, course=course)
            quiz = QuestModel.objects.get(pk=lesson.questions_id)
            if request.POST['option'].lower() == quiz.answer.lower():
                percentage = 1
            else:
                percentage = 0
            is_done = LessonsLearnerRelations.objects.create(learner=learner, lesson=lesson, percentage=percentage)
            is_done = True
            context = {'course': course,
                       'course_id': course_id,
                       'lesson': lesson,
                       'lessons': lessons,
                       'quiz': quiz,
                       'is_done': is_done,
                       'percent_of_done_lessons': percent_of_done_lessons,
                       }
            return render(request, 'courses/lessonview.html', context)
        except Course.DoesNotExist:
            raise Http404("No lesson matches the given id.")
