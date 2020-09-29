from django.db import models

class Today(models.Model):
    question=models.CharField(max_length=1000)
    answer=models.CharField(max_length=1000000)
    
    def __str__(self):
        return "{0}- {1}".format(self.question,self.answer)
class Userphone(models.Model):
    number=models.CharField(max_length=10)
    ans=models.CharField(max_length=100,null=True)
    def __str__(self):
        return f"{self.number}-{self.ans}"