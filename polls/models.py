from cProfile import Profile
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    roles = models.TextField(User, default="student")
    priority = models.BooleanField(default=False)

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



class Decision(models.Model):
    decision_text = models.CharField(max_length=200)

    def __str__(self):
        return self.decision_text



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