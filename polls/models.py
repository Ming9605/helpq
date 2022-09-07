from cProfile import Profile
from dataclasses import dataclass
import datetime
from operator import truediv
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=1, default= "None", null=True)
    roles = models.TextField(User, default="student")
    priority = models.BooleanField(default=False)
    # age = models.IntegerField(default=69, null=True)

    def is_in_Queue(self):
        main = BasicQueue.objects.all()[0]
        for id in main.data.split():
            node = QueueNode.objects.get(pk=int(id))
            if node.data == self:
                return True
        main = VipQueue.objects.all()[0]
        for id in main.data.split():
            node = QueueNode.objects.get(pk=int(id))
            if node.data == self:
                return True
        return False


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


# questions
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

'''
Beginning from here are the CSIA codes for the Help Queue apart of the IA's Criterion C section !
'''
# Classes for each account and stats placed below them

'''
class VipUser(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=1, default= "None", null=True)
    age = models.IntegerField(default=69, null=True)

    def AddName(name):
        user = name
'''


#Help queue
class QueueNode(models.Model):
    data = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    @classmethod
    def create(cls, data):
        queuenode = cls(data = data) 
        return queuenode
    

class VipNode(models.Model):
    data = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    @classmethod
    def create(cls, data):
        vipnode = cls(data = data) 
        return vipnode
    

class BasicQueue(models.Model):
    data = models.TextField(default = "", null = True)
    
    def getData(self):
        return [QueueNode.objects.get(pk=int(id)) for id in self.data.split()]

    def addNode(self, node):
        self.data += " " + str(node.id)
        self.save()

    def dismissNode(self, node):
        n = self.getData()
        n.remove(node)
        data = " ".join([str(each.id) for each in n])

class VipQueue(models.Model):
    data = models.TextField(default = "", null = True)

    def getData(self):
        return [VipNode.objects.get(pk=int(id)) for id in self.data.split()]

    def addNode(self, node):
        self.data += " " + str(node.id)
        self.save()

    def dismissNode(self, node):
        n = self.getData()
        n.remove(node)
        data = " ".join([str(each.id) for each in n])