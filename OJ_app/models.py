from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    Firstname=models.CharField(max_length=20)
    Lastname=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=30)

    def __str__(self):
        return self.Firstname

class Problem(models.Model):
    
    class Difficulty(models.TextChoices):
        easy = "EASY"
        medium = "MEDIUM"
        hard = "HARD"

    problemid = models.CharField(("ID"),max_length=50)
    problemname = models.CharField(("name"),max_length=50)
    description= models.CharField(max_length=300)
    difficulty = models.CharField(
        max_length=6, 
        choices=Difficulty.choices,
        default=Difficulty.easy
    )
    def __str__(self):
          return str(self.problemid) + " " +self.problemname


class Submission(models.Model):


    class Verdict(models.TextChoices):
        Success = "SUCCESS"
        COMPILATION_ERROR = "COMPILATION_ERROR"
        Wrong_Output = "Wrong Output"
        Time_Limit_Exceeded = "TIME LIMIT EXCEEDED"
        Runtime_Error = "RUNTIME ERROR"


    problemid=models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(
        max_length=20,
        choices=Verdict.choices
    )
    submissiontime=models.TimeField(default=timezone.now)
  
    def __str__(self):
       return str(self.problemid) + str(self.submissiontime)


class Testcase(models.Model):
    problemid = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input=models.CharField(max_length=500)
    output=models.CharField(max_length=500)

    def __str__(self):
       return str(self.problemid)

