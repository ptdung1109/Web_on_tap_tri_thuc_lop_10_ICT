from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Course,Join, Question, Option, UserAnswer,QuizResult,Knowledge_Level,YCCD, Reference 
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import QuizForm,UpdateUserProfileForm,UpdatePasswordForm
import random
from django.contrib.admin.views.decorators import staff_member_required
from random import shuffle
from django.db.models import F
from django.db.models import Q
from random import sample
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Course, Question, Option
from .forms import QuestionForm, OptionFormSet
# Create your views here.

@staff_member_required(login_url='/error_user/')
def manage_take_quiz(request, course_id):
    if request.user.is_authenticated:
        course = Course.objects.get(pk=course_id)
        questions = Question.objects.filter(course=course).order_by('yccd__id', 'id')
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"
    return render(request, 'app/manage_take_quiz.html', {'course': course, 'questions': questions,'user_not_login':user_not_login,'user_login':user_login})

@staff_member_required(login_url='/error_user/')
def save_question_selection(request, course_id):
    if request.method == 'POST':
        selected_questions = request.POST.getlist('questions')
        course = Course.objects.get(pk=course_id)
        Question.objects.filter(course=course).update(is_active=False)
        Question.objects.filter(id__in=selected_questions).update(is_active=True)
        messages.success(request, 'Selection saved successfully.')
    return redirect('manage_take_quiz', course_id=course_id)

def error(request):
    return render(request, 'app/error.html')

def error_user(request):
    return render(request, 'app/error_user.html')

def intro(request):
    return render(request, 'app/introduce.html')

