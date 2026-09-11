from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson, Question, Choice, Submission, Enrollment
from django.contrib.auth.decorators import login_required

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse/course_list.html', {'courses': courses})

def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_detail_bootstrap.html', {'course': course})

@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    
    if request.method == 'POST':
        selected_choices = []
        # Get all selected choice IDs from the form
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                try:
                    choice_id = int(value)
                    selected_choices.append(choice_id)
                except ValueError:
                    pass
        
        # Create a new submission
        submission = Submission.objects.create(enrollment=enrollment)
        submission.choices.set(selected_choices)
        submission.save()
        
        return redirect(reverse('onlinecourse:show_exam_result', args=[course_id, submission.id]))
    
    return redirect(reverse('onlinecourse:course_details', args=[course_id]))

@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Calculate score
    total_score = 0
    total_questions = course.question_set.count()
    
    selected_choices = submission.choices.all()
    
    # Logic to calculate score based on correct choices
    for question in course.question_set.all():
        correct_choices = question.choice_set.filter(is_correct=True)
        selected_for_question = selected_choices.filter(question=question)
        
        # If all correct choices are selected and no wrong ones
        if set(correct_choices) == set(selected_for_question) and correct_choices.exists():
            total_score += question.grade
            
    context = {
        'course': course,
        'submission': submission,
        'total_score': total_score,
        'total_questions': total_questions,
        'selected_choices': selected_choices,
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
