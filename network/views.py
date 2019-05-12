from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.views.generic import DeleteView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request,'network/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('success')
    else:
        form = UserCreationForm()
    return render(request, 'network/signup.html', {'form': form})

@login_required
def status_view(request):
    user = get_object_or_404(User, pk=request.user.id)
    print(request.user.id)
    status = Status.objects.all().filter(owner_id=user)
    if request.method == 'POST':
        form = StatusForm(request.POST, request.FILES)

        if form.is_valid():
            status = form.save(commit=False)
            status.owner = request.user
            status.save()
            form.save()
            return redirect('success')
    else:
        form = StatusForm()
    return render(request, 'network/status.html', {'form': form, 'status':status})
    #return HttpResponse(status)

@login_required
def success(request):
    status = Status.objects.all()
    comments = Comment.objects.all()
    return render(request,'network/display.html',{'status': status, 'comments':comments})

@login_required
def detail_status(request,id):
    status=get_object_or_404(Status,id=id)
    comments = Comment.objects.filter(status=status).order_by('-id')
    is_liked = False
    if status.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(status=status, user=request.user, content=content)
            comment.save()
            return HttpResponseRedirect(status.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'status':status,
        'is_liked': is_liked,
        'total_likes': status.total_likes(),
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request,'network/status_detail.html',context)
    #return HttpResponse(status)

@method_decorator([login_required], name='dispatch')
class StatusDeleteView(DeleteView):
    model = Status
    context_object_name = 'status'
    template_name = 'network/delete.html'
    success_url = reverse_lazy('mystatus')

    def delete(self, request, *args, **kwargs):
        status = self.get_object()
        messages.success(request, 'The status %s was deleted with success!')
        return super().delete(request, *args, **kwargs)

@login_required
def like_status(request):
    status = get_object_or_404(Status, id=request.POST.get('status_id'))
    is_liked = False
    if status.likes.filter(id=request.user.id).exists():
        status.likes.remove(request.user)
        is_liked = False
    else:
        status.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(status.get_absolute_url())