@login_required(login_url='/error/')  
def search(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            searched = request.POST["searched"]
            keys = Course.objects.filter(name__contains= searched)     
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"

    danh_sach_khoa_hoc = Course.objects.all()
    joined_courses = Join.objects.filter(user=request.user, joined=True).values_list('course__id', flat=True)
    return render(request,'app/search.html',{"searched": searched, "keys": keys,'danh_sach_khoa_hoc': danh_sach_khoa_hoc, 'joined_courses': joined_courses    ,'user_not_login':user_not_login,'user_login':user_login
 })

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context={'form':form}
    return render(request,'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('home_admin')
        else:
            return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('home_admin')
            else:
                return redirect('home')
        else:
            messages.info(request, 'Tài khoản hoặc mật khẩu chưa chính xác!')
    context = {}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        danh_sach_khoa_hoc = Course.objects.all()
        joined_courses = Join.objects.filter(user=request.user, joined=True).values_list('course__id', flat=True)
        context = {'danh_sach_khoa_hoc': danh_sach_khoa_hoc, 'joined_courses': joined_courses}
        user_not_login="hidden"
        user_login="show"
    else:
        danh_sach_khoa_hoc = Course.objects.all()
        user_not_login="show"
        user_login="hidden"
        context = {'danh_sach_khoa_hoc': danh_sach_khoa_hoc}
        return render(request, 'app/home.html',context)
    context = {'danh_sach_khoa_hoc': danh_sach_khoa_hoc, 'joined_courses': joined_courses, 'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/home.html', context)

@login_required(login_url='/error/')  
def dang_ky_khoa_hoc(request, course_id):
    user = request.user
    course = Course.objects.get(id=course_id)
    join, created = Join.objects.get_or_create(user=user, course=course)
    if not join.joined:
        join.joined = True
        join.save()
    return redirect('home')

@login_required(login_url='/error/')  
def xem_chu_de(request, course_id):
    if request.user.is_authenticated:
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(course=course)
    requirements = YCCD.objects.filter(question__in=questions).distinct()
    references = Reference.objects.filter(grade=course.grade)

    context={'course':course,'references':references,'requirements': requirements, 'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/xem_chu_de.html',context)

@login_required(login_url='/error/')  
def user_courses(request):
    if request.user.is_authenticated:
        user_joined_courses = Join.objects.filter(user=request.user)
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"
    context = {'user_joined_courses': user_joined_courses,'user_not_login':user_not_login,'user_login':user_login}
    return render(request, 'app/user_courses.html', context)

def links_reference(request):
    references = Reference.objects.all()
    context = {'references': references,}
    return render(request, 'app/links_reference.html', context)

@login_required(login_url='/error/')  
def quiz_results(request, course_id, user_id):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, id=course_id)
        user = get_object_or_404(User, id=user_id)
        quiz_results = QuizResult.objects.filter(user=user, course=course).order_by('-submit_time')
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"
    context = {
        'course': course,
        'quiz_results': quiz_results,
        'user_not_login':user_not_login,'user_login':user_login,'user':user
    }
    return render(request, 'app/quiz_results.html', context)

@login_required(login_url='/error/')
def quiz_results_detail(request, result_id):
    if request.user.is_authenticated:
        quiz_result = get_object_or_404(QuizResult, id=result_id)
        user_answers = UserAnswer.objects.filter(quiz_result=quiz_result)
        user_not_login = "hidden"
        user_login = "show"
    else:
        user_not_login = "show"
        user_login = "hidden"
    correct_answers_by_requirement = {}
    total_questions = 0
    for user_answer in user_answers:
        requirement_id = user_answer.question.yccd.id
        if requirement_id not in correct_answers_by_requirement:
            correct_answers_by_requirement[requirement_id] = {
                'correct': 0,
                'total': 0,
                'content': user_answer.question.yccd.content,
            }
        if user_answer.is_correct:
            correct_answers_by_requirement[requirement_id]['correct'] += 1
        correct_answers_by_requirement[requirement_id]['total'] += 1
        total_questions += 1
    for stats in correct_answers_by_requirement.values():
        if stats['total'] > 0:
            stats['percentage'] = (stats['correct'] / stats['total']) * 100
        else:
            stats['percentage'] = 0

    context = {
        'quiz_result': quiz_result,
        'user_answers': user_answers,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'correct_answers_by_requirement': correct_answers_by_requirement,
        'total_questions': total_questions,
    }

    return render(request, 'app/quiz_results_detail.html', context)

@login_required(login_url='/error/')
def take_quiz(request, course_id):

    if request.user.is_authenticated:
        user_not_login="hidden"
        user_login="show"
        course = get_object_or_404(Course, id=course_id)

        if request.method == 'POST':
            form = QuizForm(course_id, request.POST)
            if form.is_valid():
                user = request.user

                attempt_number = QuizResult.objects.filter(user=user, course=course).count() + 1

                quiz_result = QuizResult.objects.create(
                    user=user,
                    course=course,
                    attempt_number=attempt_number,
                    total_questions=course.question_set.filter(is_active=True).count(),
                    correct_answers=0,
                    incorrect_answers=0,
                    submit_time=timezone.now(),
                )

                total_questions = 0
                user_answers = []

                for question in course.question_set.filter(is_active=True):
                    total_questions += 1
                    option_id = form.cleaned_data.get(f'question_{question.id}')

                    if option_id is not None:
                        chosen_option = get_object_or_404(Option, id=option_id)
                        is_correct = chosen_option.is_correct
                        
                        difficulty_level = question.knowledge.text_muc_do
                        if is_correct:
                            if difficulty_level == 'Biết':
                                quiz_result.correct_answers += 1
                                quiz_result.score += 5
                            elif difficulty_level == 'Hiểu':
                                quiz_result.correct_answers += 1
                                quiz_result.score += 5
                            elif difficulty_level == 'Vận dụng':
                                quiz_result.correct_answers += 1
                                quiz_result.score += 5
                            elif difficulty_level == 'Vận dụng cao':
                                quiz_result.correct_answers += 1
                                quiz_result.score += 5
                        else:
                            quiz_result.incorrect_answers += 1

                        user_answer = UserAnswer(
                            user=user,
                            course=course,
                            quiz_result=quiz_result,
                            question=question,
                            chosen_option=chosen_option,
                            is_correct=is_correct
                        )
                        user_answers.append(user_answer)

                UserAnswer.objects.bulk_create(user_answers)
                quiz_result.save()
                end_time = timezone.now()
                elapsed_time = end_time - quiz_result.submit_time
                quiz_result.elapsed_time = elapsed_time.total_seconds()
                quiz_result.save()
                return redirect('quiz_results_detail', result_id=quiz_result.id)

        else:
            form = QuizForm(course_id)

        return render(request, 'app/take_quiz.html', {'course': course, 'form': form,'user_not_login':user_not_login,'user_login':user_login})
    else:
        user_not_login="show"
        user_login="hidden"

@login_required(login_url='/error/')
def user_profile(request):
    if request.user.is_authenticated:
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"
    return render(request, 'app/user_profile.html',{'user_not_login':user_not_login,'user_login':user_login})

@login_required(login_url='/error/')
def update_profile(request):
    if request.user.is_authenticated:
        user_not_login="hidden"
        user_login="show"
        if request.method == 'POST':
            form = UpdateUserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thông tin đã được cập nhật!')
                return redirect('user_profile')
        else:
            form = UpdateUserProfileForm(instance=request.user)
    else:
        user_not_login="show"
        user_login="hidden"

    return render(request, 'app/update_profile.html', {'form': form, 'user_not_login':user_not_login,'user_login':user_login})

@login_required(login_url='/error/')
def update_password(request):
    if request.user.is_authenticated:
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"
    if request.method == 'POST':
        form = UpdatePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mật khẩu đã được cập nhật!')
            return redirect('login')
    else:
        form = UpdatePasswordForm(request.user)
    return render(request, 'app/update_password.html', {'form': form,'user_not_login':user_not_login,'user_login':user_login})

@staff_member_required(login_url='/error_user/')
def admin_dashboard(request, course_id):
    if request.user.is_authenticated:
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"
    course_info = Join.objects.filter(course_id=course_id)

    return render(request, 'app/admin_dashboard.html', {'course_info': course_info,'user_not_login':user_not_login,'user_login':user_login})
@staff_member_required(login_url='/error_user/')
def home_admin(request):
    if request.user.is_authenticated:
        user_not_login="hidden"
        user_login="show"
    else:
        user_not_login="show"
        user_login="hidden"
    courses = Course.objects.all()
    return render(request, 'app/home_admin.html', {'courses': courses,'user_not_login':user_not_login,'user_login':user_login})

@method_decorator(staff_member_required(login_url='/error_user/'), name='dispatch')
class ManageQuestionsView(View):
    
    template_name = 'app/manage_questions.html'

    def get(self, request, course_id):
        if request.user.is_authenticated:
            user_not_login="hidden"
            user_login="show"
        else:
            user_not_login="show"
            user_login="hidden"
        course = get_object_or_404(Course, pk=course_id)
        questions = Question.objects.filter(course=course)
        return render(request, self.template_name, {'course': course, 'questions': questions,'user_not_login':user_not_login,'user_login':user_login})

@method_decorator(staff_member_required(login_url='/error_user/'), name='dispatch')
class CreateQuestionView(View):
    template_name = 'app/create_question.html'

    def get(self, request, course_id):
        if request.user.is_authenticated:
            user_not_login="hidden"
            user_login="show"
        else:
            user_not_login="show"
            user_login="hidden"
        form = QuestionForm()
        option_formset = OptionFormSet()
        return render(request, self.template_name, {'form': form, 'option_formset': option_formset,'user_not_login':user_not_login,'user_login':user_login})

    def post(self, request, course_id):
        form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST)
        if form.is_valid() and option_formset.is_valid():
            question = form.save(commit=False)
            question.course = get_object_or_404(Course, pk=course_id)
            question.save()
            option_formset.instance = question
            option_formset.save()
            messages.success(request, 'Câu hỏi đã được thêm!')
            return redirect('manage_questions', course_id=course_id)
        return render(request, self.template_name, {'form': form, 'option_formset': option_formset})

