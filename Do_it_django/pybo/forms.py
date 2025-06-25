from django import forms
from pybo.models import Question

# 장고 폼은 2개의 폼으로 구분할 수 있다. froms.Form을 상속 받으면 폼.
# forms.ModelForm을 상속받으면 모델 폼이라 부른다.
# 모델 폼이란? 말 그대로 모델과 연결된 폼으로, 모델 폼 객체를 저장하면 연결된 모델의 데이터를 저장할 수 있다.

class QuestionForm(forms.ModelForm):
    class Meta: # 장고 모델 폼은 내부 클래스로 Meta 클래스를 반드시 가져야 한다.
        model = Question # 폼이 사용할 모델
        fields = ['subject', 'content'] # 필드들을 적어야 한다.