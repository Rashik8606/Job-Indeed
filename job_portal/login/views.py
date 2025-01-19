from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomCreationForm
from .models import UserProfile, ChatMessage,JobVacancies
from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef, Q
from rest_framework import generics
from .serializer import MessageSerializer,ProfileSerializer
from .forms import JobVacanciesForm
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from http import HTTPStatus
from rest_framework import status
import requests
import json
from django.http import Http404


def user_register(request):
    if request.method == 'POST':
        form = CustomCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                profile_picture=form.cleaned_data.get('profile_picture', ''),
                location=form.cleaned_data.get('location', ''),
                education=form.cleaned_data.get('education', ''),
                email=form.cleaned_data.get('email', ''),
                skill=form.cleaned_data.get('skill', '')
            )
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = CustomCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html')


def logoutview(request):
    logout(request)
    return redirect('login')



@login_required
def messagePage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'message_page.html', {'user': request.user})



class MyInbox(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        messages = ChatMessage.objects.filter(
            Q(sender_id=user_id) | Q(receiver_id=user_id)
        ).order_by('-date')
        return messages

class GetMessage(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        receiver_id = self.kwargs['receiver_id']
        messages = ChatMessage.objects.filter(
            (Q(sender_id=sender_id, receiver_id=receiver_id) |
             Q(sender_id=receiver_id, receiver_id=sender_id))
        ).order_by('date')
        return messages

class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['sender'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs.get('username', '')
        return UserProfile.objects.filter(
            Q(user__username__icontains=username) |
            Q(location__icontains=username) |
            Q(email__icontains=username)
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"result": "no user found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ProfileDetails(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'



@login_required
def index(request):
    details = JobVacancies.objects.all()
    return render(request, 'index.html', {'disp': details})



    
@login_required
def jobVacanciesViews(request):
    if request.method == 'POST':
        form = JobVacanciesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job vacancy posted successfully!')
            return redirect('index')
    else:
        form = JobVacanciesForm()
    return render(request, 'jobvacancies.html', {'form': form})



class MessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class MessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


def job_listings(request):
    query = request.GET.get('query', '')
    post_job = request.GET.get('post_job', '')
    
    if post_job == 'yes':
        return redirect('jobPost')
        
    joblist = JobVacancies.objects.filter(
        Q(jobTitle__icontains=query) |
        Q(branchEmail__icontains=query) |
        Q(jobQualification__icontains=query) |
        Q(location__icontains=query) |
        Q(contactNumber__icontains=query) |
        Q(applicationEmailUrl__icontains=query) |
        Q(jobSkill__icontains=query) |
        Q(jobType__icontains=query) |
        Q(shortDiscription__icontains=query) |
        Q(jobCategory__icontains=query) |
        Q(jobResposibility__icontains=query) |
        Q(jobRequirement__icontains=query)
    ).order_by('-last_updated')
    
    return render(request, 'job_listings.html', {'disp': joblist})



from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver


@receiver(post_save, sender=JobVacancies)
def send_job_alert(sender,instance,created,**kwargs):
    if created:  
        subject = f"New Job Posting: {instance.jobTitle}"
        message = (
            f"A new job has been posted:\n\n"
            f"Job Title: {instance.jobTitle}\n"
            f"Location: {instance.location}\n"
            f"Category: {instance.jobCategory}\n"
            f"Salary: {instance.get_jobSalary_display()}\n"
            f"Description: {instance.shortDiscription}\n\n"
            f"Apply Here: {instance.applicationEmailUrl}\n"
        )
        
       
        recipient_list = [user.email for user in User.objects.filter(is_active=True)]

       
        send_mail(
            subject,
            message,
            'rrashik409@gmail.com',  
            recipient_list,  
            fail_silently=False,
        )




import logging

logger = logging.getLogger(__name__)

try:
    send_mail(
        'Test Subject',
        'Test Email Body',
        'your-email@gmail.com',
        ['recipient@example.com'],
        fail_silently=False,
    )
except Exception as e:
    logger.error(f"Error sending email: {e}")
