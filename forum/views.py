
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid credentials")
#     return render(request, 'forum/login.html')

# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('login')

@login_required
def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'forum/home.html', {'questions': questions})

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'forum/post_question.html', {'form': form})

@login_required
def view_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
  
    answers = question.answers.all().order_by('-created_at')

    # Check if the user has liked the answer (if needed)
    for answer in answers:
        #answer.is_liked = answer.likes.filter(user=request.user).exists()
        
        answer.is_liked = answer.user_has_liked(request.user)
       

    #is_liked = answers.user_has_liked(request.user)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('view_question', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'forum/view_question.html', {'question': question, 'answers': answers, 'form': form})

@login_required
def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)
    if not created:
        like.delete()  # Unlike if already liked
    return redirect('view_question', pk=answer.question.pk)