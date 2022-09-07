from queue import PriorityQueue
from django.contrib import admin

from .models import BasicQueue, Question, Choice, QueueNode, UserProfile, VipNode, VipQueue



# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile)
admin.site.register(BasicQueue)
admin.site.register(VipQueue)
admin.site.register(QueueNode)
admin.site.register(VipNode)
# admin.site.register(Choice)

