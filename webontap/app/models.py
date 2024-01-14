from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

# Create your models here.
#change form register django
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

    
class Grade_Level(models.Model):
    content = models.CharField(max_length=200, null=True)
    def __str__(self):
            return self.content
    
class Grade(models.Model):
    content_grade = models.IntegerField()
    grade_level = models.ForeignKey(Grade_Level,on_delete= models.SET_NULL, blank=True, null= True)
    def __str__(self):
        return f"Khối lớp {self.content_grade}"

class Content_YCCD(models.Model):
    content = models.CharField(max_length=2000, null=True)
    def __str__(self):
        return self.content
    
class YCCD(models.Model):
    content_yccd = models.ForeignKey(Content_YCCD,on_delete= models.SET_NULL, blank=True, null= True)
    content = models.CharField(max_length=2000, null=True)
    def __str__(self):
        return self.content
    
class Knowledge_Level(models.Model):
    text_muc_do = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.text_muc_do
    
class Course(models.Model):
    grade = models.ForeignKey(Grade,on_delete= models.SET_NULL, blank=True, null= True)
    name = models.CharField(max_length=200, null=True)
    date_create = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(null=True, blank=True)
    def __str__(self):
        return f"{self.name} - Lớp {self.grade.content_grade}"
    @property
    def ImageURL(self):
        try:
            url = self.avatar.url
        except:
            url = ""
        return url
    
class Join(models.Model):
    user = models.ForeignKey(User,on_delete= models.SET_NULL, blank=True, null= True)
    course = models.ForeignKey(Course,on_delete= models.SET_NULL, blank=True, null= True)
    date = models.DateTimeField(auto_now_add=True)
    joined = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user} - {self.course}"
    


class Question(models.Model):
    course = models.ForeignKey(Course,on_delete= models.SET_NULL, blank=True, null= True)
    yccd = models.ForeignKey(YCCD,on_delete= models.SET_NULL, blank=True, null= True)
    knowledge = models.ForeignKey(Knowledge_Level,on_delete= models.SET_NULL, blank=True, null= True)
    text_question = models.CharField(max_length=5000, null=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.course} - Question {self.text_question}"
    
class Option(models.Model):
    question = models.ForeignKey(Question,on_delete= models.SET_NULL, blank=True, null= True)
    text_option = models.CharField(max_length=5000, null=True)
    is_correct = models.BooleanField(default= False)
    def __str__(self):
        return f"{self.question} - Option {self.pk}"
    

class Reference(models.Model):
    grade= models.ForeignKey(Grade,on_delete= models.SET_NULL, blank=True, null= True)
    name =models.CharField(max_length=200, null=True)
    link= models.CharField(max_length=2000, null=True)
    type = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name
    

    
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attempt_number = models.IntegerField()  
    total_questions = models.IntegerField() 
    correct_answers = models.IntegerField()  
    incorrect_answers = models.IntegerField()  
    submit_time = models.DateTimeField()  
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Attempt {self.attempt_number} - Course: {self.course.name}"
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE) 
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_option = models.ForeignKey(Option, on_delete=models.CASCADE) 
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - Attempt {self.quiz_result.attempt_number} - Question: {self.question.text_question}"
    

