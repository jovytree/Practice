from django.db import models

# Create your models here.
class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject # __str__ 메서드를 추가해서 장고 셸에서 Question.objects.all()을 해서 데이터 조회 시 id가 아닌 제목을 표시하게 한다.

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

