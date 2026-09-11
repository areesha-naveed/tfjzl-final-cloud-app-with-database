from django.contrib import admin
from .models import Instructor, Learner, Course, Lesson, Enrollment, Question, Choice, Submission

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('content', 'course', 'grade')

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'pub_date')

admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
