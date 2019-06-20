from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from apps.application.models import User
from .models import Message, Comment
import datetime
from django.utils import timezone
from time import localtime, strftime

# Create your views here.
def wall(request):

    if 'userid' in request.session:
        now = datetime.datetime.now()
        user = User.objects.get(id=request.session['userid'])
        context = {
            "user": user,
            "allMessages": Message.objects.all().order_by("-created_at"),
            "thirtyAgo": now - datetime.timedelta(minutes=30),

        }
        return render(request, "wall/index.html", context)
    else:
        return redirect(reverse('home:index'))

def postMessage(request):
    message = request.POST['message']
    newMessage = Message.objects.create(user=User.objects.get(id=request.session['userid']), message=message)
    return redirect("/wall")

def postComment(request):
    comment = request.POST['comment']
    print(request.POST['messageId'])
    user = User.objects.get(id=request.session['userid'])
    message = Message.objects.get(id=request.POST['messageId'])
    newComment = Comment.objects.create(message=message, user=user, comment=comment)
    return redirect("/wall")

def deleteMessage(request, id):
    print("i am deleting a message")
    messageToDelete = Message.objects.get(id=id)
    messageToDelete.delete()
    return redirect("/wall")
