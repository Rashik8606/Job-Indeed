from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_profile')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)  
    education = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  
    phone_num = models.CharField(max_length=10, blank=True, null=True) 
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    skill = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.CharField(max_length=1000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


class JobVacancies(models.Model):

    class JobSalary(models.IntegerChoices):
        LOW = 1, 'Below $20,000'
        MID = 2, '$20,000 - $50,000'
        HIGH = 3, 'Above $50,000'


    class woworkingEnvironment(models.TextChoices):
        REMOTE = 'Remote', 'Remote'
        ONSITE = 'Onsite', 'Onsite'
        HYBRID = 'Hybrid', 'Hybrid'

    jobTitle = models.CharField(max_length=255)
    branchEmail = models.EmailField()
    jobQualification = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contactNumber = models.IntegerField()
    applicationEmailUrl = models.EmailField()
    jobSkill = models.TextField()
    jobType = models.TextField()
    jobSalary = models.IntegerField(
        choices = JobSalary.choices,
        default = JobSalary.LOW 
    )
    workingEnvironment = models.TextField(
        max_length=255,
        choices = woworkingEnvironment.choices,
        default=woworkingEnvironment.REMOTE
    )
    shortDiscription = models.TextField()
    jobCategory = models.CharField(max_length=255)
    jobResposibility = models.CharField(max_length=255)
    jobRequirement = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    companyLogo = models.ImageField(upload_to='company_logo',blank=True,null=True,default='company_logo/default_logo.png')



    def __str__(self) -> str:
        return self.jobTitle




# Message Test ------------>


