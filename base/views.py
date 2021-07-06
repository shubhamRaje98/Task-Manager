from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView 
from .models import Task 
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin  # set LOGIN_URL = 'login' in settings.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 

class RegisterPage(FormView):
	template_name = 'base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('tasks')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(RegisterPage, self).form_valid(form)   	#form_valid() of super class is being called

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('tasks')
		return super(RegisterPage, self).get(*args, **kwargs)

class CustomLoginView(LoginView):
	template_name = 'base/login.html'
	fields = '__all__'
	redirect_authenticated_user = True
	
	def get_success_url(self):
		return reverse_lazy('tasks')
	

class TaskList(LoginRequiredMixin, ListView):
	model = Task                     #for template it looks for modelName_list.html
	context_object_name = 'tasks'    # looks for task_list.html
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tasks'] = context['tasks'].filter(user=self.request.user)
		context['count'] = context['tasks'].filter(complete=False).count()

		search_input = self.request.GET.get('search-area')
		
		if search_input:
			context['tasks'] = context['tasks'].filter(title__icontains=search_input) or ''
		else:
			search_input = ""

		context['search_input'] = search_input

		return context 	

class TaskDetail(LoginRequiredMixin, DetailView):
	model = Task 					#looks for modelName_detail.html
	context_object_name = 'task'	# looks for task_detail.html
	template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
	model = Task 
	fields = ['title', 'description', 'complete']
	success_url = reverse_lazy('tasks')

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(TaskCreate, self).form_valid(form) 

class TaskUpdate(LoginRequiredMixin, UpdateView):
	model = Task 
	fields = ['title', 'description', 'complete']
	success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
	model = Task
	fields = '__all__'
	context_object_name = 'task'
	success_url = reverse_lazy('tasks')