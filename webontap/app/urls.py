from django.contrib import admin
from django.urls import path
from . import views
from.views import *

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('error/', views.error, name="error"),
    path('intro/', views.intro, name="intro"),
    path('error_user/', views.error_user, name="error_user"),
    path('logout/', views.logoutPage, name="logout"),
    path('search/', views.search, name="search"),
    path('links_reference/', views.links_reference, name="links_reference"),
    path('dang_ky_khoa_hoc/<int:course_id>', views.dang_ky_khoa_hoc, name="dang_ky_khoa_hoc"),
    path('xem_chu_de/<int:course_id>/', views.xem_chu_de, name="xem_chu_de"),
    path('take_quiz/<int:course_id>/', views.take_quiz, name='take_quiz'),    
    path('quiz/results/<int:course_id>/<int:user_id>/', views.quiz_results, name='quiz_results'),
    path('quiz/results/detail/<int:result_id>/', views.quiz_results_detail, name='quiz_results_detail'),
    path('user_courses/', views.user_courses, name='user_courses'),
    path('manage_take_quiz/<int:course_id>/', views.manage_take_quiz, name='manage_take_quiz'),
    path('save_question_selection/<int:course_id>/', views.save_question_selection, name='save_question_selection'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-password/', views.update_password, name='update_password'),
    path('admin_dashboard/<int:course_id>/', views.admin_dashboard, name='admin_dashboard'),
    path('home_admin/', views.home_admin, name='home_admin'),
    path('manage_questions/<int:course_id>/', views.ManageQuestionsView.as_view(), name='manage_questions'),
    path('create_question/<int:course_id>/', views.CreateQuestionView.as_view(), name='create_question'),
    path('update_question/<int:course_id>/<int:question_id>/', views.UpdateQuestionView.as_view(), name='update_question'),
    path('delete-question/<int:course_id>/<int:question_id>/', views.DeleteQuestionView.as_view(), name='delete_question'),



]