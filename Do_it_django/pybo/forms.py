from django import forms
from pybo.models import Question, Answer

# 장고 폼은 2개의 폼으로 구분할 수 있다. froms.Form을 상속 받으면 폼.
# forms.ModelForm을 상속받으면 모델 폼이라 부른다.
# 모델 폼이란? 말 그대로 모델과 연결된 폼으로, 모델 폼 객체를 저장하면 연결된 모델의 데이터를 저장할 수 있다.

class QuestionForm(forms.ModelForm):
    class Meta: # 장고 모델 폼은 내부 클래스로 Meta 클래스를 반드시 가져야 한다.
        model = Question # 폼이 사용할 모델
        fields = ['subject', 'content'] # 필드들을 적어야 한다.
        labels = {
            'subject': '제목',
            'content': '내용',
        }
        # {{form.as_p}}는 디자인 측면에서 제한이 생긴다. 수작업으로 폼을 작성해보자
        # widget을 삭제했다.

# 답변 등록 기능에 장고 폼을 적용해보자.
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content' : '답변내용',
        }