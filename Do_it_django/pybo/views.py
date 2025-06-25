from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone

# Create your views here.
def index(request):
    """
    pybo 목록 출력
    """
    question_list = Question.objects.order_by('-create_date') # -create_date는 -기호로 작성일시의 역순을 의미한다.
    context = {'question_list': question_list} # 조회한 Question 모델 데이터를 context 변수에 저장했다. render 함수가 템플릿을 HTML로 변환하는 과정에서 사용되는 데이터다.
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

def answer_create(request, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
    # question.answer_set.create : Answer 모델이 Question 모델을 Foreing Key로 참조하고 있어서 쓸 수 있다.
                                # Question 모델을 통해 Answer 모델 데이터를 생성하겠다.
    # content=request.POST.get('content') : request 매개변수에는 detail.html에서 textarea에 입력된 데이터가 파이썬 객체에 담겨 넘어오는데,
                                        # 이 값을 추출하기 위한 코드다. POST 형식으로 전송된 form 데이터 항목 중 name이 content인 값.
    return redirect('pybo:detail', question_id=question_id)
    # 답변 생성 후 상세 화면 호출. redirect 함수 첫 번째 인수에는 이동할 페이지의 별칭을,
    # 두 번째 인수에는 해당 URL에 전달해야 하는 값을 입력한다.

