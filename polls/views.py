from queue import PriorityQueue
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .models import VipNode, VipQueue, QueueNode, BasicQueue, UserProfile
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView


# classes to handle auth
class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('polls:index')

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_message = "Your profile was created successfully"
    success_url = reverse_lazy('polls:index')

class IndexView(TemplateView): 
    template_name = 'polls/index.html'


# error handling 
def profile(request):
    user = request.user

    try:
        if request.method == "POST":
            data= request.POST
            user.username = data.get("username")
            user.first_name = data.get("firstname")
            user.last_name = data.get("lastname")
            user.userprofile.gender = data.get("gender")
            user.userprofile.birthday = data.get("birthday")
            user.userprofile.roles = data.get("roles")
            user.save()
            user.userprofile.save()
            print(data.get("roles"))
            
    except:
        # display error
        pass

    return render(request, 'polls/profile.html', {
        'user': user, 
        })

def Queue(request):
    user = request.user
    main = BasicQueue.objects.all()[0]
    p_main = VipQueue.objects.all()[0]
    try:
        print(main.data)
        
        if request.method == "POST":
            
            print(request.POST)
            if "Add Name" in request.POST:
                print(request.POST.__dict__)
                new_node = QueueNode.create(user.userprofile)
                new_node.save()
                main.addNode(new_node)
                main.save()
            if "dismiss" in request.POST:
                student_name = " ".join(request.POST.get('dismiss').split()[1:])
                for id in main.data.split():
                    node = QueueNode.objects.get(pk=int(id))
                    if node.data.user.username == student_name:
                        current = str(node.id)
                        q = main.data.split()
                        q.remove(current)
                        main.data = " ".join(q)
                        main.save()
                        break
            if "priority-dismiss" in request.POST:
                student_name = " ".join(request.POST.get('priority-dismiss').split()[1:])
                for id in p_main.data.split():
                    node = VipNode.objects.get(pk=int(id))
                    if node.data.user.username == student_name:
                        current = str(node.id)
                        q = p_main.data.split()
                        q.remove(current)
                        p_main.data = " ".join(q)
                        p_main.save()
                        break
            if "priority" in request.POST:
                print('bruh')
                student_name = " ".join(request.POST.get('priority').split()[1:])
                print(student_name)
                for id in main.data.split():
                    node = QueueNode.objects.get(pk=int(id))
                    if node.data.user.username == student_name:
                        current = str(node.id)
                        q = main.data.split()
                        q.remove(current)
                        main.data = " ".join(q)
                        main.save()
                        
                        print(request.POST.__dict__)
                        new_node = VipNode.create(node.data)
                        
                        new_node.save()
                        print(new_node)
                        p_main.addNode(new_node)
                        p_main.save()

    except:
        pass
    print([VipNode.objects.get(pk=int(id)).data for id in p_main.data.split()])
    return render(request, 'polls/queue.html', {'student_list':[QueueNode.objects.get(pk=int(id)).data for id in main.data.split()], 'p_student_list':[VipNode.objects.get(pk=int(id)).data for id in p_main.data.split()]})