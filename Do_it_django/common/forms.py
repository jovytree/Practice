from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# django.contrib.auth.forms 패키지의 UserCreationForm 클래스 상속
# UserCreationForm은 기본적으로 가지고 있는 username, password1, password2 속성에 부가 정보인 email속성을 추가하기 위해
# UserCreationForm을 상속한 UserForm을 만든 것.

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email")
