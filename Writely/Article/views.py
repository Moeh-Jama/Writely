from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth  import authenticate, login

from . import firebase_operations
# Create your views here.
def index(request):
    context = {
        'basic': 'Hello World',
        'textValues': 'nothing to post',
        'userId': request.user.id,
        'Articles': 'a'
    }

    if request.method == 'POST':
        if request.POST.get('SubmitArticle'):
            textValues = request.POST.get('article_Text')
            username = request.user.username
            title = request.POST.get('Title')
            headerImage =request.POST.get('headerImage')
            firebase_operations.createArticle(username, request.user.id, title, textValues, headerImage)
            # send data to firebase_operations and send that onto user details.
            context['textValues'] = textValues
        elif request.POST.get('sendComment'):
            sendComment(request)



    context['Articles'] = firebase_operations.getArticles()
    return render(request, 'Article/index.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            password
            user = authenticate(username=username, password=password)
            login(request, user)
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def submitArticle(request):
    context = {
        'basic': 'some cancer here please.'
    }
    return render(request, 'Article/submit_article.html', context)

def editProfile(request):
    context = {}
    return render(request, 'Article/edit_profile.html', context)


def readArticle(request):
    context = {}
    print("VALUES LOOKING FOR IS: ", request.GET.get('article_id'))
    article_key = request.GET.get('article_id')
    context = firebase_operations.singleArticleDetails(article_key)
    context['article_id'] =article_key
    return render(request, 'Article/article.html', context)

def sendComment(request):
    #Need article_id
    message = request.POST.get('submitComment')
    if message.strip() != '':
        commenter_id = request.user.id
        sparse = request.GET.get('author')
        author_id = sparse.split('?')[0]
        article_id = sparse.split('?')[1].split('article_id=')[-1]
        author_details = firebase_operations.getUserDetails(author_id)
        firebase_operations.commentOnArticle(author_details,article_id, message, commenter_id)