@method_decorator(staff_member_required(login_url='/error_user/'), name='dispatch')
class UpdateQuestionView(View):
    template_name = 'app/update_question.html'

    def get(self, request, course_id, question_id):
        if request.user.is_authenticated:
            user_not_login="hidden"
            user_login="show"
        else:
            user_not_login="show"
            user_login="hidden"
        question = get_object_or_404(Question, pk=question_id)
        form = QuestionForm(instance=question)
        option_formset = OptionFormSet(instance=question)
        return render(request, self.template_name, {'form': form, 'option_formset': option_formset, 'question': question,'user_not_login':user_not_login,'user_login':user_login})

    def post(self, request, course_id, question_id):
        question = get_object_or_404(Question, pk=question_id)
        form = QuestionForm(request.POST, instance=question)
        option_formset = OptionFormSet(request.POST, instance=question)
        if form.is_valid() and option_formset.is_valid():
            form.save()
            option_formset.save()
            messages.success(request, 'Câu hỏi đã được cập nhật!')
            return redirect('manage_questions', course_id=course_id)
        return render(request, self.template_name, {'form': form, 'option_formset': option_formset, 'question': question})


@method_decorator(staff_member_required(login_url='/error_user/'), name='dispatch')
class DeleteQuestionView(View):

    def post(self, request, course_id, question_id):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        messages.success(request, 'Câu hỏi đã được xóa!')
        return redirect('manage_questions', course_id=course_id)
