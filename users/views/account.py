from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters, sensitive_variables
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.forms import PasswordResetForm

@login_required
@sensitive_variables()
@sensitive_post_parameters()
def change_password(request):
	status = ''
	old_password = request.POST.get('old_password')
	new_password = request.POST.get('new_password')
	verify_password = request.POST.get('verify_password')
	if old_password and new_password and verify_password:
		if request.user.check_password(old_password):
			if new_password == verify_password:
				request.user.set_password(new_password)
				request.user.save()
				status = 'success'
			else: status = 'password_mismatch'
		else: status = 'invalid_login'
	return render(request, 'users_change_password.html', {'status': status})

def reset_password(request, user=None):
	form = PasswordResetForm(request.GET)	# Able to fill in using GET params
	if request.method == 'POST':
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			form.save()
			status = ['success']
		else:
			status = form.errors	
	return render(request, 'users_reset_password.html', {'form': form})

@sensitive_variables
@sensitive_post_parameters
def reset_password_confirm(request, token):
	status = ''

	return render(request, 'users_change_password.html', {'status': status})
