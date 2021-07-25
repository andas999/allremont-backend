from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	context = {
		'posts':posts
	}
	return render(request, '/home.html',context)

def about(request):
	return render(request, '/about.html', {'title': 'About'})
