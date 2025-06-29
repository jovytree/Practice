from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # User 모델은 django.contrib.auth 앱이 제공하는 모델이다.
                        # on_delete=models.CASCADE는 계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제하라는 의미다.
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True) # null=True : modify_date 칼럼에 null을 허용하겠다.
                                                # blank=True : form.is_valid()를 통한 입력 폼 데이터 검사 시 값이 없어도 된다.
    # 수정일시는 수정한 경우에만 생성되는 데이터이므로 null=True, blank=Ture를 지정해서 어떤 조건으로던 값을 비워둘 수 있다록 했다.

    def __str__(self):
        return self.subject
    # __str__ 메서드를 추가해서 장고 셸에서 Question.objects.all()을 해서 데이터 조회 시 id가 아닌 제목을 표시하게 한다.

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

