from django.urls import path
from . import views

# 다른 앱이 프로젝트에 추가됐을 때, 같은 URL 별칭이 사용되는 걸 막기 위해 네임 스페이스를 저장한다.

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
]