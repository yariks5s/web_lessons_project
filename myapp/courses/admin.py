from django.contrib import admin

from .models import Course, Instructor, Lesson, User


# Register your models here.

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class CourseAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_filter = ['pub_date', ]
    list_display = ['pub_date', 'name', ]
    inlines = [LessonInline, ]
    fields = ['pub_date', 'name', 'description', 'image', 'distributor_name', 'instructors', ]


class InstructorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', ]
    list_filter = ['full_time', ]
    list_display = ['first_name', 'last_name', 'full_time', ]
    fields = ['first_name', 'last_name', 'full_time', ]


admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(User)
