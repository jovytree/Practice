from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm

# Create your views here.
def signup(request):
    """
    회원가입
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid(): # UserCreationForm의 is_valid 함수는 회원가입 화면의 필드값 3개가 모두 입력됐는지,
        # 비밀번호1과 비밀번호2가 같은지, 비밀번호의 값이 비밀번호 생성 규칙에 맞는지 등을 검사한다.
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

# signup 함수는 POST 요청인 경우 화면에서 입력한 데이터로 새로운 사용자를 생성하고,
# GET 요청인 경우 common/signup.html 화면을 반환한다.

# form.cleaned_data.get은 회원가입 화면에서 입력한 값을 안전하게 가져오기 위해 사용하는 메서드다.
# form.cleaned_data - Django 폼에서 유효성 검사를 통과한 데이터들을 담고 있는 딕셔너리
# .get() - 파이썬 딕셔너리의 기본 메서드 (안전하게 값을 가져오는 방법)

# 그리고 회원가입이 완료된 이후 자동으로 로그인되도록 authenticate 함수와 login 함수를 사용했다.

### login(request, user) 함수가 하는 일 // django.contrib.auth에서 제공하는 login 함수를 import해서 사용
# 1. 세션에 사용자 정보 저장 - 브라우저의 세션에 로그인된 사용자 정보를 기록
# 2. 쿠키 설정 - 브라우저에 세션 ID를 담은 쿠키를 설정
# 3. request.user 업데이트 - 이후 요청에서 request.user로 현재 로그인된 사용자에 접근 가능
# Django가 이런 복잡한 로그인 처리를 모두 내부적으로 해주기 때문에, 우리는 단순히 login(request, user)만 호출하면 된다.