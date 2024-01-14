from django import forms
from .models import Option, Course,Question,QuizResult
import random
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import inlineformset_factory


class QuizForm(forms.Form):
    def __init__(self, course_id, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        course = Course.objects.get(pk=course_id)
        questions = list(course.question_set.filter(is_active=True))
        random.shuffle(questions)
        for question in questions:
            options = Option.objects.filter(question=question)
            choices = [(option.id, option.text_option) for option in options]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text_question,
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'quiz-option'}),
            )

class UpdateUserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UpdatePasswordForm(PasswordChangeForm):
    class Meta:
        model = User

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['yccd', 'knowledge', 'text_question', 'is_active']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text_option', 'is_correct']

OptionFormSet = inlineformset_factory(Question, Option, form=OptionForm, extra=1, can_delete=True)

