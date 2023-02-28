import datetime
from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.auth.models import AbstractBaseUser, UserManager
import django
from django.db import models

# Create your models here.

# User model
class User(models.Model):
    username = models.CharField(null=False, max_length=30, default='noname')
    first_name = models.CharField(null=False, max_length=30, default='john')
    last_name = models.CharField(null=False, max_length=30, default='doe')
    social_link = models.URLField(default="", max_length=200)
    dob = models.DateField(null=True)
    is_instructor = models.BooleanField(default=False)
    objects = UserManager()


    # Create a toString method for object string representation
    def __str__(self):
        return self.first_name + " " + self.last_name

# Instructor model
class Instructor(User):
    full_time = models.BooleanField(default=True)

    # Create a toString method for object string representation
    def __str__(self):
        return "First name: " + self.first_name + ", " + \
               "Last name: " + self.last_name + ", " + \
               "Is full time: " + str(self.full_time) + ", "

# Learner model
class Learner(User):
    # Create a toString method for object string representation
    def __str__(self):
        return "First name: " + self.first_name + ", " + \
               "Last name: " + self.last_name + ", " \
                                                "Date of Birth: " + str(self.dob) + ", " + \
               "Social Link: " + self.social_link

# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=100, default='online course', )
    description = models.CharField(max_length=500, )
    distributor_name = models.CharField(null=False, max_length=100, default='Unknown', )
    image = ThumbnailerImageField(upload_to='Courses', blank=True, )
    pub_date = models.DateField(default=django.utils.timezone.now, )
    # Many-To-Many relationship with Instructors
    instructors = models.ManyToManyField(Instructor)
    # Many-To-Many relationship with Learner via Enrollment relationship
    learners = models.ManyToManyField(Learner, through='Enrollment', )

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# Enrollment model as a lookup table with additional enrollment info
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
    ]
    # Add a learner foreign key
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    # Add a course foreign key
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # Enrollment date
    date_enrolled = models.DateField(default=django.utils.timezone.now)
    # Enrollment mode
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)


# Lesson
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="Lesson title")
    course = models.ForeignKey(Course, null=True, on_delete=models.CASCADE)
    content = models.TextField()