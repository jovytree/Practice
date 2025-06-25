from django.contrib import admin
from .models import Question

# Register your models here.
# admin의 검색기능을 추가하자
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']

# admin에서 Question 모델 사용할 수 있게 등록 + 검색기능도 추가
admin.site.register(Question, QuestionAdmin)



