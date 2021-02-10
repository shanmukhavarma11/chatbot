from django.shortcuts import render
from .forms import Login
from .models import Today
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from background_task import background
from django.contrib.auth.models import User
from fbchat.models import*
from fbchat import Client
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
from py_telegram_bot.bot import Bot
bot = Bot('906446637:AAEQlAk734515XrhK4todEV0W8x1MNLYTeg')
api = bot.get_api()
a=Today.objects.all()
question1=[]
for i in a:
    question1.append(i.question)
corpus=''

for i in question1:
    corpus=corpus+' '+i
text = corpus
sent_tokens = nltk.sent_tokenize(text)
remove = dict(  ( ord(punct),None) for punct in string.punctuation)
def Lem(text):
  return nltk.word_tokenize(text.lower().translate(remove))
GREETING_IN = ["hi", "hello", "hola", "greetings", "wassup", "hey","hai","hii"]
GREETING=["howdy", "hi", "hey", "what's good", "hello", "hey there"]
greet=["how are you","how do you do","are you fine"]
greetout=["i am fine ","feeling better then you"]
def greeting(sentence):
    for word in sentence.split(' '):
        if word.lower() in GREETING_IN:
            return random.choice(GREETING)
def next1(sentence):
    if sentence in greet:
        return random.choice(greetout)
def response(user_response):
  user_response = user_response.lower() 
  robo_response = ''
  sent_tokens.append(user_response)
  TfidfVec = TfidfVectorizer(tokenizer = Lem, stop_words='english')
  tfidf = TfidfVec.fit_transform(sent_tokens)
  vals = cosine_similarity(tfidf[-1], tfidf)
  idx = vals.argsort()[0][-2]
  flat = vals.flatten()
  flat.sort()
  score = flat[-2]
  if(score == 0):
    robo_response = robo_response+"I apologize, I don't understand."
  else:
    try:
        s=sent_tokens[idx]
        if type(s)==list:
            s=s[0]
            print(s,'asd#########')
            s=s.question
            robo_response=Today.objects.get(question=s.lower())
            r=robo_response.answer
        elif type(s)==str:
            print('str********')
            robo_response=Today.objects.get(question=s)
            print(robo_response.answer)
            r=robo_response.answer
        robo_response=r
    except:
        robo_response='i will learn and return the results'
  sent_tokens.remove(user_response)  
  return robo_response


@background(schedule=5)
def notify_king():
    print('#################3')
    for update in bot.get_updates():
        user=update.text
        user=user.lower()
        if update.text !='@':
            if(greeting(user) != None):
                user_answer=greeting(user)
            elif(next1(user)!=None):
                user_answer=next1(user)
            else:
                user_answer=response(user)  
        api.send_message(chat_id=update.chat.id,text='@'+user_answer) 
        
@background(schedule=5)
def notify_user():
    log=Client('besties345sp@gmail.com','abc123456')
    for update in bot.get_updates():
        print('hai')
        user=update.text
        user=user.lower()
        if update.text !='@':
            if(greeting(user) != None):
                user_answer=greeting(user)
            elif(next1(user)!=None):
                user_answer=next1(user)
            else:
                user_answer=response(user)  
        api.send_message(chat_id=update.chat.id,text='@'+user_answer)
        aaa=True
        if aaa:
            break
        
    for i in log.fetchAllUsers():
        i=i
        sl=log.fetchThreadMessages(thread_id=i.uid,limit=1)
        al=sl[-1]
        print('h@@@@@@@@@@',al)
        al=al.text
        if al[0]!='@':
            user = al.lower()
            if(greeting(user) != None):
                user_answer=greeting(user)
            elif(next1(user)!=None):
                user_answer=next1(user)
            else:
                user_answer=response(user)      
            log.send(Message(text='@'+user_answer),thread_id=i.uid,thread_type=ThreadType.USER)  
    log.logout()



def index(request):
    if request.method=="POST":
        s=Login(request.POST)
        print(s.is_bound)
        if s.is_valid():
            print('xz')
            k=request.POST['phonenum1']
            k1=request.POST['password9']
            k=s.cleaned_data['phonenum1']
            k1=s.cleaned_data['password9']
            user=authenticate(username=k,password=k1)
            if user:
                a=login(request,user)
                return render(request,'login.html')
        else:
            return render(request,"login.html",{"form":s,"error":"not valid"})
    ss=Today.objects.get(question='who: international health emergency declared over corona virus.')
    return render(request,"login.html",{"form":Login()})
def logout1(request):
    logout(request)
    return render(request,'login.html',{'yes':'you have loggedout'})

            
            
            