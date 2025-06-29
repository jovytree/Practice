from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1')
    # 1은 ?page=1과 같은 page 파라미터가 없는 url을 위해 기본값을 1로 지정한 것이다

    # 조회
    question_list = Question.objects.order_by('-create_date') # -create_date는 -기호로 작성일시의 역순을 의미한다.

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여달라
    # Pageinator 클래스는 qeustion_list를 페이징 객체 paginator로 변환한다.
    # 두 번째 파라미터인 10은 페이지당 보여줄 게시물 개수를 의미한다.

    page_obj = paginator.get_page(page)
    # page_obj = paginator.get_page(page)로 만들어진
    # page_obj 객체에는 다음과 같은 속성들이 있다. 장고의 Paginatior 클래스를 이용하면 다른 속성들을 사용할 수 있어서 페이징 처리가 쉬워진다.
    # - pageinator.count 전체 게시물 개수
    # - paginator.per_page 페이지당 보여줄 게시물 개수
    # - number 현재 페이지 번호
    # - previous_page_number 이전 페이지 번호
    # - next_page_number 다음 페이지 번호
    # - has_previous 이전 페이지 유무
    # - has_next 다음 페이지 유무
    # - start_index 현재 페이지 시작 인덱스(1부터 시작)
    # - end_index 현재 페이지의 끝 인덱스(1부터 시작)

    context = {'question_list': page_obj} # 조회한 Question 모델 데이터를 context 변수에 저장했다. render 함수가 템플릿을 HTML로 변환하는 과정에서 사용되는 데이터다.
    # render 함수는 context에 있는 Question 모델 데이터 question_list 를 pybo/question_list.html 파일에 적용해 HTML 코드로 변환한다.
    return render(request, 'pybo/question_list.html', context)
    # return HttpResponse("안녕하세요 pybo에 오신 것을 환영합니다.")

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문 등록
    """
    # 질문 목록 화면에서 '질문 등록하기' 버튼을 누르면 get 방식으로 요청돼 질문 등록 화면이 나타나고,
    # 질문 등록 화면에서 입력값을 채우고 '저장하기' 버튼을 누르면 post 방식으로 요청돼 데이터가 저장된다.
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # post 요청으로 받은 form이 유효한지 검사
            question = form.save(commit=False) # commit=Flase 는 임시저장을 한다는 뜻이다.
            # 폼에 현재 subject, content 필드만 있고 create_date 필드는 없으므로 임시저장 후
            # question 객체를 반환받아 create_date 에 값을 설정한 뒤 question.save()로 실제 저장한다.
            question.author = request.user # 추가한 속성 author 적용
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else: # request.method가 GET인 경우 호출
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # 추가한 author 속성 적용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문 수정
    """
    # 로그인 한 사용자(request.user)와 수정하려는 글쓴이(question.author)가 다르면 오류가 발생하도록 작성
    # messages 모듈 이용
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        # messages 모듈은 장고가 제공하는 기능으로, 오류를 임의로 발생시키려는 경우에도 사용된다. 폼 필드와 관련 없으므로 넌필드 오류에 해당됨.
        return redirect('pybo:detail', question_id=question.id)

    # 질문 수정 화면에서 '저장하기'를 누르면 /pybo/question/modify/2/ 페이지가 POST 방식으로 호출돼 데이터 수정이 이뤄진다.
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        # form = ... : question을 기본값으로 해서 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성하라는 의미
        # instance=question : instance 매개변수에 question을 지정하면 기존에 저장돼 있던 제목, 내용 값을 폼에 채울 수 있다.
        if form.is_valid():
            question = form.save(commit=False) # commit=False : 메모리상의 객체만 생성, DB에는 아직 저장 안됨.
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else: # 질문상세 화면에서 '수정'을 누르면 /pybo/question/modify/2/ 페이지가 GET 방식으로 호출돼 질문 수정 화면이 나타난다.
        form = QuestionForm(instance=question) # get 요청으로 기존 값 반영할 때는 request.post 빼고 저렇게만 작성하면 된다.
    context = {'form': form}
    # context : views에서 HTML 템플릿으로 데이터를 전달하는 택배상자 역할
    # 'form' : 템플릿에서 사용할 변수명
    # form : 실제 전달되는 데이터
    return render(request, 'pybo/question_form.html', context)
    # question_form.html 템플릿에 form이라는 이름으로 QuestionForm 객체를 전달한다는 의미