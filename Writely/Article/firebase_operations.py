import pyrebase
import datetime
from django.contrib.auth.models import User
def initialise_firebase():
    config = {
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db

def getMostPopularArticles():
    pass

def createArticle(author, authorId, title, text, headerImage):
    #create datetime info
    db = initialise_firebase()
    current_time = datetime.datetime.now()
    newArticle = {
        'Author': author,
        'Author_id': authorId,
        'Date': str(current_time),
        'Header_image': headerImage,
        'Text': text,
        'Title': title
    }
    #at the end return an article id
    db.child('Articles').push(newArticle)

def getArticles():
    db = initialise_firebase()
    keys = []

    for i in  db.child('Articles').get().val():
        #print(db.child('Articles').child(i).get().val())
        article = db.child('Articles').child(i).get().val()
        post = {}
        post[i] = {}
        for articleDetails in article:
            #print(db.child('Articles').child(i).child(articleDetails).get().val())
            print(articleDetails)
            if articleDetails == 'Text':
                text = db.child('Articles').child(i).child(articleDetails).get().val()
                if len(text) > 55:
                    post[i][articleDetails] = text[:55]+"..."
                else:
                    post[i][articleDetails] = text
            else:
                post[i][articleDetails] = db.child('Articles').child(i).child(articleDetails).get().val()
        keys.append(post)
    keys.reverse()
    return keys

def singleArticleDetails(article_id):
    db  = initialise_firebase()
    context = {
        'Article': 'article in json format',
        'Comments': 'No Comments Yet!'
    }
    comments = {}
    article = db.child('Articles').child(str(article_id)).get().val()
    info = {}
    for article_details in  article:
        info[article_details] = db.child('Articles').child(str(article_id)).child(article_details).get().val()

    info['id'] = str(article_id)
    context['Article'] = info

    #Get comments, if exists
    found = False
    for comment in db.child('Comments').get().val():
        print(comment)
        if comment == info['Author']+"_"+article_id:
            found = True
            posted_comment = {}
            for i in db.child('Comments').child(comment).get().val():
                print(i)
                posted_comment[i] = db.child('Comments').child(comment).child(i).get().val()
            comments = posted_comment


    if not found:
        current_time = datetime.datetime.now()
        db.child('Comments').child(info['Author']+"_"+article_id).push({'User': 'MoehJama', 'Date':str(current_time), 'Comment': 'Leave a Message!'})
    context['Comments'] = comments
    print('SENDING OUT BELOW')
    print(context)
    return context

def getUserDetails(user_id):
    print('USER ID IS: ', user_id)
    db = initialise_firebase()
    context = {}
    user_found = False
    for user in db.child('Users').get().val():
        if str(user) == str(user_id):
            user_found = True
            context['User'] = {}
            context['User']['id'] = user_id
            for user_info in db.child('Users').child(user).get().val():
                context['User'][user_info] = db.child('Users').child(user).child(user_info).get().val()
    if not user_found:
        #Make user
        print('develop user')
        data = {}
        username = ''
        users = User.objects.all()
        for user in users:
            if str(user.id) == str(user_id):
                username = str(user.username)
        print('New username is: ', username)
        data[user_id] = {}
        data[user_id] = {
            'Age': 18,
            'Sex': 'Female',
            'listOfArticles': [],
            'profile_image': 'https://themainstage.com/assets/cdn/users/profileImgs/default.png',
            'userName':username
        }
        db.child('Users').child(user_id).set(data[user_id])
        context['User'] = {}
        context['User'] = data[user_id]
        context['User']['id'] = user_id
    return context


def commentOnArticle(user_details, article_id, comment_message, currentCommenterID):
    db = initialise_firebase()
    #user_details is a dictionary
    articleDict = {}
    for article in  db.child('Articles').get().val():
        if str(article) == str(article_id):
            for article_details in db.child('Articles').child(article).get().val():
                articleDict[article_details] = db.child('Articles').child(article).child(article_details).get().val()


    commenters_name = ''
    users = User.objects.all()
    for user in users:
        if str(user.id) == str(currentCommenterID):
            commenters_name = str(user.username)

    current_time = datetime.datetime.now()
    print('USERDETAILS:', user_details)
    #create comment
    for comments in db.child('Comments').get().val():
        if comments == str(user_details['User']['userName']+"_"+article_id):
            db.child('Comments').child(comments).push({'User': commenters_name,'Date': str(current_time), 'Comment': comment_message})


