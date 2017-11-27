from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    name = forms.CharField(max_length=20, label='Name')
    country = forms.CharField(max_length=30, label='Country')
    phone = forms.CharField()
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')


    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'phone', 'country', 'password1', 'password2')
        # 'name', 'phone', 'country',

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    # def clean_phone(self):
    #     phone = self.cleaned_data.get('phone')
    #     username = self.cleaned_data.get('username')
    #     if phone and User.objects.filter(phone=phone).exclude(username=username).exists():
    #         raise forms.ValidationError(u'Phone number must be unique.')
    #     return phone


@login_required
@transaction.atomic
def Update_Profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
