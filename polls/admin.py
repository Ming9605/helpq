from queue import PriorityQueue
from django.contrib import admin

from .models import BasicQueue, Decision, QueueNode, UserProfile, VipNode, VipQueue



# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Decision
    extra = 3


admin.site.register(UserProfile)
admin.site.register(BasicQueue)
admin.site.register(VipQueue)
admin.site.register(QueueNode)
admin.site.register(VipNode)


