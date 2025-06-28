from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name= 'common/login.html' # common 디렉터리에 템플릿을 생성했다. regitration에서 common으로 변경한 것.
    ), name='login'),
    # django.contrib.auth 앱의 LoginView 클래스를 사용했으므로 별도의 views.py 파일 수정이 필요하지 않다.
    # LoginView 클래스는 registration이라는 템플릿 디렉터리에서 login.html 파일을 찾는다.
    # 하지만 우리는 로그인을 common 앱에 구현할 것이므로, registration 디렉터리에 템플릿 파일을 생성하기 보다는,
    # common 디렉터리에 템플릿을 생성하는 것이 좋다.
]