from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	class Meta:
		model = User 
		fields = ['username','email','password','password1']
			
	"""docstring for UserRegistrationForm"""
	def __init__(self, arg):
		super(UserRegisterForm, self).__init__()
		self.arg = arg
		