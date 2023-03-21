from django.urls import path
from . import views


app_name = 'courses'
urlpatterns = [
    path(route='', view=views.CourseView.as_view(), name='index'),
    path(route='courseid:<int:pkc>/enroll/', view=views.EnrollView.as_view(), name='enroll'),
    path(route='courseid:<int:pk>/', view=views.CourseDetailsView.as_view(), name='course_details'),
    path(route='courseid:<int:pk>/progress', view=views.CourseProgressView.as_view(), name='course_progress'),
    path(route='courseid:<int:pk>/lessonid:<int:pkl>/', view=views.LessonView.as_view(), name='lesson_view'),
    path('login/', view=views.LoginView.login_request, name='login'),
    path('logout/', view=views.LoginView.logout_request, name='logout'),
    path('registration/', views.LoginView.registration_request, name='registration'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('import/', views.import_excel, name='import_excel'),
    path('export/', views.export_excel, name='export_excel'),
]
